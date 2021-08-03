from django.db import models
import re
import bcrypt

# Create your models here.
# ----------------------------------------------------------
# UserManager class (for errors and validations)----------->
# ----------------------------------------------------------
class UserManager(models.Manager):
# ----------------------------------------------------------
# registration validator----------->
# ----------------------------------------------------------
    def register_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long!"
            
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long!"
        
        if not EMAIL_REGEX.match(postData['email']):         
            errors['email'] = "Email address invalid! Please enter a valid email address."

        if User.objects.filter(email = postData['email']).exists() and postData['do_what']== "register":
            errors['email'] = "Could not register. The email address you entered already exists."

        if len(postData['password']) < 8:
            errors['password'] = "Invalid password! Password must be at least 8 characters long."

        if postData['password'] != postData['conf_pass']:
            errors['conf_pass'] = "The password and confirm password did not match! Please re-enter the password."

        return errors
    
# ----------------------------------------------------------
# login validator----------->
# ----------------------------------------------------------
    def login_validator(self, postData):
        errors = {}

        user = User.objects.filter(email=postData['login_email'])

        if len(user)<1:
            errors['login_email'] = "Invalid credentials. Please enter valid email!"
        else:
            logged_user = user[0]
            
            if not bcrypt.checkpw(postData['login_pass'].encode(), logged_user.password.encode()):
                errors['login_email'] = "Invalid password. Please enter valid password"
        
        return errors

# ----------------------------------
# User class (users in DB)----------->
# ----------------------------------
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 20)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # posted_messages: messaged posted by user
    # posted_comments: comments posted by user
    
    objects = UserManager()

# ----------------------------------
# Message class (messages in DB)----------->
# ----------------------------------
class Message(models.Model):
    message = models.TextField()
    message_posted_by = models.ForeignKey(User, related_name = 'posted_messages', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # related_comments : Comments related to message

# ----------------------------------
# Comment class (comments in DB)----------->
# ----------------------------------
class Comment(models.Model):
    comment = models.TextField()
    comment_posted_by = models.ForeignKey(User, related_name = "posted_comments", on_delete = models.CASCADE)
    comment_for_message = models.ForeignKey(Message, related_name = "related_comments", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)