from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    role = models.CharField(max_length=10, choices=[
        ('admin', 'Admin'),
        ('exploiter', 'Exploiter')
    ])

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    phone_number = models.CharField(max_length=13)
    addres = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class Exploiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='exploiter_profile')
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return self.user.username

class Country(models.Model):
    name = models.CharField(max_length=100)
    flag_image = models.ImageField(upload_to="flags/", null=True, blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="actors/", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Film(models.Model):
    name = models.CharField(max_length=150)
    views = models.PositiveIntegerField(default=0)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='films', blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, related_name='films')
    actors = models.ManyToManyField(Actor, related_name='films', blank=True)
    countries = models.ManyToManyField(Country, related_name='films', blank=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.film.name}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 rating
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film')

    def __str__(self):
        return f"{self.user.username} - {self.film.name}: {self.score}"