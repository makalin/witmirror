import { writable } from 'svelte/store';
import { browser } from '$app/environment';

export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  is_admin: boolean;
  created_at: string;
  last_login?: string;
  preferences: Record<string, any>;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

const createAuthStore = () => {
  const { subscribe, set, update } = writable<AuthState>({
    user: null,
    token: null,
    isAuthenticated: false,
    isLoading: true
  });

  return {
    subscribe,
    login: async (username: string, password: string) => {
      try {
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
        });

        if (!response.ok) {
          throw new Error('Login failed');
        }

        const data = await response.json();
        
        if (browser) {
          localStorage.setItem('token', data.access_token);
        }

        // Get user info
        const userResponse = await fetch('/api/auth/me', {
          headers: {
            'Authorization': `Bearer ${data.access_token}`,
          },
        });

        const user = await userResponse.json();

        update(state => ({
          ...state,
          user,
          token: data.access_token,
          isAuthenticated: true,
          isLoading: false
        }));

        return { success: true, user };
      } catch (error) {
        update(state => ({
          ...state,
          isLoading: false
        }));
        throw error;
      }
    },
    register: async (username: string, email: string, password: string) => {
      try {
        const response = await fetch('/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, email, password }),
        });

        if (!response.ok) {
          throw new Error('Registration failed');
        }

        const data = await response.json();
        
        if (browser) {
          localStorage.setItem('token', data.access_token);
        }

        update(state => ({
          ...state,
          token: data.access_token,
          isAuthenticated: true,
          isLoading: false
        }));

        return { success: true };
      } catch (error) {
        update(state => ({
          ...state,
          isLoading: false
        }));
        throw error;
      }
    },
    logout: () => {
      if (browser) {
        localStorage.removeItem('token');
      }
      set({
        user: null,
        token: null,
        isAuthenticated: false,
        isLoading: false
      });
    },
    checkAuth: async () => {
      if (!browser) {
        update(state => ({ ...state, isLoading: false }));
        return;
      }

      const token = localStorage.getItem('token');
      if (!token) {
        update(state => ({ ...state, isLoading: false }));
        return;
      }

      try {
        const response = await fetch('/api/auth/me', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error('Invalid token');
        }

        const user = await response.json();
        update(state => ({
          ...state,
          user,
          token,
          isAuthenticated: true,
          isLoading: false
        }));
      } catch (error) {
        if (browser) {
          localStorage.removeItem('token');
        }
        update(state => ({
          ...state,
          user: null,
          token: null,
          isAuthenticated: false,
          isLoading: false
        }));
      }
    },
    updatePreferences: async (preferences: Record<string, any>) => {
      try {
        const response = await fetch('/api/auth/preferences', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authStore.token}`,
          },
          body: JSON.stringify({ preferences }),
        });

        if (!response.ok) {
          throw new Error('Failed to update preferences');
        }

        update(state => ({
          ...state,
          user: state.user ? { ...state.user, preferences } : null
        }));
      } catch (error) {
        throw error;
      }
    }
  };
};

export const authStore = createAuthStore();
