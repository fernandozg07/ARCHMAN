from django.urls import path
from .views import BillUploadView, BillListView, BillDetailView, reprocess_bill

urlpatterns = [
    path('upload/', BillUploadView.as_view(), name='bill-upload'),
    path('', BillListView.as_view(), name='bill-list'),
    path('<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('<int:pk>/reprocess/', reprocess_bill, name='bill-reprocess'),
]