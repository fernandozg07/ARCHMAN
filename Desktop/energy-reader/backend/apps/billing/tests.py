import os
import tempfile
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Bill
from .parsers.enel_parser import EnelParser

User = get_user_model()


class BillModelTest(TestCase):
    """Test Bill model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password=os.environ.get('TEST_PASSWORD', 'temp_test_pass')
        )
    
    def test_bill_creation(self):
        """Test bill creation with file"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
            tmp_file.write(b'fake pdf content')
            tmp_file.flush()
            
            with open(tmp_file.name, 'rb') as f:
                bill = Bill.objects.create(
                    user=self.user,
                    raw_file=SimpleUploadedFile('test.pdf', f.read(), content_type='application/pdf')
                )
        
        self.assertEqual(bill.user, self.user)
        self.assertEqual(bill.status, Bill.Status.UPLOADED)
        self.assertTrue(bill.file_hash)
        
        # Cleanup
        os.unlink(tmp_file.name)
    
    def test_bill_properties(self):
        """Test bill calculated properties"""
        bill = Bill.objects.create(
            user=self.user,
            consumo_kwh=Decimal('150.00'),
            valor_total=Decimal('120.50'),
            icms=Decimal('15.00'),
            pis=Decimal('2.50'),
            cofins=Decimal('3.00')
        )
        
        self.assertEqual(bill.total_impostos, Decimal('20.50'))
        self.assertEqual(bill.custo_kwh_efetivo, Decimal('0.8033'))


class EnelParserTest(TestCase):
    """Test Enel parser"""
    
    def setUp(self):
        self.parser = EnelParser()
    
    def test_parse_basic_fields(self):
        """Test parsing basic fields from text"""
        text = """
        Enel Distribuição São Paulo
        Número do Cliente: 123456789
        Unidade Consumidora: 987654321
        Período: 15/01/2024 até 14/02/2024
        Vencimento: 25/02/2024
        Consumo: 150 kWh
        Bandeira Tarifária: Verde
        Valor Total: R$ 125,50
        """
        
        result = self.parser.parse(text)
        
        self.assertEqual(result['fornecedor'], 'Enel')
        self.assertEqual(result['numero_cliente'], '123456789')
        self.assertEqual(result['unidade_consumidora'], '987654321')
        self.assertEqual(result['periodo']['inicio'], '2024-01-15')
        self.assertEqual(result['periodo']['fim'], '2024-02-14')
        self.assertEqual(result['vencimento'], '2024-02-25')
        self.assertEqual(result['consumo_kwh'], 150.0)
        self.assertEqual(result['bandeira_tarifaria'], 'VERDE')
        self.assertEqual(result['valor_total'], 125.50)
    
    def test_parse_decimal_values(self):
        """Test parsing Brazilian decimal format"""
        self.assertEqual(self.parser._parse_decimal('1.234,56'), 1234.56)
        self.assertEqual(self.parser._parse_decimal('123,45'), 123.45)
        self.assertEqual(self.parser._parse_decimal('R$ 1.234,56'), 1234.56)
        self.assertIsNone(self.parser._parse_decimal('invalid'))
    
    def test_validate_data(self):
        """Test data validation"""
        data = {
            'consumo_kwh': -10,  # Invalid negative consumption
            'periodo': {'inicio': '2024-02-15', 'fim': '2024-01-15'},  # Invalid period
            'valor_total': 100.0,
            'impostos': {'ICMS': 150.0}  # Taxes exceed total
        }
        
        validated = self.parser._validate_data(data)
        
        # Should fix negative consumption
        self.assertIsNone(validated['consumo_kwh'])
        
        # Should fix invalid period
        self.assertIsNone(validated['periodo']['inicio'])
        self.assertIsNone(validated['periodo']['fim'])


class BillAPITest(APITestCase):
    """Test Bill API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password=os.environ.get('TEST_PASSWORD', 'temp_test_pass')
        )
        self.client.force_authenticate(user=self.user)
    
    def test_upload_bill(self):
        """Test bill upload endpoint"""
        # Create a fake PDF file
        pdf_content = b'%PDF-1.4 fake pdf content'
        uploaded_file = SimpleUploadedFile(
            'test_bill.pdf',
            pdf_content,
            content_type='application/pdf'
        )
        
        response = self.client.post('/api/bills/upload/', {
            'raw_file': uploaded_file
        }, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('bill_id', response.data)
        
        # Check bill was created
        bill = Bill.objects.get(id=response.data['bill_id'])
        self.assertEqual(bill.user, self.user)
        self.assertEqual(bill.status, Bill.Status.UPLOADED)
    
    def test_list_bills(self):
        """Test bill list endpoint"""
        # Create test bills
        Bill.objects.create(
            user=self.user,
            status=Bill.Status.PROCESSED,
            fornecedor='Enel',
            consumo_kwh=Decimal('150.00'),
            valor_total=Decimal('120.50')
        )
        
        response = self.client.get('/api/bills/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_bill_detail(self):
        """Test bill detail endpoint"""
        bill = Bill.objects.create(
            user=self.user,
            status=Bill.Status.PROCESSED,
            fornecedor='Enel',
            consumo_kwh=Decimal('150.00'),
            valor_total=Decimal('120.50')
        )
        
        response = self.client.get(f'/api/bills/{bill.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], bill.id)
        self.assertEqual(response.data['fornecedor'], 'Enel')
    
    def test_unauthorized_access(self):
        """Test unauthorized access to bills"""
        self.client.force_authenticate(user=None)
        
        response = self.client.get('/api/bills/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)