from django import template
from django.db.models.functions import Cast, Coalesce, Least
from django.db.models import Count, Case, When, IntegerField, F, Sum, FloatField, Sum, Q, BooleanField, Min, Value
from djsample.models import StudentAnswer

register = template.Library()


@register.filter(name='get_color')
def get_color(grade):
  if grade is None:
    return 'none'
  elif grade >= 90:
    return '#06ff0640'
  elif grade >= 80:
    return '#6dff093d'
  elif grade >= 70:
    return '#ffa50057'
  elif grade >= 60:
    return '#ffa5005e'
  else:
    return '#ff00002e'


@register.filter(name='get_score')
def get_score(user, quiz):
  '''
    Simple (even if doesn't seem to be so) query to calculate total score for the quiz.
    Following logic is applied:

    Correct Short Answer question = 1 point.
    Selecting correct Multiple Choice option = 1 / total number of options for the question.
    Not selecting invalid Multiple Choice options = 1 / total number of options for the question.
  '''
  answers = StudentAnswer.objects.filter(student=user, question__quiz=quiz)

  if not answers.exists():
    return None

  score = answers.annotate(
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
      Coalesce(Sum(Case(
        When(~Q(short_answer_score=None), then=F('short_answer_score')),
        output_field=FloatField()
      )), 0)
      # Add calculated Multiple Choice score
      + Coalesce(
        Sum(Case(
          When(~Q(multiple_choice_score=None), then=F('multiple_choice_score')),
          output_field=FloatField()
        )) / Cast(Count(Case(
          When(~Q(multiple_choice_score=None), then=1.0),
          output_field=FloatField()
        )), FloatField()), 0
      )
    )
    # Divide by the total number of Short Answers + (1 if Multiple Choice exist)
    / (
      Cast(Count(Case(
        When(~Q(short_answer_score=None), then=1.0),
        output_field=FloatField()
      )), FloatField())
      + Cast(Least(Count(Case(
        When(~Q(multiple_choice_score=None), then=1.0),
        output_field=FloatField()
      )), 1.0), FloatField())
    )
  ).get('total')
  return score and round(score * 100, 2)