from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from bookworm.books_api import search_query
from bookworm.models import UserProfile, Book, Review
from bookworm.forms import UserForm, UserProfileForm, ReviewForm

#Displays home page.
def index(request):
	highest_rated = Book.objects.order_by("-averageRating")[:4]
	most_viewed = Book.objects.order_by("-pageViews")[:4]
	recent_reviewed = Review.objects.order_by("-timestamp")[:4]
	return render(request, 'bookworm/index.html', {'highest_rated': highest_rated, 'most_viewed': most_viewed, 'recent_reviewed': recent_reviewed})

#Gets a list of books based on a user's query and displays it.
def book_search(request):
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = search_query(query)
	return render(request, 'bookworm/book_search.html', {'result_list': result_list})

#Gets data about a specific book and displays it.
def book_page(request, bookid):
	book_data = Book.objects.get(bookid=bookid)
	reviews = Review.objects.filter(book_id=book_data.bookid)
	if book_data:
		book_data.pageViews = (book_data.pageViews+1)
		book_data.save()
		return render(request, 'bookworm/book_page.html', {'book_data': book_data, 'reviews': reviews})
	return render(request, 'bookworm/error.html')

#Displays a list of books that are stored in the database.
def book_list(request): #Maybe add the ability to allow them to sort the list.
	context_dict = {}
	books = Book.objects.order_by("averageRating")
	context_dict["books"] = books
	return render(request, "bookworm/book_list.html", context_dict)

#Allows a user to add a review for a book.
@login_required
def add_review(request, bookid):
	try:
		user = User.objects.get(username=request.user.username)
	except User.DoesNotExist:
		return redirect('index')
	try:
		book = Book.objects.get(bookid=bookid)
	except Book.DoesNotExist:
		return redirect('index')
	form = ReviewForm()
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		if form.is_valid():
			book_review = Review.objects.get_or_create(user=request.user, book=book)[0]
			book_review.text = form.cleaned_data['text']
			book_review.save()
			reviews = Review.objects.filter(book_id=book.bookid)
			return render(request, 'bookworm/book_page.html', {'book_data': book, 'reviews': reviews})
		else:
			print(form.errors)
	return render(request, 'bookworm/add_review.html', {'form': form})

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

#Allows them to edit their user profile.
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
