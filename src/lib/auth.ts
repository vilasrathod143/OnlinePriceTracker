import Cookies from 'js-cookie';
import { authAPI } from './api';

export const auth = {
  login: async (email: string, password: string) => {
    try {
      const response = await authAPI.login(email, password);
      Cookies.set('token', response.access_token, { expires: 7 });
      // Trigger storage event for navbar update
      window.dispatchEvent(new Event('storage'));
      return { success: true, data: response };
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  },

  register: async (email: string, password: string) => {
    try {
      const response = await authAPI.register(email, password);
      Cookies.set('token', response.access_token, { expires: 7 });
      // Trigger storage event for navbar update
      window.dispatchEvent(new Event('storage'));
      return { success: true, data: response };
    } catch (error: any) {
      return { success: false, error: error.response?.data?.detail || 'Registration failed' };
    }
  },

  logout: () => {
    Cookies.remove('token');
    window.location.href = '/';
  },

  isAuthenticated: () => {
    return !!Cookies.get('token');
  },

  getToken: () => {
    return Cookies.get('token');
  },
};