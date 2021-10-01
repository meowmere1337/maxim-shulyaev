from django import forms
from .models import Expense, Category
from django.db.models import Sum


class ExpenseSearchForm(forms.ModelForm):
    GROPING = ('date', 'category', )
    grouping = forms.ChoiceField(choices=[('', '')] + list(zip(GROPING, GROPING)))
    #OPTIONS = (
        #("AUT", "Austria"),
        #("DEU", "Germany"),
        #("NLD", "Neitherlands"),
    #)
    #Countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          #choices=OPTIONS)
    #OPTIONS = ['a','b','c'] #table2
    #for x in Category.objects.all():
    #    OPTIONS.append(Category.objects.all().filter(id=x).annotate('name'))
    #category = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=OPTIONS)

    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all().select_related())

    #cate = forms.SelectMultiple()
    date_start = forms.DateField(label='Data start range')
    date_end = forms.DateField(label='Data end range')
    class Meta:
        model = Expense
        fields = ('name', )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].required = False

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []

class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(CategoryAddForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

