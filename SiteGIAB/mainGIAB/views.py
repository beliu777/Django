from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Document, DataSet
from .document_generator import generate_title_page, generate_assignment, generate_diary

def mainGIAB(request):
    return HttpResponse('app mainGIAB')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            DataSet.objects.create(user=user)
            messages.success(request, 'Регистрация прошла успешно! Теперь войдите в систему.')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте введенные данные.')
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def loginf(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Вы вошли как {username}')
                return redirect('profile')
            else:
                messages.error(request, 'Неправильное имя пользователя или пароль')
        else:
            messages.error(request, 'Неправильное имя пользователя или пароль')
    
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    data_instance, created = DataSet.objects.get_or_create(user=request.user)

    if request.method == 'POST' and 'reset' in request.POST:
        data_instance.refresh_from_db()
        messages.info(request, 'Данные сброшены до последнего сохраненного состояния')
        return redirect('profile')

    if request.method == 'POST':
        # Сохраняем данные из формы перед обычным сохранением И перед скачиванием.
        data_instance.familia = request.POST.get('familia', '')
        data_instance.name = request.POST.get('name', '')
        data_instance.otchestvo = request.POST.get('otchestvo', '')
        data_instance.tip = request.POST.get('tip', '')
        data_instance.tip_title = request.POST.get('tip_title', '')
        data_instance.module = request.POST.get('module', '')
        data_instance.module_code = request.POST.get('module_code', '')
        data_instance.specialization = request.POST.get('specialization', '')
        data_instance.group = request.POST.get('group', '')
        data_instance.date_begin = request.POST.get('date_begin', '')
        data_instance.date_finish = request.POST.get('date_finish', '')
        data_instance.head1 = request.POST.get('head1', '')
        data_instance.head2 = request.POST.get('head2', '')
        data_instance.ruc_pract = request.POST.get('ruc_pract', '')
        data_instance.fio_genitive = request.POST.get('fio_genitive', '')

        try:
            data_instance.kurs = int(request.POST.get('kurs') or 2)
        except (TypeError, ValueError):
            data_instance.kurs = 2

        try:
            data_instance.year = int(request.POST.get('year') or 2026)
        except (TypeError, ValueError):
            data_instance.year = 2026

        data_instance.save()

        # Если нажата кнопка скачивания, сразу генерируем документ с новыми данными.
        download_type = request.POST.get('download')
        if download_type == 'title':
            return generate_title_page(data_instance)
        if download_type == 'assignment':
            return generate_assignment(data_instance)
        if download_type == 'diary':
            return generate_diary(data_instance)

        messages.success(request, 'Данные успешно сохранены!')
        return redirect('profile')

    documents = Document.objects.all()

    context = {
        'data': data_instance,
        'documents': documents,
        'current_user': request.user.username,
    }
    return render(request, "profile.html", context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('login')

# Функции для скачивания документов
@login_required
def download_title(request):
    data_instance = DataSet.objects.get(user=request.user)
    return generate_title_page(data_instance)

@login_required
def download_assignment(request):
    data_instance = DataSet.objects.get(user=request.user)
    return generate_assignment(data_instance)

@login_required
def download_diary(request):
    data_instance = DataSet.objects.get(user=request.user)
    return generate_diary(data_instance)
