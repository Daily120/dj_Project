from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


def home(request):
    if request.session.get('login_check'):
        return redirect('/posts')
    else:
        return render(request, 'polls/home.html')


class IndexView(generic.ListView):
    template_name = 'polls/posts.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
            Question.objects.filter(pub_date__lte=timezone.now())
            returns a queryset containing Questions whose pub_date is less than or equal to - that is, earlier than or equal to - timezone.now.
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')  # [:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/post_details.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/post_details.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            request.session['login_check'] = True
            request.session['username'] = user.username
            return redirect('/posts')
    else:
        form = UserCreationForm()
    return render(request, 'polls/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['login_check'] = True
            request.session['username'] = user.username
            return redirect('/posts')
    else:
        form = AuthenticationForm()
    return render(request, 'polls/login.html', {'form': form})


def logout(request):
    # Deletes the current session data from the session and deletes the session cookie
    request.session.flush()
    return redirect('/')


def add_comment(request):
    question = Question.objects.get(pk=request.POST['qPK'])
    question.comments_set.create(comment_text=request.POST['comment'],
                                 comment_author=request.session.get('username'), pub_date=timezone.now())
    question.save()

    return redirect('/posts/' + request.POST['qPK'] + '/')


def new_post(request):
    if request.method == "POST":
        question = Question()
        question.author = request.session.get('username')
        question.pub_date = timezone.now()
        question.save()
        question.question_text = request.POST['question_post']
        question.choice_set.create(choice_text=request.POST['choice1'])
        question.choice_set.create(choice_text=request.POST['choice2'])
        question.choice_set.create(choice_text=request.POST['choice3'])
        question.save()
        return redirect('/posts', pk=question.pk)
    return render(request, 'polls/new_post.html')
