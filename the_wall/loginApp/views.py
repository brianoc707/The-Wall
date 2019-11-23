from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt


# Create your views here.
def home(request):
	return render(request, 'index.html')

def signUp(request):
	print("*****")
	print(request.POST)
	print("*****")
	resultFromValidator = User.objects.validateUser(request.POST)
	if len(resultFromValidator) > 0:
		for key, value in resultFromValidator.items():
			messages.error(request, value)
		return redirect('/')
	else:
		passwordFromForm = request.POST['pw']
		print(passwordFromForm)
		hash1 = bcrypt.hashpw(passwordFromForm.encode(), bcrypt.gensalt())
		print(hash1)
		newUser = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], password = hash1.decode())
		print(newUser)
		request.session['email']= newUser.email
		return redirect('/wall')

def login(request):
	
	print(request.POST)
	email = request.POST['email']
	user = User.objects.get(email = email)
	print(user.password)
	

	
	errors = User.objects.loginValidator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		request.session['email'] = email
		return redirect('/wall')




def wall(request):
	loggedInUser = User.objects.get(email = request.session['email'])
	messages = Message.objects.all()
	
	context = {
		'currentUser' : loggedInUser,
		'messages' : messages,
		
	}
	
	return render(request, 'wall.html', context)

def message(request):
	loggedInUser = User.objects.get(email = request.session['email'])
	newMessage = Message.objects.create(poster = loggedInUser, message = request.POST['message'])

	return redirect('/wall')

def comment(request, messageid):
	loggedInUser = User.objects.get(email = request.session['email'])
	message = Message.objects.get(id= messageid)
	newComment = Comment.objects.create(commenter = loggedInUser, comment = request.POST['comment'], message = message)
	
	return redirect('/wall')

def delete(request, messageid):
	
	messagetoDelete = Message.objects.get(id = messageid)
	messagetoDelete.delete()
	return redirect('/wall')

def logout(request):
	request.session.clear()
	return redirect('/')
	
