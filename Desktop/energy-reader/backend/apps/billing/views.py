import os
from django.conf import settings
from django.utils import timezone
from django.utils._os import safe_join
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Bill
from .serializers import BillUploadSerializer, BillSerializer, BillListSerializer
from .filters import BillFilter
# from .tasks import process_bill_task


class BillUploadView(generics.CreateAPIView):
    """Upload bill file for processing"""
    serializer_class = BillUploadSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Upload de conta de energia",
        description="Faz upload de arquivo (PDF/JPG/PNG) para processamento OCR"
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bill = serializer.save()
        
        # Processar arquivo imediatamente
        try:
            from .simple_processor import SimpleProcessor
            processor = SimpleProcessor()
            
            # Processar arquivo
            bill.status = Bill.Status.PROCESSING
            bill.save()
            
            ocr_data = processor.process_bill(bill.raw_file.path)
            
            if 'error' not in ocr_data:
                # Atualizar bill com dados extraídos
                for key, value in ocr_data.items():
                    if hasattr(bill, key) and value:
                        setattr(bill, key, value)
                
                bill.status = Bill.Status.PROCESSED
                bill.processed_at = timezone.now()
            else:
                bill.status = Bill.Status.FAILED
                bill.error_message = ocr_data['error']
            
            bill.save()
            
        except Exception as e:
            bill.status = Bill.Status.FAILED
            bill.error_message = str(e)
            bill.save()
        
        return Response({
            'bill_id': bill.id,
            'status': bill.status,
            'message': 'Arquivo processado com sucesso!' if bill.status == 'PROCESSED' else 'Erro no processamento',
            'data': BillSerializer(bill).data
        }, status=status.HTTP_201_CREATED)


class BillListView(generics.ListAPIView):
    """List user's bills with filtering"""
    serializer_class = BillListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BillFilter
    
    def get_queryset(self):
        return Bill.objects.filter(user=self.request.user)
    
    @extend_schema(
        summary="Listar contas do usuário",
        description="Lista contas com filtros por data e status",
        parameters=[
            OpenApiParameter('from_date', str, description='Data inicial (YYYY-MM-DD)'),
            OpenApiParameter('to_date', str, description='Data final (YYYY-MM-DD)'),
            OpenApiParameter('status', str, description='Status da conta'),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BillDetailView(generics.RetrieveAPIView):
    """Get bill details"""
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Bill.objects.filter(user=self.request.user)
    
    @extend_schema(
        summary="Detalhes da conta",
        description="Retorna detalhes completos da conta incluindo dados extraídos"
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema(
    summary="Reprocessar conta",
    description="Reprocessa uma conta que falhou ou precisa ser atualizada"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reprocess_bill(request, pk):
    """Reprocess a bill"""
    try:
        bill = Bill.objects.get(pk=pk, user=request.user)
    except Bill.DoesNotExist:
        return Response(
            {'error': 'Conta não encontrada'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Reset status and trigger reprocessing
    bill.status = Bill.Status.UPLOADED
    bill.error_message = ''
    bill.save()
    
    # process_bill_task.delay(bill.id)
    
    return Response({
        'message': 'Reprocessamento iniciado',
        'status': bill.status
    })