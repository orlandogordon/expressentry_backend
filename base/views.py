from django.shortcuts import render, redirect
from .models import User, Event, Submission
from .forms import SubmissionForm, CustomUserCreateForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages

from datetime import datetime
# Create your views here.

def login_page(request):
    page='login'
    messages.info(request, 'Test Credentials: Email: test@example.com, Password: 1234pass')


    if request.method == "POST":
        user = authenticate(
            email=request.POST['email'], 
            password=request.POST['password']
            )
        
        if user is not None:
            login(request, user)
            messages.info(request, 'User succesfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Email OR Password is incorrect')
            return redirect('login')
        

    context = {'page': page}
    return render(request, 'login_register.html', context)

def register_page(request):
    messages.info(request, 'Test Credentials: Email: test@example.com, Password: 1234pass')
    form = CustomUserCreateForm()
    if request.user.is_authenticated:
        return redirect('hackathons')
    if request.method == 'POST':
        form = CustomUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, 'User account created succesfully.')
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')

    page='register'
    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    messages.info(request, 'User succesfully logged out.')
    return redirect('login')

def home_page(request):

    users = User.objects.filter(hackathon_participant=True)
    count = users.count()

    page= request.GET.get('page')
    paginator = Paginator(users, 5)

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        users = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        users = paginator.page(page)

    pages = list(range(1, (paginator.num_pages + 1)))

    events = Event.objects.all()
    context = {'users': users, 'events': events, 'count': count, 'paginator': paginator, 'pages': pages}
    return render(request, 'home.html', context)

def hackathons_page(request):
    events = Event.objects.filter(event_type='hackathon')
    active_events = []
    past_events = []
    present = datetime.now().timestamp()
    for event in events:
        deadline = event.registration_deadline.timestamp()
        past_deadline = (present > deadline)
        if past_deadline:
            past_events.append(event)
        else:
            active_events.append(event)

    context = {'active_events': active_events, 'past_events': past_events}
    return render(request, 'hackathons.html', context)

def seminars_page(request):
    events = Event.objects.filter(event_type='seminar')
    active_events = []
    past_events = []
    present = datetime.now().timestamp()
    for event in events:
        deadline = event.registration_deadline.timestamp()
        past_deadline = (present > deadline)
        if past_deadline:
            past_events.append(event)
        else:
            active_events.append(event)

    context = {'active_events': active_events, 'past_events': past_events}
    return render(request, 'seminars.html', context)

def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user':user}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def account_page(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account.html', context)

@login_required(login_url='login')
def edit_account(request):
    form = UserForm(instance=request.user)

    if request.method == 'POST':
        if 'avatar' in request.FILES:
            request.FILES['avatar'].name = f"{request.user.id}.jpg"
        form = UserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form}
    return render(request, 'user_form.html', context)

@login_required(login_url='login')
def change_password(request):
    if str(request.user.id) == '268f17e4-4f5a-4ac3-96ea-64678db81012':
        messages.error(request, 'Password reset of the test account is not allowed.')
        return redirect('account')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            new_pass = make_password(password1)
            request.user.password = new_pass
            request.user.save()
            messages.success(request, 'Password succesfully reset.')
            return redirect('account')
        
        else:
            messages.error(request, 'Passwords do not match ')
            return redirect('change-password')


    return render(request, 'change_password.html')

def event_page(request, pk):
    event = Event.objects.get(id=pk)
    present = datetime.now().timestamp()
    deadline = event.registration_deadline.timestamp()
    past_deadline = (present > deadline)


    registered = False
    submitted = False
    isHackathon = event.event_type == 'hackathon'
    if request.user.is_authenticated:
        authenticated = True
        registered = request.user.events.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()
    else:
        authenticated = False

    context = {'event': event, 'past_deadline': past_deadline, 'authenticated': authenticated, 'registered': registered, 'submitted': submitted, 'isHackathon': isHackathon}
    return render(request, 'event.html', context)

@login_required()
def registration_confirmation(request, pk):
    event = Event.objects.get(id=pk)

    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event', pk=event.id)

    return render(request, 'event_confirmation.html', {'event':event})

@login_required()
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

@login_required()
def update_submission(request, pk):
    submission = Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse('You can\'t be here')

    event = submission.event
    form = SubmissionForm(instance=submission)

    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'event': event, 'form': form}
    return render(request, 'submit_form.html', context)