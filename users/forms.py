from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    # The frontend has "Full Name", so we add a field for it
    full_name = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'full_name',)

    def save(self, commit=True):
        user = super().save(commit=False)
        # Split "Full Name" into first and last name for the User model
        name_parts = self.cleaned_data['full_name'].split(' ', 1)
        user.first_name = name_parts[0]
        if len(name_parts) > 1:
            user.last_name = name_parts[1]

        if commit:
            user.save()
        return user