from django.db import models
from django.contrib.auth.models import User

#Model for user profile.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	bio = models.CharField(max_length=2000, blank=True)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __str__(self):
		return self.user.username
