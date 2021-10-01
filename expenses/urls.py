from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import path, reverse_lazy
from .models import Expense, Category
from . import views
from .views import ExpenseListView

urlpatterns = [
    path('expense/list/',
         ExpenseListView.as_view(),
         name='expense-list'),

    path('expense/create/',
         CreateView.as_view(
             model=Expense,
             fields='__all__',
             success_url=reverse_lazy('expenses:expense-list')
         ),
         name='expense-create'),

    path('expense/<int:pk>/edit/',
         UpdateView.as_view(
             model=Expense,
             fields='__all__',
             success_url=reverse_lazy('expenses:expense-list')
         ),
         name='expense-edit'),

    path('expense/<int:pk>/delete/',
         DeleteView.as_view(
             model=Expense,
             success_url=reverse_lazy('expenses:expense-list')
         ),
         name='expense-delete'),

    path('category/list/', views.category_list, name='category-list'),

    path('category/add', views.category_add, name='category-add'),

    path('category/edit/<category_id>/', views.category_edit, name='category-edit'),

    #path('category/<uid>/del', views.category_del, name='category-delete'),

    # path('category/create/',
    #      CreateView.as_view(
    #          model=Expense,
    #          fields='__all__',
    #          success_url=reverse_lazy('expenses:category-list')
    #      ),
    #      name='category-create'),

    # path('category/<int:pk>/edit/',
    #      UpdateView.as_view(
    #          model=Expense,
    #          fields='__all__',
    #          success_url=reverse_lazy('expenses:category-list')
    #      ),
    #      name='expense-edit'),
    path('category/<int:pk>/delete/',
         DeleteView.as_view(
             model=Category,
             success_url=reverse_lazy('expenses:category-list')
         ),
         name='category-delete'),
]
