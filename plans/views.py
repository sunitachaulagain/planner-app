from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import datetime

from .forms import SignUpForm, LoginForm, CategoryForm, PlanForm, TaskForm, ProfileForm
from .models import Profile, Category, Plan, Task
from django.contrib.auth import login
from .models import Profile

# ===========================
# AUTH
# ===========================
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'registration/login.html', {'form': form})


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'plans/home_public.html')


# ===========================
# DASHBOARD
# ===========================
@login_required
def dashboard_view(request):
    today = datetime.date.today()
    today_tasks = Task.objects.filter(user=request.user, task_date=today)

    # Group tasks: category -> plan -> list of tasks
    grouped = {}
    for task in today_tasks:
        cat_name = task.plan.category.name
        plan_title = task.plan.title
        grouped.setdefault(cat_name, {}).setdefault(plan_title, []).append(task)

    # Pie chart data
    completed_count = today_tasks.filter(is_completed=True).count()
    pending_count = today_tasks.filter(is_completed=False).count()
    today_pie = [completed_count, pending_count]

    context = {
        "grouped": grouped,
        "today_pie": today_pie,
        "profile": request.user.profile,  # signals ensure profile exists
    }
    return render(request, 'plans/dashboard.html', context)


# ===========================
# CATEGORIES
# ===========================
@login_required
def list_categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'plans/category_list.html', {'categories': categories})


@login_required
def add_category(request):
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect('list_categories')
    return render(request, 'plans/category_form.html', {'form': form, 'title': 'Add Category'})


@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    form = CategoryForm(request.POST or None, instance=category)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_categories')
    return render(request, 'plans/category_form.html', {'form': form, 'title': 'Edit Category'})


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('list_categories')
    return render(request, 'plans/category_confirm_delete.html', {'category': category})


# ===========================
# PLANS
# ===========================
@login_required
def list_plans(request):
    plans = Plan.objects.filter(user=request.user)
    return render(request, 'plans/plan_list.html', {'plans': plans})


@login_required
def add_plan(request):
    category_id = request.GET.get('category')
    category = get_object_or_404(Category, pk=category_id, user=request.user)
    form = PlanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        plan = form.save(commit=False)
        plan.user = request.user
        plan.category = category
        plan.save()
        return redirect('list_plans_by_category', category_id=category.id)
    return render(request, 'plans/plan_form.html', {'form': form})


@login_required
def edit_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)
    form = PlanForm(request.POST or None, instance=plan)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_plans')
    return render(request, 'plans/plan_form.html', {'form': form})

@login_required
def delete_plan(request, pk):
    plan = get_object_or_404(Plan, pk=pk, user=request.user)
    category_id = plan.category.id  # keep for redirect

    if request.method == 'POST':
        plan.delete()
        return redirect('list_plans_by_category', category_id=category_id)

    return render(request, 'plans/plan_confirm_delete.html', {'plan': plan})



@login_required
def list_plans_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id, user=request.user)
    plans = Plan.objects.filter(category=category, user=request.user)

    plans_with_tasks = []
    for plan in plans:
        tasks = Task.objects.filter(plan=plan, user=request.user).order_by('task_date', 'day_number')
        total = tasks.count()
        completed = tasks.filter(is_completed=True).count()
        percent = int((completed / total) * 100) if total else 0

        # Group tasks by day_number
        tasks_by_day = {}
        for task in tasks:
            tasks_by_day.setdefault(task.day_number or 1, []).append(task)

        plans_with_tasks.append({
            'plan': plan,
            'tasks': tasks,
            'tasks_by_day': tasks_by_day,
            'total_tasks': total,
            'completed_tasks': completed,
            'percent': percent,
        })

    return render(request, 'plans/plan_list.html', {'category': category, 'plans_with_tasks': plans_with_tasks})


# ===========================
# TASKS
# ===========================


@login_required
def add_task(request):
    plan_id = request.GET.get('plan')
    plan = get_object_or_404(Plan, id=plan_id, user=request.user)
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.plan = plan
        task.save()
        return redirect('list_plans_by_category', category_id=plan.category.id)
    return render(request, 'plans/task_form.html', {'form': form, 'plan': plan})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('list_tasks')
    return render(request, 'plans/task_form.html', {'form': form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        category_id = task.plan.category.id  # redirect to the category plan list
        task.delete()
        return redirect('list_plans_by_category', category_id=category_id)

    return render(request, 'plans/task_confirm_delete.html', {
        'task': task
    })


@login_required
def toggle_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


# ===========================
# PROFILE
# ===========================
@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'plans/profile.html', {'profile': profile})
