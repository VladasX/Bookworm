from bookworm.models import Book, Review, User

# Helper functions
def create_test_book():
	test_book = Book()
	test_book.bookid = "giVeMeanA1plz"
	test_book.title = "Tango with Django"
	test_book.authors = "David Maxwell, Leif Azzopardi"
	test_book.publisher = "Leanpub"
	test_book.publishedDate = "2018-02-06"
	test_book.description = "Tango With Django is a begginner's guide to Web Development using the popular Python Based Web Framework Django. The book provides a hands-on guide to designing and building web applications, explaining how all the technology fits together as you build Rango and then deploying the application on PythonAnywhere. Through the course of the book, you will not only learn how to Tango with Django, but also learn about Javascript/Jquery, CSS/Bootstrap and HTML, PIP and Git/GitHub."
	test_book.isbn = "B01N91N65Y"
	test_book.averageRating = 5.0
	test_book.thumbnail = "https://s3.amazonaws.com/titlepages.leanpub.com/tangowithdjango19/hero?1518073904"
	test_book.textSnippet = None
	test_book.pageCount = 293
	test_book.pageViews = 9001
	test_book.save()
	return test_book
	
def create_test_review(user, book, review):
	test_review = Review()
	test_review.user = user
	test_review.book = book
	test_review.text = review
	test_review.rating = 5
	test_review.save()
	return test_review
	
def create_test_user(name):
	test_user = User.objects.get_or_create(username=name, password="FrenchFries", email="2262803m@student.gla.ac.uk")[0]
	test_user.save()
	return test_user