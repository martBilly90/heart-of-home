# pages/views.py
from django.shortcuts import render, redirect
from listings.models import Listing
from .forms import ContactForm


def home_view(request):
    # Get up to 6 listings that are marked as featured
    featured_listings = Listing.objects.filter(is_featured=True).order_by('-created_at')[:6]
    context = {
        'listings': featured_listings
    }
    return render(request, 'pages/home.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # You can add a success message here if you want
            return redirect('home')  # Redirect to homepage after submission
    else:
        form = ContactForm()

    context = {
        'form': form
    }
    return render(request, 'pages/contact.html', context)