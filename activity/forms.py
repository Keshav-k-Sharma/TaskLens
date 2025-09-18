from django import forms
from .models import Category
from datetime import date


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']


class ActivityLogForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.none())
    description = forms.CharField(widget=forms.Textarea)
    date = forms.DateField(
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Date'
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M', attrs={'placeholder': 'HH:MM'}),
        label='Start Time'
    )
    start_meridiem = forms.ChoiceField(choices=[('AM', 'AM'), ('PM', 'PM')], label='Start AM/PM')
    end_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M', attrs={'placeholder': 'HH:MM'}),
        label='End Time'
    )
    end_meridiem = forms.ChoiceField(choices=[('AM', 'AM'), ('PM', 'PM')], label='End AM/PM')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError("End time must be after start time.")
