from django.views.generic import ListView , DetailView , CreateView , UpdateView , DeleteView
from .models import Blog , Comment , Category , CommentReply
from django.shortcuts import redirect , render
from django.urls import reverse_lazy
from .forms import BlogForm , CommentForm , CommentReplyForm
from django.contrib import messages
# Create your views here.

class BlogListView(ListView):

    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 12
    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset
    
class BlogDetailView(DetailView):

    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs) 
        context['comments'] = Comment.objects.filter(blog = self.get_object())
        context['categories'] = Category.objects.all()
        context['comment_form'] = CommentForm()
        context['comment_reply_form'] = CommentReplyForm()
        context['recent_blogs'] = Blog.objects.exclude(id = self.get_object().id).order_by('-created_at')[:5]
        return context
    
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.user = request.user
            comment.blog = self.get_object()
            comment.save()
            messages.success(request , 'Comment Created Successfully')
            return redirect('blog:blog-detail' , self.get_object().slug)
        form = CommentForm()
        return super().post(request, *args, **kwargs)

class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_create.html'
    success_url = reverse_lazy('blog:blog-list')
    form_class = BlogForm

    def form_valid(self, form):
        blog = form.save(commit = False)
        blog.user = self.request.user
        blog.save()
        messages.success(self.request , 'Blog Created Successfully')
        return super().form_valid(form)



class BlogUpdateView(UpdateView):
    model = Blog
    template_name = 'blog/blog_edit.html'
    success_url = reverse_lazy('blog:blog-list')
    form_class = BlogForm
    context_object_name = 'blog'

    def form_valid(self, form):
        blog = form.save(commit = False)
        blog.save()
        messages.success(self.request , 'Blog Updated Successfully')
        return super().form_valid(form)    

    def get_queryset(self):
        return super().get_queryset().filter(user = self.request.user)


class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('blog:blog-list')
    context_object_name = 'blog'

    def get_queryset(self):
        return super().get_queryset().filter(user = self.request.user)

def comment_reply(request , id):
    try:
        comment = Comment.objects.get(id = id)
        if request.method == 'POST':
            form = CommentReplyForm(request.POST)
            if form.is_valid():
                comment_reply = form.save(commit = False)
                comment_reply.user = request.user
                comment_reply.comment = comment
                comment_reply.save()
                messages.success(request , 'Comment Reply Created Successfully')
                return redirect('blog:blog-detail' , comment.blog.slug)
            form = CommentReplyForm()
    except Comment.DoesNotExist:
        messages.error(request , 'Comment Not Found')
        return redirect('blog:blog-list')
    return redirect('blog:blog-detail' , comment.blog.slug)

def comment_delete(request , id):
    try:
        comment = Comment.objects.get(id = id)
        if request.method == 'POST':
            if request.user == comment.user:
                comment.delete()
                messages.success(request , 'Comment Deleted Successfully')
                return redirect('blog:blog-detail' , comment.blog.slug)
            else:
                messages.error(request , 'You are not allowed to delete this comment')
                return redirect('blog:blog-detail' , comment.blog.slug)
    except Comment.DoesNotExist:
        messages.error(request , 'Comment Not Found')
        return redirect('blog:blog-list')
    return redirect('blog:blog-detail' , comment.blog.slug)