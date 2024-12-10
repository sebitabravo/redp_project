from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Experience(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Culinary Discovery'),
        ('milestone', 'Personal Milestone'),
        ('culture', 'Cultural Recommendation'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    additional_info = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"


class Comment(models.Model):
    experience = models.ForeignKey(
        Experience, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.name} on {self.experience.title}"


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    experience = models.ForeignKey(
        Experience, on_delete=models.CASCADE, related_name='favorited_by')

    def __str__(self):
        return f"{self.user.name} -> {self.experience.title}"
