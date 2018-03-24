from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
from django.conf import settings
from bookworm.models import Book, Review
from bookworm.models import User, UserProfile

import os

class GeneralTests(TestCase):
    def test_serving_static_files(self):
        # If static media is used properly 
        # result is not NONE once it finds logo.png
        result = finders.find('images/logo.png')
        self.assertIsNotNone(result)
        
    def test_base_template_exists(self):
        # Check base.html exists inside template folder
        path_to_base = settings.TEMPLATE_DIR + '/bookworm/base.html'
        self.assertTrue(os.path.isfile(path_to_base))
        
    def test_logo_exists(self):
        # Check that logo exists
        path_to_logo = settings.STATIC_DIR + '/images/logo.png'
        self.assertTrue(os.path.isfile(path_to_logo))

        
class IndexPageTests(TestCase):
    def test_logo_exists(self):
        # Check that logo is displayed in main page
        response = self.client.get(reverse('index'))
        self.assertIn(b'img src="/static/images/logo.png', response.content)

    def test_index_using_template(self):
        # Check that index uses a template
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'bookworm/index.html')
        
    def test_index_using_base_template(self):
        # Check that base template is also used
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'bookworm/base.html')
        
    def test_index_does_not_contain_books_message(self):
        # Returns a message if there are no books present
        response = self.client.get(reverse('index'))
        self.assertIn(b'There are currently no books in the database', response.content)
    
    def test_index_does_not_contain_reviews_message(self):
        # Returns a message if there are no books present
        response = self.client.get(reverse('index'))
        self.assertIn(b'There are currently no reviews', response.content)
        
    def test_index_shows_books_and_reviews(self):
        test_book = Book()
        test_book.bookid = "giVeMeanA1plz"
        test_book.title = "Tango with Django"
        test_book.authors = "David Maxwell, Leif Azzopardi"
        test_book.publisher = "Leanpub"
        test_book.publishedDate = "2018-02-06"
        test_book.description = "Tango With Django is a begginner's guide to Web Development using the popular Python Based Web Framework Django. The book provides a hands-on guide to designing and building web applications, explaining how all the technology fits together as you build Rango and then deploying the application on PythonAnywhere. Through the course of the book, you will not only learn how to Tango with Django, but also learn about Javascript/Jquery, CSS/Bootstrap and HTML, PIP and Git/GitHub."
        test_book.isbn = "B01N91N65Y"
        test_book.averageRating = 5.0
        test_book.thumbnail = "https://www.googleapis.com/books/v1/volumes?q=django"
        test_book.textSnippet = None
        test_book.pageCount = 293
        test_book.pageViews = 9001
        test_book.save()
        
        # Checks if the book appears in main page
        response = self.client.get(reverse('index'))
        self.assertIn(b'Tango with Django', response.content)
        
        test_user = User.objects.get_or_create(username="Vlad", password="FrenchFries", email="2262803m@student.gla.ac.uk")[0]
        test_user.save()

        
        test_review = Review()
        test_review.user = test_user
        test_review.book = test_book
        test_review.text = "It was a pleasure reading this book and helped me a lot for a Web App Development course I took"
        test_review.rating = 5
        test_review.save()
        
        # Checks if a review appears in main page
        response = self.client.get(reverse('index'))
        self.assertIn(b'Vlad', response.content)
        self.assertIn(b'Web App Development', response.content)

class PopulationScriptTests(TestCase): 
    def test_populate(self):
        try:
            from populate import populate
            populate()
        except ImportError:
            print('The populate script does not exist')
        except NameError:
            print('The function populate() does not exist')
        except:
            print('Something went wrong in the populate() function :(')
          
        # Check that books were created
        books = Book.objects.all()
        self.assertEqual((len(books) > 0), True)
        
        # Check that reviews were created
        reviews = Review.objects.all()
        self.assertEqual((len(reviews) > 0), True)
        
        # Check that reviews are not empty
        self.assertEqual((len(reviews[0].text) > 0), True)
        