from django import template
from django.db.models.functions import Cast
from django.db.models import Count, Case, When, IntegerField, F, Sum, FloatField, Sum, Q, BooleanField
from djsample.models import StudentAnswer

register = template.Library()

@register.filter(name='is_completed')
def is_completed(user, quiz):
  return StudentAnswer.objects.filter(student=user, question__quiz=quiz).exists()

@register.filter(name='get_score')
def get_score(user, quiz):
  '''
    Simple (even if doesn't seem to be so) query to calculate total score for the quiz.
    Following logic is applied:

    Correct Short Answer question = 1 point.
    Selecting correct Multiple Choice option = 1 / total number of options for the question.
    Not selecting invalid Multiple Choice options = 1 / total number of options for the question.
  '''
  score = StudentAnswer.objects.filter(
    student=user,
    question__quiz=quiz
  ).annotate(
    multiple_choice_score=Case(
      When(Q(question__options__answers=None) & Q(question__options__is_correct=False), then=1),
      When(~Q(question__options__answers=None) & Q(question__options__is_correct=False), then=0),
      When(~Q(question__options__answers=None) & Q(question__options__is_correct=True), then=1),
      When(Q(question__options__answers=None) & Q(question__options__is_correct=True), then=0),
      default=None,
      output_field=IntegerField()
    ),
    short_answer_score=Case(
      When(short_answer__iexact=F('question__short_answer'), then=1),
      When(~Q(short_answer=None), then=0),
      default=None,
      output_field=IntegerField()
    )
  ).aggregate(
    # Get sum of the Short Answer scores
    total=(
      Sum(Case(
        When(~Q(short_answer_score=None), then=F('short_answer_score')),
        output_field=FloatField()
      ))
      # Add calculated Multiple Choice score
      + (
        Sum(Case(
          When(~Q(multiple_choice_score=None), then=F('multiple_choice_score')),
          output_field=FloatField()
        )) / Cast(Count(Case(
          When(~Q(multiple_choice_score=None), then=1.0),
          output_field=FloatField()
        )), FloatField())
      )
    )
    # Divide by the total number of Short Answers + 1
    / (
      Cast(Count(Case(
        When(~Q(short_answer_score=None), then=1.0),
        output_field=FloatField()
      )), FloatField())
      + 1.0
    )
  ).get('total')
  return f'{round(score * 100, 2)}%'