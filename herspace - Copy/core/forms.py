from django import forms
from .models import MoodEntry, JournalEntry, FinanceEntry, Goal, EmergencyContact

class MoodForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood']

class JournalForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['title', 'content']

class FinanceForm(forms.ModelForm):
    class Meta:
        model = FinanceEntry
        fields = ['entry_type', 'description', 'amount']

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'target_amount', 'current_progress']

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'phone']