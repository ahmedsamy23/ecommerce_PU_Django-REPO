from django.views.generic import CreateView , DetailView , UpdateView , DeleteView
from .forms import ProfileForm, Signupform, UserForm
from django.urls import reverse_lazy
from .models import UserProfile , City
from django.shortcuts import redirect

# Create your views here.

class SignupView(CreateView):
    form_class = Signupform
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
class ProfileView(DetailView):
    model = UserProfile
    template_name = 'accounts/profile.html' 
    context_object_name = 'profile' 
    def get_object(self):
        return self.request.user.userprofile

class ProfileEditView(UpdateView):
    model = UserProfile
    fields = ['bio' , 'phone_number' , 'image' , 'city']
    template_name = 'accounts/profile_edit.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def post(self, request, *args, **kwargs):
        userform = UserForm(request.POST ,instance = request.user)
        profileform = ProfileForm(request.POST , request.FILES ,instance = self.get_object())
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profile = profileform.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('accounts:profile')
        else:
            userform = UserForm(instance = request.user)
            profileform = ProfileForm(instance = self.get_object())
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userform'] = UserForm(instance=self.request.user)
        context['profileform'] = ProfileForm(instance=self.get_object())
        context['cities'] = City.objects.all()
        return context

class DeleteProfileView(DeleteView):
    model = UserProfile
    template_name = 'accounts/delete_profile.html'
    success_url = reverse_lazy('accounts:signup')

    def get_object(self , queryset=None):
        return self.request.user.userprofile