from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import RegistrationForm, LoginForm, UpdateProfileForm
from .models import UserProfile


class SignUp(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('users_management:login')
    template_name = 'users_management/registration.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign In'  # Add your title here
        return context


class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'users_management/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log In'

        return context

    def get_success_url(self):
        return reverse_lazy('core:main')


class UserProfileView(LoginRequiredMixin, UpdateView, DetailView):
    model = UserProfile
    form_class = UpdateProfileForm
    template_name = 'users_management/user_profile.html'

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('users_management:user_profile', kwargs={'user_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'User Profile'
        context['user_details'] = UserProfile.objects.filter(user=self.request.user)

        return context


def logout_user(request):
    logout(request)
    return redirect('core:main')



