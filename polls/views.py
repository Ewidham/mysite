from django.shortcuts import render, get_object_or_404, redirect
from django.http import  HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Vote

from .models import Question, Choice
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/polls')
        return HttpResponse("User creation failed!")
    else:
        form = UserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        )

class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    choices = question.choice_set.all()
    user_voted = 0

    for choice in choices:
        for vote in choice.vote_set.all():
            if (vote.voter.id == request.user.id):
                user_voted += 1

    try:
        selected_choice = choices.get(pk = request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{'question':question, 'error_message':'You did not select a choice.'})
    else:
        if (user_voted >= question.nr_of_votes):
            return render(request, 'polls/detail.html', {'question':question, 'error_message':'You have already voted for this question %s times' % question.nr_of_votes})
        if (selected_choice.vote_set.filter(voter__id=request.user.id).count() > 0):
             return render(request, 'polls/detail.html', {'question':question, 'error_message':'You have already voted for the selected option.'})
        Vote.objects.create(choice=selected_choice, voter = request.user)

        return HttpResponseRedirect(reverse('polls:results', args = (question.id,)))

@login_required
def add_choice(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        choice_text_to_add = request.POST['add_choice']
    except (KeyError):
        return render(request, 'polls/detail.html', {'question': question, 'error_message':'You tried to add an empty choice.'})
    else:
        Choice.objects.create(question = question, choice_text = choice_text_to_add)

    return render(request, 'polls/detail.html', {'question': question, 'error_message':'You tried to add an empty choice.'})