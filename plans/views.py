from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # we’ll create this later
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')



#for day 3 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category
from .forms import CategoryForm
from django.contrib.auth.decorators import login_required

# List categories
@login_required
def list_categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'plans/category_list.html', {'categories': categories})

# Add category
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('list_categories')
    else:
        form = CategoryForm()
    return render(request, 'plans/category_form.html', {'form': form, 'title': 'Add Category'})

# Edit category
@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('list_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'plans/category_form.html', {'form': form, 'title': 'Edit Category'})

# Delete category
@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('list_categories')
    return render(request, 'plans/category_confirm_delete.html', {'category': category})



#plans
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PlanForm
from .models import Plan, Category
from django.contrib.auth.decorators import login_required

@login_required
def list_plans(request):
    plans = Plan.objects.filter(user=request.user)
    return render(request, 'plans/plan_list.html', {'plans': plans})

@login_required
def add_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect('list_plans')
    else:
        form = PlanForm()
    return render(request, 'plans/plan_form.html', {'form': form})

@login_required
def edit_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('list_plans')
    else:
        form = PlanForm(instance=plan)
    return render(request, 'plans/plan_form.html', {'form': form})

@login_required
def delete_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)
    plan.delete()
    return redirect('list_plans')

def list_plans_by_category(request, category_id):
    user = request.user
    category = get_object_or_404(Category, pk=category_id, user=user)
    plans = Plan.objects.filter(user=user, category=category)
    return render(request, 'plans/plan_list.html', {'plans': plans, 'category': category})



from django.shortcuts import render
from .models import Category, Plan, Task
from django.utils import timezone
from datetime import timedelta

def dashboard_view(request):
    user = request.user
    today = timezone.localdate()

    # Stats
    total_categories = Category.objects.filter(user=user).count()
    total_plans = Plan.objects.filter(user=user).count()
    tasks_today = Task.objects.filter(
        user=user, plan__start_date__lte=today, plan__end_date__gte=today
    )
    tasks_completed = tasks_today.filter(is_completed=True)  # corrected

    # Chart Data: last 7 days
    chart_labels = []
    chart_completed = []
    chart_pending = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_tasks = Task.objects.filter(
            user=user, plan__start_date__lte=day, plan__end_date__gte=day
        )
        chart_labels.append(day.strftime("%b %d"))
        chart_completed.append(day_tasks.filter(is_completed=True).count())  # corrected
        chart_pending.append(day_tasks.filter(is_completed=False).count())  # corrected

    context = {
        'total_categories': total_categories,
        'total_plans': total_plans,
        'tasks_today': tasks_today,
        'tasks_completed': tasks_completed,
        'chart_labels': chart_labels,
        'chart_completed': chart_completed,
        'chart_pending': chart_pending,
    }

    return render(request, 'plans/dashboard.html', context)




#task 
from .forms import TaskForm
from .models import Task, Plan
from django.shortcuts import render, redirect, get_object_or_404

# List Tasks
def list_tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'plans/task_list.html', {'tasks': tasks})

# Add Task
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('list_tasks')
    else:
        form = TaskForm()
    return render(request, 'plans/task_form.html', {'form': form})

# Edit Task
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('list_tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'plans/task_form.html', {'form': form})

# Delete Task
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('list_tasks')
    return render(request, 'plans/task_confirm_delete.html', {'task': task})



from django.shortcuts import render, get_object_or_404
from .models import Category, Plan, Task

def category_detail_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id, user=request.user)
    plans = Plan.objects.filter(category=category, user=request.user)

    # Optional: load tasks for each plan
    plan_tasks = {}
    for plan in plans:
        tasks = Task.objects.filter(plan=plan, user=request.user)
        plan_tasks[plan.id] = tasks

    context = {
        'category': category,
        'plans': plans,
        'plan_tasks': plan_tasks,
    }
    return render(request, 'plans/category_detail.html', context)


def home_view(request):
    if request.user.is_authenticated:
        # Redirect logged-in users to dashboard
        return redirect('dashboard')
    # Show public home page to everyone else
    return render(request, 'plans/home_public.html')

