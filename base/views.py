from django.shortcuts import render, redirect
from .models import User, Event, Submission
from .forms import SubmissionForm
# Create your views here.

def home_page(request):
    users = User.objects.filter(hackathon_participant=True)
    events = Event.objects.all()
    context = {'users': users, 'events': events}
    return render(request, 'home.html', context)

def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request, 'profile.html', context)

def account_page(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account.html', context)

def event_page(request, pk):
    event = Event.objects.get(id=pk)
    registered = request.user.events.filter(id=event.id).exists()
    submitted = Submission.objects.filter(participant=request.user, event=event).exists()
    context = {'event': event, 'registered': registered, 'submitted': submitted}
    return render(request, 'event.html', context)


def registration_confirmation(request, pk):
    event = Event.objects.get(id=pk)

    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event', pk=event.id)

    return render(request, 'event_confirmation.html', {'event':event})

def project_submission(request, pk):
    event = Event.objects.get(id=pk)

    form = SubmissionForm()

    if request.method == 'POST':
        form = SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()
            return redirect('account')

    context = {'event': event, 'form': form}
    return render(request, 'submit_form.html', context)