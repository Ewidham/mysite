from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'polls'

urlpatterns = [
    path('register', views.register, name = 'register'),
    #url(r'^register/$', views.register, name='register'),
    path('', views.IndexView.as_view(), name = 'index'),
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),
    path('<int:pk>/results', views.ResultsView.as_view(), name = 'results'),
    path('<int:question_id>/vote', views.vote, name = 'vote'),
    path('<int:question_id>/add_choice', views.add_choice, name = 'add_choice'),
]