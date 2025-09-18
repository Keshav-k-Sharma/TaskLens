from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .models import Category, ActivityLog
from .forms import CategoryForm, ActivityLogForm
from datetime import date, datetime

# Homepage: shows today's logs
@login_required
def home(request):
    today = date.today()
    logs = ActivityLog.objects.filter(user=request.user, start_time__date=today).order_by('start_time')
    return render(request, 'activity/home.html', {'logs': logs})

# Add a new log
@login_required
def add_log(request):
    if not Category.objects.filter(user=request.user).exists():
        return render(request, 'activity/no_categories.html')

    if request.method == 'POST':
        form = ActivityLogForm(request.POST, user=request.user)
        if form.is_valid():
            cd = form.cleaned_data

            def convert_to_24h(t, meridiem):
                hour = t.hour
                if meridiem == 'PM' and hour < 12:
                    hour += 12
                elif meridiem == 'AM' and hour == 12:
                    hour = 0
                return t.replace(hour=hour)

            start_dt = datetime.combine(cd['date'], convert_to_24h(cd['start_time'], cd['start_meridiem']))
            end_dt = datetime.combine(cd['date'], convert_to_24h(cd['end_time'], cd['end_meridiem']))

            ActivityLog.objects.create(
                user=request.user,
                category=cd['category'],
                description=cd['description'],
                date=cd['date'],
                start_time=start_dt,
                end_time=end_dt
            )
            return redirect('home')
    else:
        form = ActivityLogForm(user=request.user)

    return render(request, 'activity/add_log_combined.html', {'log_form': form})

# Register a new user
def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'activity/register.html', {'form': form})

# Manage categories
@login_required
def manage_categories(request):
    category_form = CategoryForm(request.POST or None)
    categories = Category.objects.filter(user=request.user)

    if 'add_category' in request.POST and category_form.is_valid():
        new_cat = category_form.save(commit=False)
        new_cat.user = request.user
        new_cat.save()
        return redirect('manage_categories')

    return render(request, 'activity/manage_categories.html', {
        'category_form': category_form,
        'categories': categories,
        'title': 'Manage Categories'
    })


# Delete a category
@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('add_log')
    return render(request, 'activity/confirm_delete.html', {'category': category})

# Edit an existing log
@login_required
def edit_log(request, pk):
    log = get_object_or_404(ActivityLog, pk=pk, user=request.user)

    if request.method == 'POST':
        form = ActivityLogForm(request.POST, user=request.user)
        if form.is_valid():
            cd = form.cleaned_data

            def convert_to_24h(t, meridiem):
                hour = t.hour
                if meridiem == 'PM' and hour < 12:
                    hour += 12
                elif meridiem == 'AM' and hour == 12:
                    hour = 0
                return t.replace(hour=hour)

            log.category = cd['category']
            log.description = cd['description']
            log.date = cd['date']
            log.start_time = datetime.combine(cd['date'], convert_to_24h(cd['start_time'], cd['start_meridiem']))
            log.end_time = datetime.combine(cd['date'], convert_to_24h(cd['end_time'], cd['end_meridiem']))
            log.save()
            return redirect('home')
    else:
        initial = {
            'category': log.category,
            'description': log.description,
            'date': log.date,
            'start_time': log.start_time.time(),
            'start_meridiem': 'AM' if log.start_time.hour < 12 else 'PM',
            'end_time': log.end_time.time(),
            'end_meridiem': 'AM' if log.end_time.hour < 12 else 'PM',
        }
        form = ActivityLogForm(initial=initial, user=request.user)

    return render(request, 'activity/edit_log.html', {'log_form': form, 'title': 'Edit Log'})

# Delete a log
@login_required
def delete_log(request, pk):
    log = get_object_or_404(ActivityLog, pk=pk, user=request.user)
    log.delete()
    return redirect('home')

# Logout
def custom_logout(request):
    logout(request)
    return redirect('/login/')