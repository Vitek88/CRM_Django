from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.
def home(request):
    records = Record.objects.all()  # Fetch all records from the database
    context = {"records": records}

    #if loging in user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')  # Redirect to home or another page after login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')
    else:
        return render(request, 'home.html', context)

# def login_user(request):
#     pass

def logout_user(request):
    logout(request)
    messages.success(request, f'User has been logged out.')
    return redirect('home')  # Redirect to home or another page after logout

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            #Authenticate the user after registration and login
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'customer_record.html', {'record': record})
    else:
        messages.warning(request, f'You are not allowed to get this data!')
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, f'Record has been deleted successfully!')
        return redirect('home')
    else:
        messages.warning(request, f'You are not allowed to delete this data!')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record added successfully!')
                return redirect('home')
        
    else:
        messages.warning(request, f'You must be logged in to add a record!')
        return redirect('home')

    context = {"form": form}
    return render(request, 'add_record.html', context)

def update_record(request, pk):
    if request.user.is_authenticated:
        record =Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully!')
            return redirect('home')
    else:
        messages.warning(request, f'You must be logged in to update a record!')
        return redirect('home')
    context = {"form": form}
    return render(request, 'add_record.html', context)