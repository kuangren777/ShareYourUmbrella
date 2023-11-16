import django_filters
from .models import *
from .forms import *
from django_filters import DateFilter, CharFilter


class OrderFilter(django_filters.FilterSet):
    # start_date = DateFilter(field_name='borrow_time', lookup_expr='gte')
    # end_date = DateFilter(field_name='borrow_time', lookup_expr='lte')
    # note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Diary
        fields = [
            'umbrella_id',
            'lending_site_id',
            # 'borrow_time',
            'return_site_id',
            # 'back_time'
        ]

        labels = {
            'umbrella_id': '伞',
            'lending_site_id': '借出地点',
            # 'borrow_time': '借出时间',
            'return_site_id': '还伞地点',
            # 'back_time': '还伞时间',
        }

        # widgets = {
        #     'can_use': forms.CheckboxInput(attrs={'class': 'form-check'}),
        #     'umbrella': forms.Select(attrs={'class': 'form-select'}),
        #     'borrow_place': forms.Select(attrs={'class': 'form-select'}),
        #     'back_place': forms.Select(attrs={'class': 'form-select'}),
        # }
