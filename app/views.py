from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . import models

# Create your views here.

def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        fullname = request.POST.get('first_name') + request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        acc_type = request.POST.get('acc_type')
        user = User.objects.create_user(username=username)
        user.password = make_password(password)
        user.save()
        profile = models.Profile.objects.create(user=user, name=fullname, account_type=acc_type)
        return redirect('login')
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
        return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    if request.user.profile_user.account_type == 'client':
        bookings = models.Bookings.objects.filter(consumer=request.user.profile_user)
        return render(request, 'dashboard.html', {'bookings': bookings})
    else:
        bookings = models.Bookings.objects.filter(service__profile=request.user.profile_user)
    return render(request, 'dashboard.html', {'bookings': bookings})

def profile(request, user_id):
    profile = models.Profile.objects.get(id=user_id)
    services = models.Services.objects.filter(profile=profile)
    return render(request, 'profile.html', {'profile': profile, 'services': services})

def portfolio(request):
    return render(request, 'portfolio.html')

def services(request):
    services = models.Services.objects.all()
    return render(request, 'services.html', {'services': services})

def edit_profile(request):
    if request.method == 'POST':
        profile = request.user.profile_user
        profile.name = request.POST.get('name')
        profile.description = request.POST.get('description')
        profile.location = request.POST.get('location')
        profile.tagline = request.POST.get('tagline')
        profile.contact = request.POST.get('contact')
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('profile', user_id=request.user.profile_user.id)
    return redirect("profile", user_id=request.user.profile_user.id)

def create_service(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        costs = request.POST.get('price')
        category = request.POST.get('category')
        tags = request.POST.get('tags').split(',')
        cover_picture = request.FILES.get('cover_picture')

        added_name = request.POST.getlist('addon_name')
        added_rate = request.POST.getlist('addon_rate')


        service = models.Services.objects.create(
            profile=request.user.profile_user,
            title=title,
            description=description,
            costs=costs,
            category=category,
            cover_picture=cover_picture
        )
        for i in range(len(added_name)):
            extra = models.Event_Extras.objects.create(services=service, add_on=added_name[i], rate=added_rate[i])
            extra.save()
        for tag_name in tags:
            tag = models.Tags.objects.filter(name=tag_name.strip()).first()
            if not tag:
                tag = models.Tags.objects.create(name=tag_name.strip())
            service.tags.add(tag)
        service.save()
        if 'addon_name1' in request.POST:
            addon_name1 = request.POST.get('addon_name1')
            addon_rate1 = request.POST.get('addon_rate1')
            extra1 = models.Event_Extras.objects.create(service=service, add_on=addon_name1, rate=addon_rate1)
            extra1.save()
        if 'addon_name2' in request.POST:
            addon_name2 = request.POST.get('addon_name2')
            addon_rate2 = request.POST.get('addon_rate2')
            extra2 = models.Event_Extras.objects.create(service=service, add_on=addon_name2, rate=addon_rate2)
            extra2.save()
        if 'addon_name3' in request.POST:
            addon_name3 = request.POST.get('addon_name3')
            addon_rate3 = request.POST.get('addon_rate3')
            extra3 = models.Event_Extras.objects.create(service=service, add_on=addon_name3, rate=addon_rate3)
            extra3.save()
        if 'addon_name4' in request.POST:
            addon_name4 = request.POST.get('addon_name4')
            addon_rate4 = request.POST.get('addon_rate4')
            extra4 = models.Event_Extras.objects.create(service=service, add_on=addon_name4, rate=addon_rate4)
            extra4.save()
        if 'addon_name5' in request.POST:
            addon_name5 = request.POST.get('addon_name5')
            addon_rate5 = request.POST.get('addon_rate5')
            extra5 = models.Event_Extras.objects.create(service=service, add_on=addon_name5, rate=addon_rate5)
            extra5.save()
        return redirect('services')
    return render(request, 'create_service.html')

def package(request, package_id):
    # Retrieve the specific package based on its ID
    package = models.Services.objects.get(id=package_id)
    return render(request, 'packages.html', {'package': package})

@login_required(login_url='login')
def booking_proposal(request, service_id):
    if request.method == 'POST':
        guests = int(request.POST.get('guests') or 0)
        service = models.Services.objects.get(id=service_id)

        selected_extras = []
        total_charges = int(service.costs)

        for extra in service.service_extras.all():
            if extra.add_on in request.POST:
                selected_extras.append(extra)
                total_charges += int(extra.rate) * guests

        booking = models.Bookings.objects.create(
            date = request.POST.get('event_date'),
            service=service,
            consumer=request.user.profile_user,
            provider=service.profile,
            guests=guests,
            charges=total_charges,
            status='pending'
        )
        booking.extras.set(selected_extras)
        booking.save()
        return redirect('dashboard')
    return redirect('services')

# def booking_response(request, booking_id, response):
#     booking = models.Bookings.objects.get(id=booking_id)
#     if booking.provider == request.user.profile_user:
#         if response == 'accept':
#             booking.status = 'accepted'
#         elif response == 'reject':
#             booking.status = 'rejected'
#         elif response == 'complete':
#             booking.status = 'completed'
#         booking.save()
#     return redirect('dashboard')

def confirm_booking(request, booking_id):
    booking = models.Bookings.objects.get(id=booking_id)
    print("hello")
    booking.status = 'confirmed'
    booking.save()
    return redirect('dashboard')

# def contact(request):
#     return render(request, 'contact.html')

def reject_booking(request, booking_id):
    booking = models.Bookings.objects.get(id=booking_id)
    booking.status = 'rejected'
    booking.save()
    return redirect('dashboard')

def delete_service(request, service_id):
    service = models.Services.objects.get(id=service_id)
    if service.profile == request.user.profile_user:
        service.delete()
    return redirect('services')