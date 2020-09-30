"""djsample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.conf.urls import url
from djsample import views, forms

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',
        LoginView.as_view(template_name="registration/login.html", authentication_form=forms.LoginForm),
        name='login'
    ),
    path('', include('django.contrib.auth.urls')),
    path('', views.Quizzes.as_view(), name='quizzes'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('quiz/create/', views.QuizCreate.as_view(), name='quiz_create'),
    url(r'^quiz/(?P<quiz_id>\d+)/$', views.Quiz.as_view(), name='quiz'),
]
