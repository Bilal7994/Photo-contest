from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Contest,Photo,Like
from django.utils import timezone
import pytz
from django.db.models import Max

# from .forms import SignUpForm

# Create your views here.
def home(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')
def contest(request):
    obj=Contest.objects.all()
    return render(request,'contest.html',{'x':obj})


def first(request):
    return render(request,'first.html')

def login_page(request):
    return render(request,'login.html')

def signup_page(request):
    return render(request,'signup.html')

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def login_save(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password3']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')  # Use redirect to the home view
        else:
            errors = {}
            errors['invalid']='invalid username or passsword'
            return render(request, 'login.html',{'errors':errors,})
    else:
        return redirect('index')
        
 
def signup_save(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        errors = {}

        # Check if passwords match
        if password != confirm_password:
            errors['password_mismatch'] = 'Passwords do not match'

        # Check if email is already taken
        if User.objects.filter(email=email).exists():
            errors['email_taken'] = 'Email is already taken'

        # Check if username is already taken
        if User.objects.filter(username=username).exists():
            errors['username_taken'] = 'Username is already taken'

        # If no errors, create the user
        if not errors:
            user = User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password)
            )
            user.save()

            # Redirect to the login page after successful signup
            return redirect('login')

        # If there are errors, render the signup page again with error messages
        return render(request, 'signup.html', {'errors': errors})
    
    return render(request, 'signup.html')

       
       
def create_contest(request):
    return render(request,"create_contest.html")

def add_contest(request):
    if request.method == 'POST':
        obj=Contest()
        obj.user = request.user
        obj.Cname = request.POST.get('cname')
        obj.Cdescription = request.POST.get('cdescription')
        obj.Cdate = request.POST.get('cdate')
        obj.save()
        return redirect('contest')
    return create_contest(request)

def contest_details(request, contest_id):
    contest = get_object_or_404(Contest, id=contest_id)
    photos = Photo.objects.filter(contest=contest)

    # Convert to the local timezone (Asia/Kolkata)
    local_timezone = pytz.timezone('Asia/Kolkata')
    current_time = timezone.now().astimezone(local_timezone)
    
    # Now you can safely compare the date
    expired = contest.Cdate < current_time.date()


    liked_photos = set()
    if request.user.is_authenticated:
        liked_photos = set(Like.objects.filter(user=request.user, photo__in=photos).values_list('photo_id', flat=True))

    if request.method == 'POST' and request.FILES.get('photo') and not expired:
        # Create and save the photo
        photo = Photo()
        photo.user = request.user
        photo.contest = contest
        photo.image = request.FILES['photo']
        photo.save()

        return redirect('post_contest', contest_id=contest.id)

    context = {
        'contest': contest,
        'photos': photos,
        'expired': expired,
        'liked_photos': liked_photos,
    }
    return render(request, 'post_contest.html', context)



def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    user = request.user

    # Check if the user has already liked the photo
    like, created = Like.objects.get_or_create(user=user, photo=photo)

    if not created:
        # If the like already exists, remove it (unlike)
        like.delete()
        # Ensure the like count does not go below zero
        if photo.likes_count > 0:
            photo.likes_count -= 1
    else:
        # If the like didn't exist, it's a new like
        like.save()
        photo.likes_count += 1

    # Save the updated photo with the new like count
    photo.save()

    # Redirect back to the contest details page after the like/unlike action
    return redirect('post_contest', contest_id=photo.contest.id)


def show_winner(request, contest_id):
    # Get the maximum likes count for the contest
    max_likes = Photo.objects.filter(contest_id=contest_id).aggregate(Max('likes_count'))['likes_count__max']
    
    # Get all photos with that maximum likes count
    winner_photos = Photo.objects.filter(contest_id=contest_id, likes_count=max_likes)
    
    context = {
        'winner_photos': winner_photos,
        'max_likes': max_likes
    }
    
    return render(request, 'winner.html', context)



def logout_view(request):
    logout(request)
    return first(request)