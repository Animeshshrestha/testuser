import os, pdb, ast

from django.conf import settings

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from django.contrib import messages

from .forms import UserSignupForm, UserLoginForm

def logout_view(request):

	logout(request)
	return HttpResponse("You are logged out ")

class UserLoginView(View):

	template_name = 'userlogin.html'
	form_class = UserLoginForm

	def get(self,request):

		form = self.form_class(None)
		try:
			if request.session['signup-sucess']:
				messages.info(request,request.session['signup-sucess'])
		except:
			pass

		return render(request, self.template_name, {'form':form})

	def post(self, request):

		form = self.form_class(request.POST)

		if form.is_valid():
			user_email = request.POST.get('email')
			password = request.POST.get('password')

			user = authenticate(email=user_email, password=password)

			if user is not None:

				login(request, user)
				request.session['signup-sucess'] = dict()
				return HttpResponse("Its okay")

			messages.error(request,"Invalid user/email combination")
			return render(request, self.template_name,{'form':form})
			
		request.session['signup-sucess'] = dict()	
		return render(request, self.template_name,{'form':form})		


class UserSignupView(View):

	template_name = 'usersignup.html'
	form_class = UserSignupForm

	def get(self,request):

		form = self.form_class(None)
		return render(request,self.template_name, {'form':form})

	def post(self, request):

		form = self.form_class(request.POST)
		if form.is_valid():

			user = form.save(commit=False)
			password = form.cleaned_data['password']
			user.set_password(password)
			user.is_active=True
			user.save()
			request.session['signup-sucess'] = "Please login to continue the rest form filler"
			return redirect('user-login')

		return render(request,self.template_name,{'form':form})
