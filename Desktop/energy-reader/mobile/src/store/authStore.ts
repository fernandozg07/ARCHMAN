import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  user_type: string;
  phone?: string;
  accessToken?: string;
  refreshToken?: string;
}

interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  login: (accessToken: string, refreshToken: string, user: User) => Promise<void>;
  logout: () => Promise<void>;
  loadStoredAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  isAuthenticated: false,
  user: null,
  accessToken: null,
  refreshToken: null,

  login: async (accessToken: string, refreshToken: string, user: User) => {
    try {
      await SecureStore.setItemAsync('access_token', accessToken);
      await SecureStore.setItemAsync('refresh_token', refreshToken);
      await SecureStore.setItemAsync('user', JSON.stringify(user));
      
      // Set token in API service
      const { api } = await import('../services/api');
      api.setToken(accessToken);
      
      set({
        isAuthenticated: true,
        user,
        accessToken,
        refreshToken,
      });
    } catch (error) {
      console.error('Error storing auth data:', error);
    }
  },

  logout: async () => {
    try {
      await SecureStore.deleteItemAsync('access_token');
      await SecureStore.deleteItemAsync('refresh_token');
      await SecureStore.deleteItemAsync('user');
      
      set({
        isAuthenticated: false,
        user: null,
        accessToken: null,
        refreshToken: null,
      });
    } catch (error) {
      console.error('Error clearing auth data:', error);
    }
  },

  loadStoredAuth: async () => {
    try {
      const accessToken = await SecureStore.getItemAsync('access_token');
      const refreshToken = await SecureStore.getItemAsync('refresh_token');
      const userString = await SecureStore.getItemAsync('user');
      
      if (accessToken && refreshToken && userString) {
        const user = JSON.parse(userString);
        
        // Set token in API service
        const { api } = await import('../services/api');
        api.setToken(accessToken);
        
        set({
          isAuthenticated: true,
          user,
          accessToken,
          refreshToken,
        });
      }
    } catch (error) {
      console.error('Error loading stored auth:', error);
    }
  },
}));