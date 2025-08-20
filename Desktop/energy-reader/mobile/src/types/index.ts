// API Types
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  phone: string;
  cep: string;
  person_type: 'PF' | 'PJ';
  user_type: 'CLIENT' | 'ADMIN' | 'PARTNER';
  mfa_enabled: boolean;
  created_at: string;
  updated_at: string;
}

export interface Bill {
  id: number;
  status: 'UPLOADED' | 'PROCESSING' | 'PROCESSED' | 'FAILED';
  error_message: string;
  parsed_json: any;
  fornecedor: string;
  numero_cliente: string;
  unidade_consumidora: string;
  instalacao: string;
  endereco: string;
  period_start: string;
  period_end: string;
  issue_date: string;
  due_date: string;
  consumo_kwh: number;
  tarifa_kwh: number;
  valor_total: number;
  bandeira_tarifaria: 'VERDE' | 'AMARELA' | 'VERMELHA' | 'ESCASSEZ_HIDRICA' | 'DESCONHECIDA';
  icms: number;
  pis: number;
  cofins: number;
  outros_impostos: number;
  total_impostos: number;
  linha_digitavel: string;
  codigo_de_barras: string;
  custo_kwh_efetivo: number;
  created_at: string;
  updated_at: string;
  processed_at: string;
}

export interface AnalyticsSummary {
  current_kwh: number;
  current_cost: number;
  current_avg_kwh_cost: number;
  kwh_change_percent: number;
  cost_change_percent: number;
  projected_monthly_kwh: number;
  projected_monthly_cost: number;
  efficiency_score: number;
  potential_savings: number;
  trends: ConsumptionTrend[];
  anomalies_count: number;
  last_anomaly: string;
}

export interface ConsumptionTrend {
  id: number;
  year: number;
  month: number;
  total_kwh: number;
  total_cost: number;
  avg_daily_kwh: number;
  avg_cost_per_kwh: number;
  kwh_change_percent: number;
  cost_change_percent: number;
  is_anomaly: boolean;
  anomaly_reason: string;
  created_at: string;
}

export interface RenewableProvider {
  id: number;
  nome: string;
  descricao: string;
  site: string;
  contato_email: string;
  contato_telefone: string;
  modalidades: string[];
  is_verified: boolean;
}

export interface RenewableOffer {
  id: number;
  provider: RenewableProvider;
  regiao: string;
  modalidade: string;
  preco_estimado_kwh: number;
  economia_estimada_percent: number;
  sla_contato_horas: number;
  investimento_minimo: number;
  payback_meses: number;
  economia_mensal_estimada: number;
  economia_anual_estimada: number;
}

export interface RenewableOptions {
  cep: string;
  offers: RenewableOffer[];
  total_offers: number;
  consumo_medio_kwh: number;
  custo_medio_mensal: number;
}

export interface Lead {
  id: number;
  offer: RenewableOffer;
  status: 'NEW' | 'CONTACTED' | 'QUALIFIED' | 'PROPOSAL_SENT' | 'CLOSED_WON' | 'CLOSED_LOST';
  consumo_medio_kwh: number;
  custo_medio_mensal: number;
  melhor_horario_contato: string;
  observacoes: string;
  consentimento_lgpd: boolean;
  contatado_em: string;
  proposta_enviada_em: string;
  fechado_em: string;
  created_at: string;
  updated_at: string;
}

// Navigation Types
export type RootStackParamList = {
  Auth: undefined;
  Main: undefined;
};

export type AuthStackParamList = {
  Login: undefined;
  Register: undefined;
};

export type MainTabParamList = {
  Dashboard: undefined;
  Upload: undefined;
  History: undefined;
  Renewables: undefined;
  Profile: undefined;
};

export type DashboardStackParamList = {
  DashboardHome: undefined;
  BillDetail: { billId: number };
};

export type RenewablesStackParamList = {
  RenewablesHome: undefined;
  OfferDetail: { offerId: number };
  LeadForm: { offerId: number };
};

// Store Types
export interface AuthState {
  user: User | null;
  tokens: {
    access: string;
    refresh: string;
  } | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
  updateProfile: (userData: Partial<User>) => Promise<void>;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  phone: string;
  cep: string;
  person_type: 'PF' | 'PJ';
}

// API Response Types
export interface ApiResponse<T> {
  results: T[];
  count: number;
  next: string | null;
  previous: string | null;
}

export interface ApiError {
  message: string;
  status: number;
  data?: any;
}