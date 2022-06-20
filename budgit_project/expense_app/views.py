from django.shortcuts import redirect, render
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import Expense
from users_app.models import User
from . import forms

# class ExpenseListView(generic.ListView):
#     model = models.Expense
#     form_class = forms.ExpenseForm

@login_required(redirect_field_name='index', login_url='/login')
def dashboard(request):
    # print(request.session['user_id'])
    current_user = User.objects.get(id=request.session['user_id'])
    data = Expense.objects.filter(user=current_user)
    context = {
        'user': current_user,
        'data': data,
        'total': Expense.get_total(current_user)
    }
    # print(context['data'])
    return render(request, 'dashboard.html', context)

def add_expense(request):
    context = {
        "page_name": 'Add an Expense',
        'categories': Expense.get_choices(),
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, "expense_form.html", context)

def create_expense(request):
    errors = Expense.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('expense_form')
    else:
        print(request.session['user_id'])
        Expense.objects.create(
            name=request.POST['name'],
            amount=int(request.POST['amount']),
            category=request.POST['category'],
            recurring=request.POST['recurring'],
            user = User.objects.get(id=request.session['user_id']),
            )
        return redirect('dashboard')

def edit_expense(request, id):
    context = {
        'page_name': 'Edit Expense',
        'exp': Expense.objects.get(id=id),
        'categories': Expense.get_choices(),
    }
    return render(request, 'expense_edit.html', context)