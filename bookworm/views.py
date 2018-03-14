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

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                "bookworm/register.html",
                {"user_form": user_form,
                "profile_form": profile_form,
                "registered": registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponse("Your Bookworm account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "bookworm/login.html", {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))