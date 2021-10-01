from django.shortcuts import render
from django.views.generic.list import ListView

from .forms import ExpenseSearchForm
from .models import Expense, Category
from .reports import summary_per_category, summary_per_year_month  # , summary_all
from django.db.models import Sum
from . import forms
from django.shortcuts import redirect


def category_list(request):
    category = Category.objects.select_related()
    amount = []
    for x in Category.objects.all():
        amount.append(Expense.objects.all().filter(category_id=x).aggregate(Sum('amount'))['amount__sum'])
    totalammont = Expense.objects.select_related().all()
    summary_all = totalammont.aggregate(Sum('amount'))['amount__sum']
    context = {
        'titlepage': 'test',
        'table': category,
        'table2': amount,
        'summary_all': summary_all,
    }
    # if request.method == "POST" and 'category-delete' in request.POST:
    #     uid = request.POST['id']
    #     category_del(request, uid)
    #     return redirect('category-delete', id=uid)
    # if 'af_del' in request.POST and request.POST['af_del']:
    #     #for_del.delete()
    #     a=1
    #     return redirect('../list')
    return render(request, 'category/category_list.html', context)


def category_add(request):
    if request.method == "POST":
        form = forms.CategoryAddForm(request.POST)
        if form.is_valid():
            form.save()
            if 'add' in request.POST and request.POST['add']:
                return redirect('../category/list')
            else:
                return redirect('../category/list')
    else:
        form = forms.CategoryAddForm()
    context = {
        'form': form,
    }
    return render(request, 'category/category_form.html', context)


def category_edit(request, category_id):
    category = Category.objects.get(pk=category_id)
    if request.method == "POST":
        form = forms.CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            send = form.save(commit=False)
            send.save()
            if 'addp' in request.POST and request.POST['addp']:
                return redirect('../../list')
            else:
                return redirect('../../list', category_id=form.save().id)
    else:
        form = forms.CategoryForm(instance=category)
    context = {
        'form': form,
    }
    return render(request, 'category/category_form.html', context)


# def category_del(request, uid):
#     for_del = Category.objects.get(id=uid)
#     x = Expense.objects.all().filter(category_id=uid).aggregate(Sum('amount'))['amount__sum']
#     context = {
#         'for_del': for_del,
#         'fx': x,
#     }
#     return render(request, 'category/category_confirm_delete.html', context)

class ExpenseListView(ListView):
    model = Expense
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list

        form = ExpenseSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            if name:
                queryset = queryset.filter(name__icontains=name)

            category = form.cleaned_data['category']
            if category:
                queryset = queryset.filter(category=category)

            grouping = form.cleaned_data['grouping']
            if grouping == 'data':
                queryset = queryset.order_by('date', '-pk')
            else:
                queryset = queryset.order_by('category', '-pk')

            date_start = form.cleaned_data['date_start']
            date_end = form.cleaned_data['date_end']
            if date_start and date_end:
                queryset = queryset.filter(date__gte=date_start, date__lte=date_end)

            totalammont = Expense.objects.select_related().all()
            #queryset = totalammont.aggregate(Sum('amount'))
            summary_all = totalammont.aggregate(Sum('amount'))['amount__sum']
            order_by = self.request.GET.get('order_by')
            if order_by and order_by in ['category', '-category']:
                queryset = queryset.order_by(order_by)

            # if (self.request.GET.get('order_by')):
            #     queryset = Expense.objects.all().order_by('-category')
            #     order_by = self.request.GET.get('order_by', 'defaultOrderField')
            #     if order_by == "-category":
            #         queryset = Expense.objects.all().order_by('category')

        return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_all=summary_all,
            summary_per_category=summary_per_category(queryset),
            summary_per_year_month=summary_per_year_month(queryset),
            **kwargs)
