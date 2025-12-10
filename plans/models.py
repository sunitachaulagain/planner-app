from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta


# ==========================
# Profile
# ==========================
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username


# Signal to create/update Profile automatically
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()


# ==========================
# Category
# ==========================
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ==========================
# Plan
# ==========================
class Plan(models.Model):
    PLAN_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    plan_type = models.CharField(max_length=10, choices=PLAN_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  # auto-calculated or user-defined
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Auto-calculate end_date for non-custom plans
        if self.plan_type != 'custom' and self.start_date:
            if self.plan_type == 'daily':
                self.end_date = self.start_date
            elif self.plan_type == 'weekly':
                self.end_date = self.start_date + timedelta(days=6)
            elif self.plan_type == 'monthly':
                self.end_date = self.start_date + timedelta(days=29)  # simple 30-day month
        super().save(*args, **kwargs)

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.title} ({self.user.username})"


# ==========================
# Task
# ==========================
class Task(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='tasks')
    day_number = models.PositiveIntegerField()  # which day of the plan
    task_date = models.DateField(blank=True, null=True)  # auto-calculated
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    estimated_time = models.FloatField(help_text="Estimated time in hours", blank=True, null=True)
    time_taken = models.FloatField(help_text="Actual time spent in hours", blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    summary = models.TextField(blank=True, null=True)  # reflection notes
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Auto-calculate task_date from plan's start_date + day_number
        if self.plan and self.day_number:
            self.task_date = self.plan.start_date + timedelta(days=self.day_number - 1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.plan.title})"
