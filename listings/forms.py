from django import forms
from .models import Listing
from .models import Listing, Message


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ('owner', 'is_available', 'created_at', 'is_featured', 'saved_by')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your message here...'})
        }
        labels = {
            'content': ''  # Hides the "Content:" label
        }
