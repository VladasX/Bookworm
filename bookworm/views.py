from django.shortcuts import render
from django.http import HttpResponse
from bookworm.books_api import search_query

def index(request):
        return HttpResponse("Welcome!")

def search(request):
	result_list = []
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = search_query(query)
	return render(request, 'bookworm/search.html', {'result_list': result_list})
