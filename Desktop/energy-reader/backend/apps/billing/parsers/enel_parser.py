import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class EnelParser:
    """Parser for Enel energy bills"""
    
    def __init__(self):
        self.patterns = self._init_patterns()
    
    def _init_patterns(self) -> Dict[str, re.Pattern]:
        """Initialize regex patterns for Enel bill parsing"""
        return {
            # Customer info
            'numero_cliente': re.compile(r'(?:Número do Cliente|Cliente)[:\s]*(\d+)', re.IGNORECASE),
            'unidade_consumidora': re.compile(r'(?:Unidade Consumidora|UC)[:\s]*(\d+)', re.IGNORECASE),
            'instalacao': re.compile(r'(?:Instalação|Instalacao)[:\s]*(\d+)', re.IGNORECASE),
            
            # Dates
            'periodo_inicio': re.compile(r'(?:Período|Periodo)[:\s]*(\d{2}/\d{2}/\d{4})', re.IGNORECASE),
            'periodo_fim': re.compile(r'(?:até|a)[:\s]*(\d{2}/\d{2}/\d{4})', re.IGNORECASE),
            'vencimento': re.compile(r'(?:Vencimento|Data de Vencimento)[:\s]*(\d{2}/\d{2}/\d{4})', re.IGNORECASE),
            'emissao': re.compile(r'(?:Emissão|Data de Emissão)[:\s]*(\d{2}/\d{2}/\d{4})', re.IGNORECASE),
            
            # Consumption
            'consumo_kwh': re.compile(r'(?:Consumo|kWh)[:\s]*(\d+(?:,\d+)?)', re.IGNORECASE),
            'leitura_anterior': re.compile(r'(?:Leitura Anterior)[:\s]*(\d+)', re.IGNORECASE),
            'leitura_atual': re.compile(r'(?:Leitura Atual)[:\s]*(\d+)', re.IGNORECASE),
            
            # Tariff
            'tarifa_kwh': re.compile(r'(?:Tarifa|R\$/kWh)[:\s]*R?\$?\s*(\d+,\d+)', re.IGNORECASE),
            'bandeira_tarifaria': re.compile(r'(?:Bandeira)[:\s]*(Verde|Amarela|Vermelha|Escassez Hídrica)', re.IGNORECASE),
            
            # Values
            'valor_total': re.compile(r'(?:Total a Pagar|Valor Total)[:\s]*R\$\s*(\d+,\d+)', re.IGNORECASE),
            'icms': re.compile(r'ICMS[:\s]*R\$\s*(\d+,\d+)', re.IGNORECASE),
            'pis': re.compile(r'PIS[:\s]*R\$\s*(\d+,\d+)', re.IGNORECASE),
            'cofins': re.compile(r'COFINS[:\s]*R\$\s*(\d+,\d+)', re.IGNORECASE),
            
            # Payment
            'linha_digitavel': re.compile(r'(\d{5}\.\d{5}\s\d{5}\.\d{6}\s\d{5}\.\d{6}\s\d\s\d{14})', re.IGNORECASE),
            'codigo_barras': re.compile(r'(\d{44})', re.IGNORECASE),
            
            # Address
            'endereco': re.compile(r'(?:Endereço|Endereco)[:\s]*([^\n]+)', re.IGNORECASE),
        }
    
    def parse(self, text: str, barcodes: List[dict] = None) -> Dict[str, Any]:
        """Parse Enel bill text and return structured data"""
        if not text:
            return {}
        
        # Clean text
        cleaned_text = self._clean_text(text)
        
        # Extract data
        parsed_data = {
            "fornecedor": "Enel",
            "numero_cliente": self._extract_field(cleaned_text, 'numero_cliente'),
            "unidade_consumidora": self._extract_field(cleaned_text, 'unidade_consumidora'),
            "instalacao": self._extract_field(cleaned_text, 'instalacao'),
            "endereco": self._extract_field(cleaned_text, 'endereco'),
            "periodo": self._extract_period(cleaned_text),
            "emissao": self._extract_date(cleaned_text, 'emissao'),
            "vencimento": self._extract_date(cleaned_text, 'vencimento'),
            "consumo_kwh": self._extract_consumption(cleaned_text),
            "bandeira_tarifaria": self._extract_bandeira(cleaned_text),
            "tarifa_kwh": self._extract_decimal(cleaned_text, 'tarifa_kwh'),
            "impostos": self._extract_taxes(cleaned_text),
            "valor_total": self._extract_decimal(cleaned_text, 'valor_total'),
            "linha_digitavel": self._extract_payment_line(cleaned_text, barcodes),
            "codigo_de_barras": self._extract_barcode(cleaned_text, barcodes)
        }
        
        # Validate and normalize
        parsed_data = self._validate_data(parsed_data)
        
        return parsed_data
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might interfere
        text = re.sub(r'[^\w\s.,;:!?()[\]{}/-]', ' ', text)
        return text.strip()
    
    def _extract_field(self, text: str, field: str) -> Optional[str]:
        """Extract a field using regex pattern"""
        pattern = self.patterns.get(field)
        if not pattern:
            return None
        
        match = pattern.search(text)
        return match.group(1).strip() if match else None
    
    def _extract_date(self, text: str, field: str) -> Optional[str]:
        """Extract and normalize date"""
        date_str = self._extract_field(text, field)
        if not date_str:
            return None
        
        try:
            # Convert DD/MM/YYYY to YYYY-MM-DD
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            logger.warning(f"Invalid date format: {date_str}")
            return None
    
    def _extract_period(self, text: str) -> Dict[str, Optional[str]]:
        """Extract billing period"""
        inicio = self._extract_date(text, 'periodo_inicio')
        fim = self._extract_date(text, 'periodo_fim')
        
        return {
            "inicio": inicio,
            "fim": fim
        }
    
    def _extract_consumption(self, text: str) -> Optional[float]:
        """Extract consumption in kWh"""
        # Try direct consumption pattern
        consumo_str = self._extract_field(text, 'consumo_kwh')
        if consumo_str:
            return self._parse_decimal(consumo_str)
        
        # Try calculating from readings
        leitura_anterior = self._extract_field(text, 'leitura_anterior')
        leitura_atual = self._extract_field(text, 'leitura_atual')
        
        if leitura_anterior and leitura_atual:
            try:
                anterior = int(leitura_anterior)
                atual = int(leitura_atual)
                return float(atual - anterior)
            except ValueError:
                pass
        
        return None
    
    def _extract_bandeira(self, text: str) -> str:
        """Extract tariff flag"""
        bandeira = self._extract_field(text, 'bandeira_tarifaria')
        if not bandeira:
            return "DESCONHECIDA"
        
        bandeira_upper = bandeira.upper()
        bandeira_map = {
            'VERDE': 'VERDE',
            'AMARELA': 'AMARELA',
            'VERMELHA': 'VERMELHA',
            'ESCASSEZ HÍDRICA': 'ESCASSEZ_HIDRICA',
            'ESCASSEZ HIDRICA': 'ESCASSEZ_HIDRICA'
        }
        
        return bandeira_map.get(bandeira_upper, 'DESCONHECIDA')
    
    def _extract_decimal(self, text: str, field: str) -> Optional[float]:
        """Extract decimal value"""
        value_str = self._extract_field(text, field)
        return self._parse_decimal(value_str) if value_str else None
    
    def _parse_decimal(self, value_str: str) -> Optional[float]:
        """Parse Brazilian decimal format (1.234,56)"""
        if not value_str:
            return None
        
        try:
            # Remove currency symbols and spaces
            cleaned = re.sub(r'[R$\s]', '', value_str)
            # Convert Brazilian format to standard decimal
            if ',' in cleaned:
                # Handle thousands separator
                if cleaned.count(',') == 1 and '.' in cleaned:
                    # Format: 1.234,56
                    cleaned = cleaned.replace('.', '').replace(',', '.')
                else:
                    # Format: 1234,56
                    cleaned = cleaned.replace(',', '.')
            
            return float(cleaned)
        except (ValueError, InvalidOperation):
            logger.warning(f"Could not parse decimal: {value_str}")
            return None
    
    def _extract_taxes(self, text: str) -> Dict[str, Optional[float]]:
        """Extract tax values"""
        return {
            "ICMS": self._extract_decimal(text, 'icms'),
            "PIS": self._extract_decimal(text, 'pis'),
            "COFINS": self._extract_decimal(text, 'cofins'),
            "outros": None  # Could be calculated as difference
        }
    
    def _extract_payment_line(self, text: str, barcodes: List[dict] = None) -> Optional[str]:
        """Extract payment line (linha digitável)"""
        # Try from text first
        linha = self._extract_field(text, 'linha_digitavel')
        if linha:
            return linha
        
        # Try from barcodes
        if barcodes:
            for barcode in barcodes:
                if barcode.get('type') == 'CODE128' and len(barcode.get('data', '')) >= 44:
                    return barcode['data']
        
        return None
    
    def _extract_barcode(self, text: str, barcodes: List[dict] = None) -> Optional[str]:
        """Extract barcode"""
        # Try from text first
        codigo = self._extract_field(text, 'codigo_barras')
        if codigo:
            return codigo
        
        # Try from barcodes
        if barcodes:
            for barcode in barcodes:
                data = barcode.get('data', '')
                if len(data) == 44 and data.isdigit():
                    return data
        
        return None
    
    def _validate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and clean parsed data"""
        # Ensure required fields are not empty strings
        for key, value in data.items():
            if value == '':
                data[key] = None
        
        # Validate date ranges
        periodo = data.get('periodo', {})
        if periodo.get('inicio') and periodo.get('fim'):
            try:
                inicio = datetime.strptime(periodo['inicio'], '%Y-%m-%d')
                fim = datetime.strptime(periodo['fim'], '%Y-%m-%d')
                if inicio > fim:
                    logger.warning("Invalid period: start date after end date")
                    data['periodo'] = {"inicio": None, "fim": None}
            except ValueError:
                pass
        
        # Validate consumption is positive
        if data.get('consumo_kwh') and data['consumo_kwh'] < 0:
            logger.warning("Negative consumption detected")
            data['consumo_kwh'] = None
        
        # Validate total taxes don't exceed total value
        impostos = data.get('impostos', {})
        valor_total = data.get('valor_total')
        if valor_total and impostos:
            total_impostos = sum(v for v in impostos.values() if v is not None)
            if total_impostos > valor_total:
                logger.warning("Total taxes exceed total value")
        
        return data