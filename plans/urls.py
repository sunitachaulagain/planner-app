from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),  # root URL
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    
    # categories
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    
    # Plan CRUD
    path('plans/', views.list_plans, name='list_plans'),
    path('plans/add/', views.add_plan, name='add_plan'),
    path('plans/edit/<int:pk>/', views.edit_plan, name='edit_plan'),
    path('plans/delete/<int:pk>/', views.delete_plan, name='delete_plan'),
    path('categories/<int:category_id>/plans/', views.list_plans_by_category, name='list_plans_by_category'),
    
    #task crud
    
    path('tasks/', views.list_tasks, name='list_tasks'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:pk>/', views.delete_task, name='delete_task'),
    
    
    #detail view
    path('categories/<int:category_id>/', views.category_detail_view, name='category_detail'),


]
