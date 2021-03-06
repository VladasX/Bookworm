from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import F
from bookworm.books_api import search_query
from bookworm.models import UserProfile, Book, Review, ReadingList
from bookworm.forms import UserForm, UserProfileForm, ReviewForm, ReadingListForm, ReadingListFormChange
from django.http import JsonResponse
from math import ceil

#Displays home page.
def index(request):
	highest_rated = Book.objects.order_by("-averageRating")[:12]
	most_viewed = Book.objects.order_by("-pageViews")[:12]
	recent_reviewed = Review.objects.order_by("-timestamp")[:12]
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
	stored =  None
	if request.user.is_authenticated():
		stored = ReadingList.objects.filter(user=request.user, book=book_data)
		if stored:
			stored = stored[0].status
	if book_data:
		book_data.pageViews = (book_data.pageViews+1)
		book_data.save()
		try:
			user = User.objects.get(username=request.user.username)
			form = ReadingListForm()
			if request.method == 'POST':
				form = ReadingListForm(request.POST)
				if form.is_valid():
					readinglist_data = ReadingList.objects.get_or_create(user=request.user, book=book_data)[0]
					readinglist_data.status = form.cleaned_data['status']
					readinglist_data.pagesread = 0
					readinglist_data.save()
					stored = readinglist_data.status
			else:
				render(request, 'bookworm/book_page.html', {'book_data': book_data, 'reviews': reviews, 'status': stored, 'form': form})
		except User.DoesNotExist:
			return render(request, 'bookworm/book_page.html', {'book_data': book_data, 'reviews': reviews})
		return render(request, 'bookworm/book_page.html', {'book_data': book_data, 'reviews': reviews, 'status': stored, 'form': form})
	return render(request, 'bookworm/error.html')

#Displays a list of books that are stored in the database.
def book_list(request, pages=1, sort="pageViews"):
	sortdic = {"title": "Title", "authors": "Authors", "publishedDate": "Published Date", "averageRating": "Average Rating", "pageCount": "Page Count", "pageViews": "Views"}
	if sort not in sortdic.keys():
		return render(request, "bookworm/error.html")
	# This will be sorted in alphabetical order.
	if sort in ["title", "authors"]:
		books = Book.objects.order_by(F("{}".format(sort)).asc(nulls_last=True))
	# Everything numerical will be sorted in descending order.
	else:
		books = Book.objects.order_by(F("{}".format(sort)).desc(nulls_last=True))
	start = (int(pages)-1)*12
	next = int(pages)+1
	previous = int(pages)-1
	last = ceil(len(books)/12)
	return render(request, "bookworm/book_list.html", 
	{'books': books[start:start+12], 'range': range(ceil(len(books)/12)), 'next': next, 'previous': previous, 'last': last, 'currentpage': int(pages), 'sort': {"method": sort, "text": sortdic[sort]}})

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
			book_review.rating = form.cleaned_data['rating']
			book_review.save()
			reviews = Review.objects.filter(book_id=book.bookid)
			if len(reviews) != 0:
				average = 0
				for review in reviews:
					average += review.rating
				book.averageRating = round(average/len(reviews))
			else:
				book.averageRating = book_review.rating
			book.save()
			return redirect('/book/{}'.format(book.bookid))
		else:
			print(form.errors)
	return render(request, 'bookworm/add_review.html', {'form': form})

#Allows to see the reading list of a person.
def reading_list(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('index')
	reading_data = ReadingList.objects.filter(user=user)
	if request.method == 'POST':
				form = ReadingListFormChange(request.POST)
				if form.is_valid():
					bookid = form.cleaned_data['bookid']
					book_data = Book.objects.get(bookid=bookid)
					readinglist_data = ReadingList.objects.get(user=user, book=book_data)
					readinglist_data.status = form.cleaned_data['status']
					readinglist_data.pagesread = form.cleaned_data['pages']
					if readinglist_data.pagesread and readinglist_data.pagesread == book_data.pageCount:
						readinglist_data.status = 1
					elif readinglist_data.pagesread and readinglist_data.pagesread > book_data.pageCount:
						readinglist_data.pagesread = book_data.pageCount
						readinglist_data.status = 1
					readinglist_data.save()
	if reading_data:
		return render(request, 'bookworm/reading_list.html', {'reading_data': reading_data, 'selecteduser': user})
	return render(request, 'bookworm/reading_list.html', {'reading_data': {}, 'selecteduser': user})
	
def delete(request, username, bookid):
	user = User.objects.get(username=username)
	book_data = Book.objects.get(bookid=bookid)
	data = ReadingList.objects.filter(user=user, book=book_data)
	data.delete()
	return HttpResponseRedirect('/reading_list/{}'.format(username))

#Displays a user's profile.
def profile(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('index')
	userprofile = UserProfile.objects.get_or_create(user=user)[0]
	review = {}
	book = None
	if userprofile.favouriteBook:
		try:
			review = Review.objects.get(book=userprofile.favouriteBook, user=user)
		except:
			pass
		book = Book.objects.get(bookid=userprofile.favouriteBook)
	form = UserProfileForm(
		{'bio': userprofile.bio, 'picture': userprofile.picture})
	return render(request, 'bookworm/profile.html',
		{'userprofile': userprofile, 'selecteduser': user, 'form': form, 'book': book, 'review': review})

#Allows them to edit their user profile.
@login_required
def profile_edit(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('index')
	userprofile = UserProfile.objects.get_or_create(user=user)[0]
	reading_data = ReadingList.objects.filter(user=user)
	form = UserProfileForm(
		{'bio': userprofile.bio, 'picture': userprofile.picture})
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
		if form.is_valid():
			form.save(commit=True)
			return redirect('profile_edit', user.username)
	return render(request, 'bookworm/profile_edit.html',
		{'userprofile': userprofile, 'selecteduser': user, 'readingList': reading_data, 'form': form})

#Used for an ajax call to see if a username is taken or not.
def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)