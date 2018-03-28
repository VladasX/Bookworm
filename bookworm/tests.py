from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
from django.conf import settings
from bookworm.models import Book, Review, ReadingList, User, UserProfile
from test_utils import create_test_book, create_test_review, create_test_user

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
		self.assertIn(b'img src="/static/images/logo.png"', response.content)

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
		# Creates a test book
		test_book = create_test_book()
		
		# Checks if the book appears in main page
		response = self.client.get(reverse('index'))
		self.assertTrue(len(response.context['highest_rated']) > 0)
		self.assertTrue(len(response.context['most_viewed']) > 0)
		# Test book is named Tango with Django just for testing purposes
		self.assertIn(b'Tango with Django', response.content)
		
		# Creates a test user
		test_user = create_test_user("Vlad")
		
		# Creates a test review
		test_review = create_test_review(test_user, test_book, "It was a pleasure reading this book and helped me a lot for a Web App Development course I took")
		
		# Checks if a review appears in main page
		response = self.client.get(reverse('index'))
		self.assertTrue(len(response.context['recent_reviewed']) > 0)
		# Review's author should be displayed
		self.assertIn(b'Vlad', response.content)
		# Checks if at least a portion of review's text is shown
		self.assertIn(b'Web App Development course', response.content)
		
class BooksListPageTests(TestCase):
	def test_no_books_in_database(self):
		# Checks that a message is shown when there are no books in the database
		response = self.client.get(reverse('book_list', kwargs={'pages':1}))   
		self.assertIn(b'No books have been added yet, please search for books to populate this list.', response.content)
		
	def test_books_shown(self):
		# Creates a test book
		test_book = create_test_book()
		# Checks that books list shows a test book
		response = self.client.get(reverse('book_list', kwargs={'pages':1}))
		self.assertTrue(len(response.context['books']) > 0)
		self.assertIn(b'Tango with Django', response.content)
		
class ProfilePageTests(TestCase):
	def test_profile_no_avatar(self):
		# Creates a test user
		test_user = create_test_user("Vlad")
		
		# Checks that a default avatar is shown when a user has not set an avatar yet
		response = self.client.get(reverse('profile', kwargs={'username':test_user.username}))
		self.assertIn(b'img src="/static/images/default_avatar.png"', response.content)
		
	def test_profile_favourite_book(self):
		# Creates a test user
		test_user = create_test_user("Vlad")
		# Creates a test book
		test_book = create_test_book()
		
		# Sets test user's favourite book		
		userprofile = UserProfile.objects.get_or_create(user=test_user)[0]
		userprofile.favouriteBook = test_book.bookid
		userprofile.save()
		
		# Checks that a favourite book is displayed on profile page if it is set
		response = self.client.get(reverse('profile', kwargs={'username':test_user.username}))
		self.assertIn(b'src="https://s3.amazonaws.com/titlepages.leanpub.com/tangowithdjango19/hero?1518073904"', response.content)
		
class ReadingListTests(TestCase):
	def test_empty_reading_list(self):
		# Creates a test user
		test_user = create_test_user("Vlad")
		
		# Checks that a default avatar is shown when a user has not set an avatar yet
		response = self.client.get(reverse('reading_list', kwargs={'username':test_user.username}))
		self.assertIn(b'You currently don\'t have any books in your reading list', response.content)

	def test_filled_reading_list(self):
		# Creates a test user
		test_user = create_test_user("Vlad")
		# Creates a test book
		test_book = create_test_book()		
		
		# Sets test book in user's reading list
		test_reading_list = ReadingList()
		test_reading_list.user = test_user
		test_reading_list.book = test_book
		test_reading_list.save()
		
		# Checks that a reading list shows books when they are added
		response = self.client.get(reverse('reading_list', kwargs={'username':test_user.username}))
		self.assertTrue(len(response.context['reading_data']) > 0)
		# Test book is called Tango with Django
		self.assertIn(b'Tango with Django', response.content)

class PopulationScriptTests(TestCase): 
	def test_populate(self):
		try:
			from population_script import populate
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
		