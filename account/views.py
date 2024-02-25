from django.shortcuts import render
from django.views import View
from . import forms
from django.contrib.auth.views import LoginView as django_login_view
from django.contrib.auth import logout
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.


class SignupView(View):
    def get(self, request):
        form = forms.SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return render(request, 'registration/signup_thankyou.html')
        return render(request, 'registration/signup.html', {'form': form})


class LoginView(django_login_view):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    form_class = forms.LoginForm

    def post(self, request, *args, **kwargs):
        return super().post(*args, **kwargs)



def logout_view(request):
    logout(request)
    return redirect('store:list_products')

