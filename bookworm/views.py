from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from bookworm.books_api import search_query, book_query
from bookworm.models import UserProfile
from bookworm.forms import UserForm, UserProfileForm

def index(request):
	return render(request, 'bookworm/index.html')

#Gets a list of books based on a user's query and displays it.
def search(request):
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = search_query(query)
	return render(request, 'bookworm/search.html', {'result_list': result_list})

#Gets data about a specific book and displays it.
def book_page(request, book_id):
	book_data = book_query(book_id)
	if book_data:
		return render(request, 'bookworm/book_page.html', {'book_data': book_data})
	return render(request, 'bookworm/error.html')

#Displays a user's profile.

def profile(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('index')
	userprofile = UserProfile.objects.get_or_create(user=user)[0]
	form = UserProfileForm(
		{'bio': userprofile.bio, 'picture': userprofile.picture})
	return render(request, 'bookworm/profile.html',
		{'userprofile': userprofile, 'selecteduser': user, 'form': form})

#Displays a user's profile and allows them to edit it if it's theirs.

@login_required
def profile_edit(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('index')
	userprofile = UserProfile.objects.get_or_create(user=user)[0]
	form = UserProfileForm(
		{'bio': userprofile.bio, 'picture': userprofile.picture})
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
		if form.is_valid():
			form.save(commit=True)
			return redirect('profile_edit', user.username)
		else:
			print(form.errors)
	return render(request, 'bookworm/profile_edit.html',
		{'userprofile': userprofile, 'selecteduser': user, 'form': form})
