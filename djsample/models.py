from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  is_teacher = models.BooleanField(default=False)


class Quiz(models.Model):
  pass


class Question(models.Model):
  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
  text = models.CharField(max_length=256, blank=False, null=False)
  is_multiple_choice = models.BooleanField(default=False)
  short_answer = models.CharField(max_length=256, blank=True, null=True)


class MultipleChoice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
  text = models.CharField(max_length=256, null=False, blank=False)
  is_correct = models.BooleanField(default=False)


class StudentAnswer(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='student_answers')
  student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
  short_answer = models.CharField(max_length=256, blank=True, null=True)
  mc_answers = models.ManyToManyField(MultipleChoice, related_name='answers')