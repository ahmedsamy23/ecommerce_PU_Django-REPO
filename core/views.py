from django.db.models import ObjectDoesNotExist
from django.shortcuts import redirect, render , get_object_or_404
from .models import Item , OrderItem , Order , Refund
from .forms import QuantityForm , RefundForm
from django.views.generic import ListView , DetailView , View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import SearchFilter
from django.db import transaction
# Create your views here.

class ItemListView(ListView):
    model = Item
    template_name = 'core/items_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by category if provided in Url
        category = self.kwargs.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Apply search filter
        self.FilterSet = SearchFilter(self.request.GET, queryset=queryset)
        return self.FilterSet.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.FilterSet
        context['categories'] = Item.objects.values_list('category', flat=True).distinct()
        context['selected_category'] = self.kwargs.get('category')
        context['men_count'] = Item.objects.filter(category='Men').count()
        context['women_count'] = Item.objects.filter(category='Women').count()
        context['kids_count'] = Item.objects.filter(category='Kids').count()
        context['accessories_count'] = Item.objects.filter(category='Accessories').count()
        context['beauty_count'] = Item.objects.filter(category='Beauty').count()
        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'core/item_detail.html'
    context_object_name = 'item'
    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuantityForm()
        return context


class OrderSummaryView(LoginRequiredMixin , View):
    def get(self , *args , **kwargs):
        try:
            order = Order.objects.get(user = self.request.user , ordered = False)
            if order.items.count == 0:
                messages.error(self.request , "Your cart is empty")
                return redirect("core:item-list")
            context = {
                'object': order,                
            }
            return render(self.request , 'core/order_summary.html' , context)
        except ObjectDoesNotExist:
            messages.error(self.request , "You do not have an active order")
            return redirect("core:item-list")

@login_required
def add_quantity(request , slug):
    item = get_object_or_404(Item , slug = slug)
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')

            order_item , created = OrderItem.objects.get_or_create(
                item = item,
                user = request.user,
                ordered = False
            )
            order_qs = Order.objects.filter(user = request.user , ordered = False)
            if order_qs.exists():
                order = order_qs[0]
                if order.items.filter(item__slug = item.slug).exists():
                    order_item.quantity += quantity
                    order_item.save()
                    messages.success(request , 'Quantity was updated')
                    return redirect('core:order-summary')
                else:
                    order.items.add(order_item)
                    order_item.quantity = quantity
                    order_item.save()
                    messages.success(request , 'Item was added to your cart')
                    return redirect('core:order-summary')
            else:
                ordered_date = timezone.now()
                order = Order.objects.create(user = request.user , ordered_date = ordered_date)
                order.items.add(order_item)
                messages.success(request , 'Item was added to your cart')
            return redirect('core:order-summary')
        else:
            messages.error(request , 'Invalid form submission')
            return redirect('core:order-summary')
    else:
        messages.error(request , 'Invalid request method')
        return redirect('core:order-summary')



@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item , slug=slug)
    order_item , create = OrderItem.objects.get_or_create(
        user = request.user,
        item = item , 
        ordered = False
    )
    order_qs = Order.objects.filter(user = request.user , ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request , 'Item quantity was updated')
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.success(request , 'Item was added to your cart')
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user , ordered_date = ordered_date)
        order.items.add(order_item)
        messages.success(request , 'Item was added to your cart')
    return redirect("core:order-summary")

@login_required
def remove_from_cart(request , slug):
    item = get_object_or_404(Item , slug=slug)
    order_qs = Order.objects.filter(user = request.user , ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                user = request.user , 
                item = item , 
                ordered = False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.success(request , 'Item was Removed From Your Cart')
            return redirect('core:order-summary')
        else:
            messages.info(request, "This Item Was Not in Your Cart")
            return redirect('core:order-summary')
    else:
        messages.info(request, 'You Do Not Have an Active Order')
        return redirect('core:order-summary')

@login_required
def remove_single_item_from_cart(request , slug):
    item = get_object_or_404(Item , slug = slug)
    order_qs = Order.objects.filter(user = request.user , ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(
                user = request.user , 
                item = item ,
                ordered = False
            )[0]
            if order_item.quantity > 1 :
                order_item.quantity -= 1
                order_item.save()
                messages.success(request , 'Item quantity was updated')
                return redirect('core:order-summary')
            else:
                order.items.remove(order_item)
                order_item.delete()
                messages.success(request , 'Item was removed from your cart')
                return redirect('core:order-summary')
        else:
            messages.info(request , 'This item was not in your cart')
            return redirect('core:order-summary')
    else:
        messages.info(request , 'You do not have an active order')
        return redirect('core:order-summary')


class RequestRefundView(LoginRequiredMixin , View):
    def get(self , *args , **kwargs):
        form = RefundForm()
        context = {
            'refund_form': form
        }
        return render(self.request , 'core/request_refund.html' , context)
    
    def post(self , *args , **kwargs):
        form = RefundForm(self.request.POST or None)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            try :
                order = Order.objects.get(ref_code = ref_code)
                with transaction.atomic():
                    order.refund_requested = True
                    order.save()
                    refund = Refund.objects.create(
                        order = order,
                        reason = message,
                        email = email
                    )
                    messages.info(self.request , 'Refund Request Sent , Please wait for the response')
                    return redirect('core:request-refund')
            except ObjectDoesNotExist:
                messages.info(self.request , 'This order does not exist')
                return redirect('core:request-refund')
        else:
            messages.warning(self.request , 'Invalid form submission')
            return redirect('core:request-refund')
        return render(self.request , 'core/request_refund.html')