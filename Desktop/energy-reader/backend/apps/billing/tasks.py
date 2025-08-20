import logging
from celery import shared_task
from django.utils import timezone
from .models import Bill
from .ocr.processor import OCRProcessor
from .parsers.enel_parser import EnelParser

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_bill_task(self, bill_id):
    """Process bill file with OCR and data extraction"""
    try:
        bill = Bill.objects.get(id=bill_id)
        bill.status = Bill.Status.PROCESSING
        bill.save()
        
        logger.info("Starting bill processing")
        
        # Initialize OCR processor
        ocr_processor = OCRProcessor()
        
        # Process file with safe path handling
        from django.core.files.storage import default_storage
        file_path = default_storage.path(bill.raw_file.name)
        ocr_result = ocr_processor.process_file(file_path)
        
        if not ocr_result.success:
            raise Exception(f"OCR failed: {ocr_result.error}")
        
        # Parse Enel data
        parser = EnelParser()
        parsed_data = parser.parse(ocr_result.text, ocr_result.barcodes)
        
        # Update bill with parsed data
        bill.parsed_json = parsed_data
        bill.status = Bill.Status.PROCESSED
        bill.processed_at = timezone.now()
        
        # Update extracted fields for easier querying
        _update_bill_fields(bill, parsed_data)
        
        bill.save()
        
        logger.info("Bill processed successfully")
        
        # Create analytics snapshot
        from apps.analytics.tasks import create_metric_snapshot_task
        create_metric_snapshot_task.delay(bill_id)
        
    except Bill.DoesNotExist:
        logger.error("Bill not found", extra={'bill_id': bill_id})
        
    except Exception as exc:
        logger.error("Error processing bill", extra={'bill_id': bill_id, 'error': str(exc)[:200]})
        
        try:
            bill = Bill.objects.get(id=bill_id)
            bill.status = Bill.Status.FAILED
            bill.error_message = str(exc)
            bill.save()
        except Bill.DoesNotExist:
            pass
        
        # Retry with exponential backoff
        if self.request.retries < self.max_retries:
            raise self.retry(countdown=60 * (2 ** self.request.retries))


def _update_bill_fields(bill, parsed_data):
    """Update bill fields from parsed data"""
    if not parsed_data:
        return
    
    # Basic info
    bill.fornecedor = parsed_data.get('fornecedor', '')
    bill.numero_cliente = parsed_data.get('numero_cliente', '')
    bill.unidade_consumidora = parsed_data.get('unidade_consumidora', '')
    bill.instalacao = parsed_data.get('instalacao', '')
    bill.endereco = parsed_data.get('endereco', '')
    
    # Dates
    periodo = parsed_data.get('periodo', {})
    if periodo.get('inicio'):
        bill.period_start = periodo['inicio']
    if periodo.get('fim'):
        bill.period_end = periodo['fim']
    
    if parsed_data.get('emissao'):
        bill.issue_date = parsed_data['emissao']
    if parsed_data.get('vencimento'):
        bill.due_date = parsed_data['vencimento']
    
    # Values
    if parsed_data.get('consumo_kwh'):
        bill.consumo_kwh = parsed_data['consumo_kwh']
    if parsed_data.get('tarifa_kwh'):
        bill.tarifa_kwh = parsed_data['tarifa_kwh']
    if parsed_data.get('valor_total'):
        bill.valor_total = parsed_data['valor_total']
    
    # Bandeira tarifária
    bandeira = parsed_data.get('bandeira_tarifaria', '').upper()
    if bandeira in [choice[0] for choice in Bill.BandeiraTarifaria.choices]:
        bill.bandeira_tarifaria = bandeira
    
    # Taxes
    impostos = parsed_data.get('impostos', {})
    if impostos.get('ICMS'):
        bill.icms = impostos['ICMS']
    if impostos.get('PIS'):
        bill.pis = impostos['PIS']
    if impostos.get('COFINS'):
        bill.cofins = impostos['COFINS']
    if impostos.get('outros'):
        bill.outros_impostos = impostos['outros']
    
    # Payment info
    if parsed_data.get('linha_digitavel'):
        bill.linha_digitavel = parsed_data['linha_digitavel']
    if parsed_data.get('codigo_de_barras'):
        bill.codigo_de_barras = parsed_data['codigo_de_barras']