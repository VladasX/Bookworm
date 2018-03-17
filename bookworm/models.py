from django.db import models
from django.contrib.auth.models import User

#Model for user profile.
class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	bio = models.CharField(max_length=2000, blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username


class Book(models.Model):
	title = models.CharField(max_length=256),
	author = models.CharField(max_length=128),
	publisher = models.CharField(max_length=2000),
	publishedDate = models.CharField(max_length=2000),
	description = models.TextField(max_length=4096, blank=True),
	isbn = models.Integer(ForeignKey=True),
	averageRating = models.FloatField(max_length=2000),

	def __str__(self):
		return self.title, self.author, self.publisher， self.publishedDate, self.description, self.isbn, self.averageRating


class Review(models.Model):
	comment = models.ForeignKey(Book),
	date = models.dateTimeField(auto_now=False, auto_add=False),
	user = models.ForeignKey(UserProfile),
	text = models.TextField(max_length=2000),

#class BookList(models.Model):
