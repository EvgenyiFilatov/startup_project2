from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from startup.models import Startup, StartupDeveloper
from startup.forms import StartupForm, StartupDeveloperFormSet
from django.db.models import Q
from django.core.paginator import Paginator

from startup.permissions import (
    custom_login_required,
    admin_or_owner_required,
    owner_required
)


@custom_login_required
def wellcome_view(request):
    user = request.user
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        if first_name and last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return render(request, 'wellcome.html')

        else:
            messages.error(request, "Пожалуйста, заполните оба поля.")

    return render(request, 'wellcome.html')


@custom_login_required
def startup_list(request):
    startups = Startup.objects.filter(
        Q(creator=request.user) | Q(startupdeveloper__user=request.user)
    ).distinct()
    paginator = Paginator(startups, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'POST':
        form = StartupForm(request.POST)
        if form.is_valid():
            startup = form.save(commit=False)
            startup.creator = request.user
            formset = StartupDeveloperFormSet(request.POST, instance=startup)
            if formset.is_valid():
                startup.save()
                formset.save()
                StartupDeveloper.objects.create(
                    startup=startup, user=request.user, role='owner'
                )
                return redirect('startup:startup_detail', pk=startup.id)
        else:
            formset = StartupDeveloperFormSet(request.POST)
    else:
        form = StartupForm()
        formset = StartupDeveloperFormSet(instance=Startup())
    context = {
        'startups': [{'startup': startup}for startup in page_obj],
        "page_obj": page_obj,
        "form": form,
        "formset": formset
    }
    return render(request, "startup_list.html", context)


@custom_login_required
def startup_detail(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    members = StartupDeveloper.objects.filter(startup=startup)
    context = {
        'startup': startup,
        'members': members,
    }
    return render(request, 'startup_detail.html', context)


@admin_or_owner_required
def startup_edit(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    if request.method == 'POST':
        form = StartupForm(request.POST, instance=startup)
        formset = StartupDeveloperFormSet(request.POST, instance=startup)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('startup:startup_detail', pk=startup.pk)
    else:
        form = StartupForm(instance=startup)
        formset = StartupDeveloperFormSet(instance=startup)
    context = {
        'form': form,
        'formset': formset,
        'startup': startup
    }
    return render(request, 'startup_edit.html', context)


@owner_required
def startup_delete(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    if request.method == "POST":
        startup.delete()
        return redirect('startup:startup_list')
    context = {'startup': startup}
    return render(request, 'startup_delete.html', context)
