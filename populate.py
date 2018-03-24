import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wad2_project.settings")

import django
django.setup()
from django.contrib.auth.models import Group, Permission
from bookworm.books_api import search_query
from bookworm.models import User, UserProfile, Book, Review, ReadingList
from random import randint, choice, shuffle
from string import ascii_uppercase

booklist = ["Harry Potter", "Hunger Games", "Lord of the rings", "Game of thrones", "Pride and Prejudice", "Jane Eyre", "Nineteen Eighty-Four", "The Hitchhiker's Guide to the Galaxy", "The Hobbit", "The Catcher in the Rye", "Frankenstein", "Moby-Dick", "The Scarlet Letter", "Dracula", "Django Unchained", "Algorithms", "Django", "Web App Development"]
usernames = ["Jane", "John", "Joe", "Mark", "Dylan", "Samantha", "Oliver", "Emily", "Ryan", "Scott", "Freya", "Aiden", "James", "Harris", "Jackson", "Lola", "Lily", "Mia", "Sophie", "Sarah", "Brandon", "Tom", "Harry", "Richard"]
biolist = ["I like reading books.", "I'm an author.", "I'm a writer.", "I'm a student.", "I'm studing in university.", "Too many books to read.", "Books are a good way to pass time.", "Not enough time to read every book I wish to."]
reviews = [{"text": "Very good book.", "rating": 5}, {"text": "Not a bad book.", "rating": 3}, {"text": "Wouldn't recommend.", "rating": 1}, {"text": "Best book I've read.", "rating": 5}, {"text": "Worst book I've read.", "rating": 0}, {"text": "Good.", "rating": 4}, {"text": "Bad", "rating": 2}, {"text": "Awesome!", "rating": 5}, {"text": "Author did a great job!", "rating": 5}, {"text": "It was okay.", "rating": 3}, {"text": "Author did a good job.", "rating": 4}, {"text": "Mediocre.", "rating": 2}, {"text": "Meh.", "rating": 2}, {"text": "It was fine.", "rating": 3}, {"text": "Author needs to learn how to write.", "rating": 1}, {"text": "Best book.", "rating": 5}]
books = []

def populate():

	#Uses the books_api.py file to search for books, since it adds them to the database itself we only need to update the page views.
	for x in booklist:
		for y in search_query(x):
			books.append(y)
			add_page_views(y)

	#Calls the add_user function for all users in the list.
	for x in usernames:
		add_user(x)

	#Selects a random book, user and review to pass to the add_review function. 
	for x in range(30, randint(35, 70)):
		add_review(Book.objects.order_by('?').first(), User.objects.order_by('?').first(), choice(reviews))

	#Calls the add_readingList function between 50 and 100 times.
	for x in range(50, randint(55, 100)):
		add_readingList()

#Updates the book's page views.
def add_page_views(book):
	try:
		newbook = Book.objects.get(bookid=book["bookid"])
		newbook.pageViews = randint(0,100)
		newbook.save()
	except:
		return
	print("Added Book: {0.title}".format(newbook))

#Adds the user and then reviews a book which is set as their favourite book along with a bio being added. 
def add_user(username):
	try:
		newuser = User.objects.get_or_create(username=username, email="{}@hotmail.com".format(username), password=(''.join(choice(ascii_uppercase) for i in range(8))))[0]
		book = Book.objects.order_by('?').first()
		pagesread = 0
		if book.pageCount:
			pagesread = book.pageCount
		add_review(book, newuser, choice(reviews))
		favouriteBook = ReadingList.objects.get_or_create(user=newuser, book=book, status=2, pagesread=pagesread)[0]
		UserProfile.objects.get_or_create(user=newuser, bio=choice(biolist), favouriteBook=favouriteBook)[0]
	except:
		return
	print("Added User: {0}".format(username))

#Adds a review for a book and updates the average rating for it.
def add_review(book, user, review):
	try:
		newreview = Review.objects.get_or_create(user=user, book=book, text=review["text"], rating=review["rating"])[0]
		reviews = Review.objects.filter(book_id=book.bookid)
		if len(reviews) != 0:
			average = 0
			for review in reviews:
				average += review.rating
			book.averageRating = round(average/len(reviews))
		else:
			book.averageRating = review["rating"]
		book.save()
	except:
		return
	print("Added Review: {0.book.title} - {0.text}".format(newreview))

#Adds books to users reading lists.
def add_readingList():
	try:
		book = Book.objects.order_by('?').first()
		pagesread = 0
		if book.pageCount:
			pagesread = randint(0, book.pageCount)
		ReadingList.objects.get_or_create(user=User.objects.get(username=choice(usernames)), book=book, status=randint(0,4), pagesread=pagesread)[0]
	except:
		return
	print("Added Reading List Item: {0.title}".format(book))

if __name__ == "__main__":
	print("Starting Bookworm population script...")
	populate()