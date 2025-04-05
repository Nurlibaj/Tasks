from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from .models import Classroom, Student, ViolationLevel, ViolationType, ViolationAct,PointReward
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import get_template
import os
from django.conf import settings


@login_required
def home_view(request):
    return render(request, 'app/home.html')
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # позже добавим домашнюю страницу

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный email или пароль.')

    return render(request, 'app/login.html')
def logout_view(request):
    logout(request)
    return redirect('login')


# Акт составление
@login_required
def violation_section(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        violation_id = request.POST.get('violation_id')
        comment = request.POST.get('comment')
        points = request.POST.get('points')

        ViolationAct.objects.create(
            from_user=request.user,
            to_student_id=student_id,
            violation_id=violation_id,
            comment=comment,
            points=points,
            created_at=date.today()
        )
        return JsonResponse({'status': 'ok'})

    classrooms = Classroom.objects.all()
    levels = ViolationLevel.objects.all()
    return render(request, 'app/violation.html', {
        'classrooms': classrooms,
        'levels': levels
    })
@login_required
def api_students(request):
    class_id = request.GET.get('classroom_id')
    students = Student.objects.filter(classroom_id=class_id).values('id', 'full_name')
    return JsonResponse(list(students), safe=False)
@login_required
def api_violations(request):
    level_id = request.GET.get('level_id')
    violations = ViolationType.objects.filter(level_id=level_id).values('id', 'name')
    return JsonResponse(list(violations), safe=False)
#Награда
@login_required
def reward_section(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        comment = request.POST.get('comment')
        points = request.POST.get('points')

        # Для замдиректора добавим в комментарий категорию и уровень
        if request.user.role == 3:
            category = request.POST.get('category', '')
            level = request.POST.get('level', '')
            if category:
                comment = f"[{category}" + (f" - {level}]" if level else "]") + " " + comment

        PointReward.objects.create(
            from_user=request.user,
            to_student_id=student_id,
            comment=comment,
            points=points
        )
        return JsonResponse({'status': 'ok'})

    classrooms = Classroom.objects.all()
    return render(request, 'app/reward.html', {
        'classrooms': classrooms
    })

# Показ моих актов
@login_required
def my_acts_view(request):
    acts = ViolationAct.objects.filter(from_user=request.user).order_by('-created_at')
    return render(request, 'app/my_acts.html', {'acts': acts})

#Создание акт файла
@login_required
def act_pdf_view(request, id):
    act = ViolationAct.objects.get(id=id, from_user=request.user)
    template = get_template('pdf/act.html')

    font_path = os.path.join(settings.BASE_DIR, 'app', 'fonts', 'DejaVuSans.ttf').replace('\\', '/')


    html = template.render({
        'act': act,
        'font_path': font_path,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=act-{id}.pdf'

    pisa_status = pisa.CreatePDF(BytesIO(html.encode("utf-8")), dest=response, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse('Ошибка генерации PDF', status=500)
    return response
