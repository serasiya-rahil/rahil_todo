from app.forms import TODOForm #imported
from app.models import TODO # imported
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #imported
from django.contrib.auth import authenticate, login as loginUser, logout #imported
from django.contrib.auth.decorators import login_required #imported
from app.log import setup_logger as log, log_function_name



#setup log function to keep application tracking
logger = log("./logs/app.log")

@login_required(login_url='login')
def home(request):
    
    if(request.user.is_authenticated): 
       
     

        user = request.user
        todos = TODO.objects.filter(user = user).order_by('-status')

        pending_count = TODO.objects.filter(user=user, status__in=['Pending', 'In Progress']).count()

        Complete_count = TODO.objects.filter(user = user, status='Completed').count()
        Total_count = TODO.objects.filter(user = user).count()
        if(Total_count or Complete_count):

            percentage = (Complete_count / Total_count) * 100
            percentage = round(percentage,2)
        else:
            percentage=0

        form = TODOForm()

        context ={ 'form': form,
                 'todos': todos ,
                 'pending_count': pending_count,
                 'Complete_count': Complete_count,
                 'percentage':percentage,
                 'user': user
            }
        return render(request, 'index.html', context = context)
    else:
        form = AuthenticationForm()
        context ={
            "form":form}
        return render(request, 'login.html', context=context)

def login(request):
    if(request.method == 'GET'):
        form = AuthenticationForm()
        context ={
            "form":form}
        return render(request, 'login.html', context=context)
    else:
        form = AuthenticationForm(data = request.POST)

        if(form.is_valid()):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            #print("Authenticated", user)
            if(user is not None):
                loginUser(request, user)
                return redirect('home')
        else:
            logger.error(f"{log_function_name(logger)} - {request.user} username or password is wrong | Redirecting to Login Page")
            context ={
                "form":form
            }
            return render(request, 'login.html', context=context)

def signup(request):
    if(request.method == 'GET'):
        form = UserCreationForm()

        context = {
            "form": form
            }
        return render(request, 'singup.html', context = context)
    else:
        #print(request.POST)
        form = UserCreationForm(request.POST)
        context = {
            "form": form
            }
        if (form.is_valid()):
            user = form.save()
            if(user is not None):
                return redirect('login')

        else:
            #Log The error
            logger.error(f"{log_function_name(logger)} - {request.user} User Creation Form is Invalid | Try signing in again")
            #log ends
            return render(request, 'singup.html', context = context)

#add the todo list
@login_required(login_url='login')
def add_todo(request):
    
    #check if user is logged in or not
    if(request.user.is_authenticated): 
        user = request.user
        #print("User: ",user)
        form = TODOForm(request.POST)
        
        todo = form.save(commit=False)
        todo.user = user
        todo.save()
        #print(todo)
        #print(f"Todo :{todo}")
        if(form.is_valid()):
            #print(form.cleaned_data) 
            return redirect('home')
        else:
            return render(request, 'index.html', context = {'form': form})


def signout(request):
    logout(request)
    return redirect('login')

def delete_todo(request, id):
    TODO.objects.get(pk=id).delete()
    return redirect('home')

def change_todo(request, id, status):
    todo = TODO.objects.get(pk=id)
    todo.status = status
    todo.save()
    return redirect('home')

def update_todo(request, id):
    update_todo = TODO.objects.get(id=id)
    form = TODOForm(instance=update_todo)

    if(request.method == 'POST'):
        form = TODOForm(request.POST, instance = update_todo)
        if(form.is_valid()):
            form.save()
            return redirect('home')

    
    context = {'form': form}
    return render(request, 'update.html', context)
