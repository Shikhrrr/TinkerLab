from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, ProfileEditForm, BookingForm, ItemForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Admin access check
from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta
from django.core.mail import send_mail


def register(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})

def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        if user.is_superuser:
            return redirect('admin_dashboard')  # ✅ this handles it
        return redirect('home')
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def view_profile(request):
    return render(request, 'profile.html')

@login_required
def edit_profile(request):
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('view_profile')
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def home(request):
    query = request.GET.get('q', '')
    dept = request.GET.get('dept', '')
    
    items = Item.objects.all()

    if query:
        items = items.filter(title__icontains=query)
    if dept:
        items = items.filter(location__icontains=dept)

    return render(request, 'home.html', {
        'items': items,
        'query': query,
        'dept': dept,
    })


@login_required
def search_items(request):
    query = request.GET.get('q', '')
    department = request.GET.get('dept', '')
    items = Item.objects.all()

    if query:
        items = items.filter(Q(title__icontains=query) | Q(item_id__icontains=query))
    if department:
        items = items.filter(location__icontains=department)

    return render(request, 'search.html', {'items': items})

@login_required
def view_item(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    active_borrowers = BookingRequest.objects.filter(item=item, status='Approved')
    history = BookingRequest.objects.filter(item=item).exclude(status='Pending')
    return render(request, 'item_detail.html', {
        'item': item,
        'borrowers': active_borrowers,
        'history': history,
    })

@login_required
def book_item(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    form = BookingForm(request.POST or None)
    
    if form.is_valid():
        booking = form.save(commit=False)
        booking.item = item
        booking.student = request.user  # ✅ This is critical
        booking.save()
        return redirect('request_status')
    
    return render(request, 'book_item.html', {'form': form, 'item': item})


@login_required
def request_status(request):
    requests = BookingRequest.objects.filter(student=request.user).order_by('-request_date')
    return render(request, 'request_status.html', {'requests': requests})


def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    items = Item.objects.all().order_by('title')
    return render(request, 'admin/dashboard.html', {'items': items})

@user_passes_test(is_admin)
def add_item(request):
    form = ItemForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'admin/add_item.html', {'form': form})

@user_passes_test(is_admin)
def edit_item(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    form = ItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'admin/edit_item.html', {'form': form, 'item': item})

@user_passes_test(is_admin)
def delete_item(request, item_id):
    item = get_object_or_404(Item, item_id=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect('admin_dashboard')
    return render(request, 'admin/delete_item.html', {'item': item})

@user_passes_test(is_admin)
def pending_requests(request):
    requests = BookingRequest.objects.filter(status='Pending').order_by('-request_date')
    return render(request, 'admin/pending_requests.html', {'requests': requests})

@user_passes_test(is_admin)
def respond_request(request, req_id):
    req = get_object_or_404(BookingRequest, id=req_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        comment = request.POST.get('comment')
        req.status = status
        req.admin_comment = comment

        if status == 'Approved':
            req.item.available -= 1
            req.return_date = req.request_date.date() + timedelta(days=req.duration_days)
            req.item.save()

            # ✅ Send approval email
            if req.student.email:
                try:
                    send_mail(
                        subject='Your Equipment Request has been Approved',
                        message=f"""Hi {req.student.username},

Your request for "{req.item.title}" has been approved.

Return Date: {req.return_date}
Comment from admin: {comment or 'None'}

- TinkerLab Admin""",
                        from_email=None,
                        recipient_list=[req.student.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print("❌ Email sending failed:", e)

        req.save()
        return redirect('pending_requests')

    return render(request, 'admin/respond_request.html', {'req': req})

