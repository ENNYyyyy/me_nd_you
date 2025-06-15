
# Create your models here.
from django.db import models

# Each couple shares a secret word (like a room code)
class CoupleSession(models.Model):
    secret_word = models.CharField(max_length=100, unique=True)
    partner1_name = models.CharField(max_length=50)
    partner2_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.partner1_name} & {self.partner2_name}"

# Admin-added questions
class Question(models.Model):
    MODES = [
        ('questions', 'Questions'),
        ('truth', 'Truth or Dare'),
        ('challenge', 'Challenge'),
        ('spicy', 'Spicy Only'),
        ('mixed', 'Mixed Mode'),
        ('would', 'Would You Rather'),
    ]
    text = models.TextField()
    mode = models.CharField(max_length=20, choices=MODES)

    def __str__(self):
        return f"[{self.mode}] {self.text[:50]}"

# Couple-created questions
class CustomQuestion(models.Model):
    couple = models.ForeignKey(CoupleSession, on_delete=models.CASCADE)
    text = models.TextField()
    mode = models.CharField(max_length=20, choices=Question.MODES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Custom by {self.couple.secret_word}: {self.text[:50]}"

class PlayedQuestion(models.Model):
    couple = models.ForeignKey(CoupleSession, on_delete=models.CASCADE)
    text = models.TextField()
    mode = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
