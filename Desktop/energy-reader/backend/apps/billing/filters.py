import django_filters
from .models import Bill


class BillFilter(django_filters.FilterSet):
    """Filters for Bill model"""
    
    from_date = django_filters.DateFilter(field_name='period_start', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='period_end', lookup_expr='lte')
    status = django_filters.ChoiceFilter(choices=Bill.Status.choices)
    fornecedor = django_filters.CharFilter(lookup_expr='icontains')
    bandeira = django_filters.ChoiceFilter(
        field_name='bandeira_tarifaria',
        choices=Bill.BandeiraTarifaria.choices
    )
    
    class Meta:
        model = Bill
        fields = ['from_date', 'to_date', 'status', 'fornecedor', 'bandeira']