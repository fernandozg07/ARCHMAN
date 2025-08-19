import { create } from 'zustand';
import { Bill, User, apiService } from '../services/api';

interface AppState {
  // User
  user: User | null;
  isLoadingUser: boolean;
  
  // Bills
  bills: Bill[];
  isLoadingBills: boolean;
  
  // Auth
  isAuthenticated: boolean;
  
  // Actions
  loadUser: () => Promise<void>;
  loadBills: () => Promise<void>;
  addBill: (bill: Bill) => void;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  
  // UI State
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const useAppStore = create<AppState>((set, get) => ({
  // Initial state
  user: null,
  isLoadingUser: false,
  bills: [],
  isLoadingBills: false,
  isAuthenticated: false,
  activeTab: 'Home',

  // Actions
  loadUser: async () => {
    set({ isLoadingUser: true });
    try {
      const user = await apiService.getUser();
      set({ user, isLoadingUser: false });
    } catch (error) {
      console.error('Failed to load user:', error);
      set({ isLoadingUser: false });
    }
  },

  loadBills: async () => {
    set({ isLoadingBills: true });
    try {
      const bills = await apiService.getBills();
      set({ bills, isLoadingBills: false });
    } catch (error) {
      console.error('Failed to load bills:', error);
      set({ isLoadingBills: false });
    }
  },

  addBill: (bill: Bill) => {
    const { bills } = get();
    set({ bills: [bill, ...bills] });
  },

  login: async (email: string, password: string) => {
    set({ isLoadingUser: true });
    try {
      await apiService.login(email, password);
      const user = apiService.getUserData();
      if (user) {
        set({ user, isAuthenticated: true, isLoadingUser: false });
      } else {
        throw new Error('Erro ao carregar dados do usuário');
      }
    } catch (error) {
      console.error('Login failed:', error);
      set({ isLoadingUser: false, isAuthenticated: false, user: null });
      throw error;
    }
  },

  logout: () => {
    apiService.logout();
    set({ user: null, isAuthenticated: false, bills: [] });
  },

  setActiveTab: (tab: string) => {
    set({ activeTab: tab });
  },
}));