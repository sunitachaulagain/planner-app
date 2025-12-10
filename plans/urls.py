from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    # Root
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Categories
    path('categories/', views.list_categories, name='list_categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    # Plans
    path('plans/', views.list_plans, name='list_plans'),
    path('plans/add/', views.add_plan, name='add_plan'),
    path('plans/edit/<int:pk>/', views.edit_plan, name='edit_plan'),
    path('plans/delete/<int:pk>/', views.delete_plan, name='delete_plan'),
    path('categories/<int:category_id>/plans/', views.list_plans_by_category, name='list_plans_by_category'),

    # Tasks
    # path('tasks/', views.list_tasks, name='list_tasks'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/edit/<int:pk>/', views.edit_task, name='edit_task'),
    path('tasks/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/toggle/', views.toggle_task_complete, name='toggle_task_complete'),

    # Profile
    path('profile/', views.profile_view, name='profile'),

    # Password change
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
