from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from bookworm.books_api import search_query, book_query
from bookworm.forms import UserForm, UserProfileForm

def index(request):
	return HttpResponse("Welcome!")

def search(request):
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = search_query(query)
	return render(request, 'bookworm/search.html', {'result_list': result_list})

def book_page(request, book_id):
	book_data = book_query(book_id)
	if book_data:
		return render(request, 'bookworm/book_page.html', {'book_data': book_data})
	return HttpResponse("Error, book not found.")