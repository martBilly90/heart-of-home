# listings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.db.models import Q
from .models import Listing, Agent
from .forms import ListingForm, MessageForm


def all_listings_view(request):
    query = request.GET.get('q', '')
    listings = Listing.objects.filter(is_available=True).order_by('-created_at')
    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query)
        ).distinct()
    context = {'listings': listings, 'query': query}
    return render(request, 'listings/all_listings.html', context)


def listing_detail_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    is_saved = False
    if request.user.is_authenticated:
        if request.user in listing.saved_by.all():
            is_saved = True
    context = {'listing': listing, 'is_saved': is_saved}
    return render(request, 'listings/listing_detail.html', context)


def agents_view(request):
    agents = Agent.objects.all()
    context = {'agents': agents}
    return render(request, 'listings/agents.html', context)


@login_required
def create_listing_view(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect('listing-detail', pk=listing.pk)
    else:
        form = ListingForm()
    context = {'form': form}
    return render(request, 'listings/create_listing.html', context)


@login_required
def edit_listing_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.owner != request.user:
        return HttpResponseForbidden("You do not have permission to edit this listing.")
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listing-detail', pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    context = {'form': form, 'listing': listing}
    return render(request, 'listings/edit_listing.html', context)


@login_required
def delete_listing_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if listing.owner != request.user:
        return HttpResponseForbidden("You do not have permission to delete this listing.")
    if request.method == 'POST':
        listing_title = listing.title
        listing.delete()
        messages.success(request, f'Listing "{listing_title}" has been deleted.')
        return redirect('profile')
    context = {'listing': listing}
    return render(request, 'listings/listing_delete_confirm.html', context)


@login_required
def toggle_save_listing_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    user = request.user
    if request.method == 'POST':
        if user in listing.saved_by.all():
            listing.saved_by.remove(user)
        else:
            listing.saved_by.add(user)
        return redirect('listing-detail', pk=listing.pk)
    return redirect('listing-detail', pk=listing.pk)


# 👇 This is the function that was missing
@login_required
def send_message_view(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)
    if listing.owner == request.user:
        messages.error(request, "You cannot send a message to yourself.")
        return redirect('listing-detail', pk=listing_pk)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.listing = listing
            message.sender = request.user
            message.recipient = listing.owner
            message.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('listing-detail', pk=listing_pk)
    else:
        form = MessageForm()
    context = {'form': form, 'listing': listing}
    return render(request, 'listings/send_message.html', context)