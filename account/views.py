from django.shortcuts import redirect, render
from django.views.generic import RedirectView, View
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

from .forms import SignUpForm, LoginForm, ChangePasswordForm


class CustomerSigninView(FormView):
    template_name = 'account/signin.html'
    form_class = SignUpForm
    success_url = '/login/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CustomerLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = LoginForm
    success_url = '/'


class CustomerLogoutView(RedirectView):
    url = '/account/login/'

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class ChangePasswordView(View):
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm(user=request.user)
        context = {
            'form': form
        }
        return render(request, 'account/changepass.html', context)

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        context = {
            'form': form
        }
        return render(request, 'account/changepass.html', context)
