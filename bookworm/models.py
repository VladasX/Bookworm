from django.db import models
from django.contrib.auth.models import User

#Model for user profile.
class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	bio = models.CharField(max_length=2000, blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)
	favouriteBook = models.ForeignKey(Book, blank=true)

	def __str__(self):
		return self.user.username

#Model for books stored.
class Book(models.Model):
	bookid = models.CharField(primary_key=True, max_length=256) #Uses the Google page ID instead of the ISBN since not all results via the API seem to return an ISBN.
	title = models.CharField(max_length=256, null=True)
	authors = models.CharField(max_length=128, null=True)
	publisher = models.CharField(max_length=256, null=True)
	publishedDate = models.CharField(max_length=256, null=True)
	description = models.TextField(max_length=4096, null=True)
	isbn = models.CharField(max_length=40, null=True)
	averageRating = models.FloatField(max_length=2) #We'll use our own ratings instead of Google Book's.
	thumbnail = models.URLField(max_length=2000, null=True)
	textSnippet = models.TextField(max_length=2000, null=True)
	pageViews = models.IntegerField()

#Model for reviews stored.
class Review(models.Model):
	user = models.ForeignKey(User)
	book = models.ForeignKey(Book)
	text = models.TextField(max_length=4096, null=True)
	timestamp = models.DateTimeField(auto_now=True)
