import re
from decimal import Decimal
from datetime import datetime
from PIL import Image
import pytesseract

class OCRProcessor:
    def __init__(self):
        # Configurar tesseract se necessário
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass
    
    def process_bill(self, image_path):
        """Processa conta de energia e extrai dados"""
        try:
            # Abrir imagem
            image = Image.open(image_path)
            
            # Extrair texto com OCR
            text = pytesseract.image_to_string(image, lang='por')
            
            # Processar texto extraído
            return self.extract_data_from_text(text)
            
        except Exception as e:
            return {'error': str(e)}
    
    def extract_data_from_text(self, text):
        """Extrai dados estruturados do texto OCR"""
        data = {}
        
        # Fornecedor
        if 'ENEL' in text.upper():
            data['fornecedor'] = 'ENEL'
        elif 'CPFL' in text.upper():
            data['fornecedor'] = 'CPFL'
        elif 'CEMIG' in text.upper():
            data['fornecedor'] = 'CEMIG'
        else:
            data['fornecedor'] = 'Desconhecido'
        
        # Número do cliente
        cliente_match = re.search(r'(?:CLIENTE|CLIENT)[:\s]*(\d{8,12})', text, re.IGNORECASE)
        if cliente_match:
            data['numero_cliente'] = cliente_match.group(1)
        
        # Consumo kWh
        consumo_match = re.search(r'(\d{1,4})\s*kWh', text, re.IGNORECASE)
        if consumo_match:
            data['consumo_kwh'] = Decimal(consumo_match.group(1))
        
        # Valor total
        valor_matches = re.findall(r'R\$\s*(\d{1,4}[,\.]\d{2})', text)
        if valor_matches:
            # Pegar o maior valor (provavelmente o total)
            valores = [float(v.replace(',', '.')) for v in valor_matches]
            data['valor_total'] = Decimal(str(max(valores)))
        
        # Data de vencimento
        venc_match = re.search(r'(?:VENCIMENTO|VENC)[:\s]*(\d{2}[/\-]\d{2}[/\-]\d{4})', text, re.IGNORECASE)
        if venc_match:
            try:
                data['due_date'] = datetime.strptime(venc_match.group(1), '%d/%m/%Y').date()
            except:
                pass
        
        # Período
        periodo_match = re.search(r'(\d{2}[/\-]\d{2}[/\-]\d{4})\s*a\s*(\d{2}[/\-]\d{2}[/\-]\d{4})', text, re.IGNORECASE)
        if periodo_match:
            try:
                data['period_start'] = datetime.strptime(periodo_match.group(1), '%d/%m/%Y').date()
                data['period_end'] = datetime.strptime(periodo_match.group(2), '%d/%m/%Y').date()
            except:
                pass
        
        return data