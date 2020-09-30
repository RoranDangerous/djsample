import json
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from djsample import models, forms
from djsample.mixins import IsTeacherMixin


class SignUpView(generic.CreateView):
    form_class = forms.SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Quizzes(LoginRequiredMixin, generic.TemplateView):
  template_name = 'pages/quizzes.html'

  def get_context_data(self, **kwargs):
    return {
      **super(generic.TemplateView, self).get_context_data(**kwargs),
      'quizzes': models.Quiz.objects.all()
    }


class Quiz(LoginRequiredMixin, generic.View):
  template_name = 'pages/quiz.html'

  def get(self,request, *args, **kwargs):
    return render(request, 'pages/quiz.html', {"quiz": models.Quiz.objects.get(id=kwargs.get("quiz_id"))})

  def post(self, request, *args, **kwargs):
    questions = models.Quiz.objects.get(id=kwargs.get("quiz_id")).questions.all()

    for question in questions:
      student_answer, _ = models.StudentAnswer.objects.update_or_create(
        question=question,
        student=request.user,
        defaults={
          'short_answer': request.POST.get(f'answer_{question.id}') if not question.is_multiple_choice else None
        }
      )

      if question.is_multiple_choice:
        student_answer.mc_answers.clear()
        for option in question.options.all():
          if request.POST.get(f'answer_{question.id}_{option.id}'):
            student_answer.mc_answers.add(option)

    return redirect('quizzes')


class QuizCreate(LoginRequiredMixin, IsTeacherMixin, generic.View):
  def get(self, request, *args, **kwargs):
    return render(request, 'pages/create_quiz.html')

  def post(self, request, *args, **kwargs):
    questions = json.loads(request.POST.get("questions"))

    quiz = models.Quiz.objects.create()

    for question in questions:
      is_multiple_choice = question.get('multiple_choice', False)
      question_instance = models.Question.objects.create(
        quiz=quiz,
        text=question.get('question', ''),
        is_multiple_choice=is_multiple_choice,
        short_answer=question.get('answer') if not is_multiple_choice else None
      )

      if is_multiple_choice:
        for answer in question.get('answer', []):
          models.MultipleChoice.objects.create(
            question=question_instance,
            text=answer.get('option', ''),
            is_correct=answer.get('is_correct', False)
          )

    return HttpResponse('success')