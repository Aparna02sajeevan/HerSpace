from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from collections import defaultdict
import random

from .forms import (
    MoodForm,
    JournalForm,
    FinanceForm,
    GoalForm,
    EmergencyContactForm
)

from .models import (
    MoodEntry,
    JournalEntry,
    FinanceEntry,
    Goal,
    EmergencyContact
)


# ================= LANDING =================
def landing(request):
    return render(request, 'landing.html')


# ================= SIGNUP =================
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


# ================= DASHBOARD =================
@login_required
def dashboard(request):
    moods = MoodEntry.objects.filter(
        user=request.user
    ).order_by('-created_at')

    suggestion = None
    mood_stats = None

    if moods.exists():
        latest_mood = moods.first().mood.strip()

        if latest_mood == "Stressed":
            suggestion = "meditate"
        elif latest_mood == "Sad":
            suggestion = "music"
        elif latest_mood == "Happy":
            suggestion = "confidence"
        elif latest_mood == "Neutral":
            suggestion = "journal"

        mood_stats = moods.values('mood').annotate(
            count=Count('mood')
        ).order_by('-count')

    return render(request, 'dashboard.html', {
        "moods": moods,
        "suggestion": suggestion,
        "mood_stats": mood_stats
    })


# ================= ADD MOOD =================
@login_required
def add_mood(request):
    if request.method == 'POST':
        form = MoodForm(request.POST)
        if form.is_valid():
            mood = form.save(commit=False)
            mood.user = request.user
            mood.save()
            return redirect('dashboard')
    else:
        form = MoodForm()

    return render(request, 'mood.html', {'form': form})


# ================= JOURNAL =================
@login_required
def journal(request):
    entries = JournalEntry.objects.filter(
        user=request.user
    ).order_by('-created_at')

    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('journal')
    else:
        form = JournalForm()

    return render(request, 'journal.html', {
        'form': form,
        'entries': entries
    })


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(
        JournalEntry,
        id=entry_id,
        user=request.user
    )
    entry.delete()
    return redirect('journal')


# ================= WELLNESS =================
@login_required
def music(request):
    return render(request, 'music.html')


@login_required
def meditate(request):
    return render(request, 'meditate.html')


@login_required
def doodle(request):
    return render(request, 'doodle.html')


@login_required
def drums(request):
    return render(request, 'drums.html')


# ================= CAREER =================
@login_required
def career(request):
    return render(request, 'career.html')


# ================= CONFIDENCE =================
def confidence(request):
    affirmations = [
        "You are capable of achieving great things.",
        "Your voice matters.",
        "You are stronger than your fears.",
        "Progress is more important than perfection."
    ]
    message = random.choice(affirmations)

    return render(request, 'confidence.html', {
        "message": message
    })


# ================= GOALS =================
@login_required
def goals(request):
    goals = Goal.objects.filter(user=request.user)

    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals')
    else:
        form = GoalForm()

    return render(request, 'goals.html', {
        'goals': goals,
        'form': form
    })


# ================= FINANCE =================
@login_required
def finance(request):
    selected_month = request.GET.get('month')

    entries = FinanceEntry.objects.filter(user=request.user)

    if selected_month:
        year, month = selected_month.split('-')
        entries = entries.filter(
            created_at__year=year,
            created_at__month=month
        )

    entries = entries.order_by('-created_at')

    if request.method == 'POST':
        form = FinanceForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('finance')
    else:
        form = FinanceForm()

    total_income = sum(
        e.amount for e in entries if e.entry_type == "Income"
    )
    total_expense = sum(
        e.amount for e in entries if e.entry_type == "Expense"
    )

    balance = total_income - total_expense

    expense_dict = defaultdict(float)
    for entry in entries:
        if entry.entry_type == "Expense":
            expense_dict[entry.description] += float(entry.amount)

    chart_labels = list(expense_dict.keys())
    chart_data = list(expense_dict.values())

    spending_alert = total_expense > total_income

    return render(request, 'finance.html', {
        'form': form,
        'entries': entries,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'spending_alert': spending_alert,
        'selected_month': selected_month
    })


# ================= EMERGENCY =================
@login_required
def emergency(request):
    contacts = EmergencyContact.objects.filter(user=request.user)

    if request.method == 'POST':
        form = EmergencyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('emergency')
    else:
        form = EmergencyContactForm()

    return render(request, 'emergency.html', {
        'contacts': contacts,
        'form': form
    })