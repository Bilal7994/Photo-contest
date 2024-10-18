from django.contrib.auth.models import User
from django.db import models

class Contest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User model
    Cname = models.CharField(max_length=100)  # Contest name
    Cdate = models.DateField()  # Contest date
    Cdescription = models.CharField(max_length=200)  # Contest description

    def __str__(self):
        return self.Cname


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    upload_date = models.DateTimeField(auto_now_add=True)
    likes_count = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return f"Photo by {self.user.username} for {self.contest.Cname}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who liked the photo
    photo = models.ForeignKey(Photo, related_name='likes', on_delete=models.CASCADE)  # Photo being liked
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'photo')  # Prevent a user from liking the same photo multiple times

    def __str__(self):
        return f"{self.user.username} liked Photo {self.photo.id}"