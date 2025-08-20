const API_BASE_URL = 'http://localhost:8000/api';

interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    user_type: string;
  };
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}

class ApiService {
  private baseURL = API_BASE_URL;
  private token: string | null = null;

  setToken(token: string) {
    this.token = token;
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers: any = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Network error' }));
      throw new Error(error.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  private async get(endpoint: string) {
    return this.request(endpoint, { method: 'GET' });
  }

  private async post(endpoint: string, data: any) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  private async postFormData(endpoint: string, formData: FormData) {
    const url = `${this.baseURL}${endpoint}`;
    const headers: any = {};

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Network error' }));
      throw new Error(error.message || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Auth endpoints
  async login(username: string, password: string): Promise<LoginResponse> {
    return this.post('/auth/login/', { username, password });
  }

  async register(data: RegisterData) {
    return this.post('/auth/register/', data);
  }

  async getProfile() {
    return this.get('/auth/profile/');
  }

  async updateProfile(data: any) {
    return this.request('/auth/profile/', {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  // Bills endpoints
  async getBills() {
    return this.get('/bills/');
  }

  async uploadBill(formData: FormData) {
    return this.postFormData('/bills/upload/', formData);
  }

  // Analytics endpoints
  async getAnalyticsSummary() {
    return this.get('/analytics/summary/');
  }
}

export const api = new ApiService();