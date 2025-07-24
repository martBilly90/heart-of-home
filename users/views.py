from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from listings.models import Listing
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have been registered successfully!')
            return redirect('home')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


@login_required
def profile_view(request):
    # Get listings created by the current user
    my_listings = Listing.objects.filter(owner=request.user)

    # Get listings saved by the current user
    # This works because of the 'saved_by' ManyToManyField in your Listing model
    saved_listings = request.user.saved_listings.all()

    context = {
        'my_listings': my_listings,
        'saved_listings': saved_listings,
    }
    return render(request, 'users/profile.html', context)
