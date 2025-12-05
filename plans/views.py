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


