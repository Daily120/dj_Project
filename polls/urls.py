from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', login_required(views.IndexView.as_view()), name='index'),
    # ex: /polls/5/
    path('posts/<int:pk>/', login_required(views.DetailView.as_view()), name='detail'),
    # ex: /polls/5/results/
    path('posts/<int:pk>/results/', login_required(views.ResultsView.as_view()), name='results'),
    # ex: /polls/5/vote/
    path('posts/<int:question_id>/vote/', login_required(views.vote), name='vote'),
    path('reg/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add_comment/', login_required(views.add_comment), name='add_comment'),
    path('new_post/', login_required(views.new_post), name='new_post'),
]
