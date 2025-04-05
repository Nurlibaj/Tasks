from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Student, Classroom, Shanyrak,
    ViolationLevel, ViolationType, ViolationAct,
    PointReward,ArchiveEntry
)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('full_name', 'role')}),
        ('Права', {'fields': ('is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'full_name')
    ordering = ('email',)
    filter_horizontal = ()

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'classroom', 'shanyrak', 'is_active')
    list_filter = ('classroom', 'shanyrak', 'is_active')
    search_fields = ('full_name', 'email')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Shanyrak)
class ShanyrakAdmin(admin.ModelAdmin):
    list_display = ('name', 'curator')

@admin.register(ViolationLevel)
class ViolationLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'min_points', 'max_points')

@admin.register(ViolationType)
class ViolationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')

@admin.register(ViolationAct)
class ViolationActAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_student', 'violation', 'points', 'created_at')
    list_filter = ('violation__level', 'created_at')

@admin.register(PointReward)
class PointRewardAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_student', 'points', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('comment',)

@admin.register(ArchiveEntry)
class ArchiveEntryAdmin(admin.ModelAdmin):
    list_display = (
        'student_full_name', 'year', 'type', 'points', 'class_name',
        'shanyrak_name', 'from_full_name', 'date'
    )
    list_filter = ('year', 'type', 'shanyrak_name', 'class_name')
    search_fields = ('student_full_name', 'from_full_name', 'comment', 'violation_type')