from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, role, password=None):
        if not email:
            raise ValueError("Email обязателен")
        user = self.model(email=self.normalize_email(email), full_name=full_name, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, role=0, password=None):
        user = self.create_user(email=email, full_name=full_name, role=role, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'Teacher'),
        (2, 'Curator'),
        (3, 'Vice'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']
    objects = UserManager()
    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"


class Classroom(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Shanyrak(models.Model):
    name = models.CharField(max_length=50)
    curator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 2})

    def __str__(self):
        return self.name



class Student(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    birth_date = models.DateField()
    classroom = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True)
    shanyrak = models.ForeignKey(Shanyrak, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class PointReward(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    points = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.points} баллов → {self.to_student.full_name}"
class ViolationAct(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    violation = models.ForeignKey('ViolationType', on_delete=models.SET_NULL, null=True)
    points = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Акт: {self.violation.name} для {self.to_student.full_name}"

class ViolationLevel(models.Model):
    name = models.CharField(max_length=50)
    min_points = models.IntegerField()
    max_points = models.IntegerField()

    def __str__(self):
        return self.name

class ViolationType(models.Model):
    name = models.CharField(max_length=255)
    level = models.ForeignKey(ViolationLevel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ArchiveEntry(models.Model):
    year = models.CharField(
        max_length=9,
        help_text="Учебный год, например: 2024-2025"
    )
    student_full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('M', 'Мальчик'), ('F', 'Девочка')])
    class_name = models.CharField(max_length=10)
    shanyrak_name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=20,
        choices=[('reward', 'Награда'), ('violation', 'Наказание')]
    )
    from_full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    comment = models.TextField()
    points = models.IntegerField()
    violation_type = models.CharField(max_length=255, null=True, blank=True)
    violation_level = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"[{self.year}] {self.student_full_name} ({self.type}) — {self.points} баллов"