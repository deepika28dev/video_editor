from django.contrib import admin
from .models import *

@admin.register(Clips)
class ClipsAdmin(admin.ModelAdmin):
  list_display = ('id','video','title','subclips','thumbnail_url')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ('id', 'username', 'email')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'age', 'address')

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'profile')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  list_display = ('id', 'first_name', 'last_name','roll_number')

  def has_add_permission(self, request):
    return False

  def has_delete_permission(self, request, obj=None):
    return False