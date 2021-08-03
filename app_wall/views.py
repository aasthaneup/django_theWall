from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# import datetime
# from datetime import date
# from time import strftime

# Create your views here.
def root(request):
    return render(request, 'logreg.html')

def register(request):

    errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ("/")

    else:
        hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hashpw
        )
        request.session['userid'] = new_user.id

        return redirect('/wall')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ("/")
    else:
        user = User.objects.filter(email = request.POST['login_email'])
        request.session['userid'] = user[0].id
        return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect('/')

def wall(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login before continuing!")
    else:
        logged_user = User.objects.get(id = request.session['userid'])
        context = {
            'logged_user' : logged_user,
            'all_messages' : Message.objects.all().order_by('-updated_at'),
            
        }

        return render(request, 'wall.html', context)

def post_message(request):
    Message.objects.create(
        message = request.POST['postedmsg'],
        message_posted_by = User.objects.get(id = request.session['userid'])
    )
    return redirect('/wall')

def post_comment(request, id):
    Comment.objects.create(
        comment = request.POST['postedcmt'],
        comment_posted_by = User.objects.get(id = request.session['userid']
        ),
        comment_for_message = Message.objects.get(id = id)
    )
    return redirect('/wall')

def delete_post(request, id):
    if 'userid' not in request.session:
        messages.error(request, "Please login before continuing!")
        return redirect('/')
    else:
        Message.objects.get(id = id).delete()
        return redirect('/wall')