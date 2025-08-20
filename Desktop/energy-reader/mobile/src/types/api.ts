// API Types
export interface UserRegistrationData {
  email: string;
  password: string;
  name: string;
  phone?: string;
  cep?: string;
}

export interface CreateLeadData {
  name: string;
  email: string;
  phone: string;
  cep: string;
  provider_id: number;
  estimated_savings?: number;
  notes?: string;
}

export interface ProfileUpdateData {
  name?: string;
  phone?: string;
  cep?: string;
}

export interface BillUploadResponse {
  bill_id: number;
  status: string;
  message: string;
}

export interface AnalyticsSummaryParams {
  window?: '1m' | '3m' | '6m' | '1y';
}

export interface RenewableOptionsParams {
  cep: string;
  limit?: number;
}