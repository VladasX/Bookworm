from django.db import models
from django.contrib.auth.models import User

#Model for user profile.
class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	bio = models.CharField(max_length=2000, blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username

#Model for books stored.
class Book(models.Model):
	title = models.CharField(max_length=256),
	author = models.CharField(max_length=128),
	publisher = models.CharField(max_length=256),
	publishedDate = models.CharField(max_length=256),
	thumbnail = models.URLField(max_length=2000)
	description = models.TextField(max_length=4096, blank=True),
	linkid = models.CharField(primary_key=True, max_length=256), #Uses the Google page ID instead of the ISBN since not all results via the API seem to return an ISBN.
	averageRating = models.FloatField(max_length=5)

	def __str__(self):
		return self.title, self.author, self.publisher, self.publishedDate, self.description, self.linkid, self.averageRating

#Model for reviews stored.
class Review(models.Model):
	book = models.ForeignKey(Book),
	user = models.ForeignKey(UserProfile),
	date = models.DateField(auto_now_add=True),
	text = models.TextField(max_length=4096)
