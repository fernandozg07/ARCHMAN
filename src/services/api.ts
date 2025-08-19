export interface Bill {
  id: number;
  status: string;
  fornecedor: string;
  period_start: string;
  period_end: string;
  consumo_kwh: number;
  valor_total: number;
  created_at: string;
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  address?: string;
  user_type: 'user' | 'admin' | 'officer';
}

class ApiService {
  private token: string | null = null;
  private users: (User & { password: string })[] = [];
  private currentUser: User | null = null;
  private bills: { [userId: number]: Bill[] } = {};

  constructor() {
    this.users = [
      {
        id: 1,
        email: 'admin@admin.com',
        first_name: 'Admin',
        last_name: 'Sistema',
        phone: '',
        address: '',
        user_type: 'admin',
        password: 'admin123'
      },
      {
        id: 2,
        email: 'user@user.com',
        first_name: 'Usuário',
        last_name: 'Comum',
        phone: '',
        address: '',
        user_type: 'user',
        password: 'user123'
      },
      {
        id: 3,
        email: 'officer@officer.com',
        first_name: 'Officer',
        last_name: 'Sistema',
        phone: '',
        address: '',
        user_type: 'officer',
        password: 'officer123'
      }
    ];
  }

  setToken(token: string) {
    this.token = token;
  }

  getToken(): string | null {
    return this.token;
  }

  logout() {
    this.token = null;
    this.currentUser = null;
  }

  async login(email: string, password: string): Promise<{ access: string; refresh: string }> {
    const user = this.users.find(u => u.email === email && u.password === password);
    
    if (user) {
      const tokens = {
        access: 'token-' + Date.now(),
        refresh: 'refresh-' + Date.now()
      };
      this.setToken(tokens.access);
      const { password: _, ...userWithoutPassword } = user;
      this.currentUser = userWithoutPassword;
      return tokens;
    } else {
      throw new Error('Email ou senha incorretos');
    }
  }

  async register(data: { email: string; password: string; first_name: string; last_name: string; phone?: string; address?: string; user_type?: 'user' | 'admin' | 'officer' }): Promise<User> {
    if (this.users.find(u => u.email === data.email)) {
      throw new Error('Email já cadastrado');
    }

    const newUser = {
      id: Date.now(),
      email: data.email,
      first_name: data.first_name,
      last_name: data.last_name,
      phone: data.phone || '',
      address: data.address || '',
      user_type: data.user_type || 'user',
      password: data.password
    };

    this.users.push(newUser);
    
    const { password, ...userWithoutPassword } = newUser;
    return userWithoutPassword;
  }

  async getBills(): Promise<Bill[]> {
    if (!this.currentUser) return [];
    return this.bills[this.currentUser.id] || [];
  }

  async saveBill(bill: Omit<Bill, 'id'>): Promise<Bill> {
    if (!this.currentUser) throw new Error('Usuário não logado');

    const newBill: Bill = {
      ...bill,
      id: Date.now(),
      created_at: new Date().toISOString()
    };

    if (!this.bills[this.currentUser.id]) {
      this.bills[this.currentUser.id] = [];
    }
    this.bills[this.currentUser.id].push(newBill);

    return newBill;
  }

  async getUser(): Promise<User> {
    if (this.currentUser) {
      return this.currentUser;
    }
    throw new Error('Usuário não encontrado');
  }

  getUserData(): User | null {
    return this.currentUser;
  }

  saveUserData(user: User) {
    this.currentUser = user;
  }

  async getAnalytics(): Promise<any> {
    const bills = await this.getBills();
    
    const totalBills = bills.length;
    const totalConsumption = bills.reduce((sum, bill) => sum + (bill.consumo_kwh || 0), 0);
    const totalCost = bills.reduce((sum, bill) => sum + (bill.valor_total || 0), 0);
    const avgCostKwh = totalConsumption > 0 ? totalCost / totalConsumption : 0;

    return {
      total_bills: totalBills,
      total_consumption: totalConsumption,
      total_cost: totalCost,
      avg_cost_kwh: avgCostKwh
    };
  }
}

export const apiService = new ApiService();