from django.shortcuts import render, get_object_or_404, redirect
from .models import TodoList, Task
from .forms import TodoListForm, TaskForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def signUp(r):
    if r.method == 'POST':
        form = UserCreationForm(r.POST)
        if form.is_valid():
            user = form.save()
            login(r, user)
            messages.success(r, f"You've Signed Up!")  
            return redirect('todo_list')
        else:
            messages.error(r, f'Fill The Fields Correctly!')
    else:
        form = UserCreationForm()
    
    return render(r, 'todo/signup.html', {'form': form})

@login_required
def logOut(r):
    if r.method == 'POST':
        logout(r)
        messages.success(r, f"You've Been Logged Out!")
        return redirect('todo_list')
    else:
        return render(r, 'todo/logout.html')

def logIn(r):
    if r.user.is_authenticated:
        return redirect('todo_list')
    
    if r.method == 'POST':
        form = AuthenticationForm(request=r, data=r.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(r, user)
                messages.success(r, f"You've Been Logged In!")
                return redirect('todo_list')
        else:
            messages.error(r, f'Invalid Username Or Password!')
            
    form = AuthenticationForm()
    return render(r, 'todo/login.html', {'form': form})

@login_required
def changePass(r):
    user = r.user
    if r.method == 'POST':
        form = PasswordChangeForm(user, r.POST)
        if form.is_valid():
            form.save()
            messages.success(r, 'Your Password Has Been Changed!')
            return redirect('login')
    form = PasswordChangeForm(user)
    return render(r, 'todo/changepass.html', {'form': form})

def list(r):
    lists = TodoList.objects.filter(user=r.user.id)
    query = r.GET.get('q')  
    sort_by = r.GET.get('sort')
    if query:
        lists = lists.filter(Q(title__icontains=query))
    if sort_by == 'created_asc':
        lists = lists.order_by('time')
    elif sort_by == 'created_desc':
        lists = lists.order_by('-time')
    else:
        TodoList.objects.filter(user=r.user.id)
    return render(r, 'todo/viewlist.html', {'lists': lists})

@login_required
def detail(r, pk):
    todo_list = get_object_or_404(TodoList, pk=pk)
    tasks = todo_list.tasks.all()

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    
    if total_tasks > 0:
        progress = int((completed_tasks / total_tasks) * 100)
    else:
        progress = 0

    status = r.GET.get('status')
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'pending':
        tasks = tasks.filter(completed=False)
    else:
        tasks = todo_list.tasks.all()

    sort_by = r.GET.get('sort')
    if sort_by == 'due':
        tasks = tasks.order_by('due')
    elif sort_by == 'priority':
        tasks = tasks.order_by('-priority')

    return render(r, 'todo/detail.html', {'todo_list': todo_list, 'tasks': tasks, 'progress': progress})

@login_required
def addlist(r):
    if r.method == 'POST':
        form = TodoListForm(r.POST)
        if form.is_valid():
            todo_list = form.save(commit=False)
            todo_list.user = r.user
            form.save()
            messages.success(r, 'New List Has Been Added!')
            return redirect('todo_list')
    else:
        form = TodoListForm()
    return render(r, 'todo/addlist.html', {'form': form})

@login_required
def deletelist(r, pk):
    todo_list = get_object_or_404(TodoList, pk=pk)
    todo_list.delete()
    messages.success(r, 'The List Has Been Deleted!')
    return redirect('todo_list')

@login_required
def add_task(r, pk):
    todo_list = get_object_or_404(TodoList, pk=pk)
    if r.method == 'POST':
        form = TaskForm(r.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.todo_list = todo_list
            task.save()
            messages.success(r, 'New Task Has Been Added!')
            return redirect('todo_detail', pk=todo_list.pk)
        else:
            messages.error(r, 'Fill the Bars Correctly!')
    else:
        form = TaskForm()
    return render(r, 'todo/addtask.html', {'form': form, 'todo_list': todo_list})

@login_required
def edit_task(r, pk, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    if r.method == 'POST':
        form = TaskForm(r.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(r, 'The Task Has Been Edited!')
            return redirect('todo_detail', pk=task.todo_list.pk)
        else:
            messages.error(r, 'Fill The Fields Correctly!')
    else:
        form = TaskForm(instance=task)
    return render(r, 'todo/edittask.html', {'form': form, 'todo_list': task.todo_list})

@login_required
def delete_task(r, pk, task_pk):
    task = get_object_or_404(Task, pk=task_pk)
    task.delete()
    messages.success(r, 'The Task Has Been Deleted!')
    return redirect('todo_detail', pk=pk)
