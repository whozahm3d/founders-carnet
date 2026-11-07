'use client';

import React, { createContext, useContext, useState } from 'react';
import { User, LoginCredentials, RegisterData } from '@/types/auth';
import { authStorage, loginApi, registerApi } from '@/lib/auth';

const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK !== 'false';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  isMockEnabled: boolean;
  login: (credentials: LoginCredentials) => Promise<User>;
  register: (data: RegisterData) => Promise<User>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(() => {
    const savedToken = authStorage.getToken();
    const savedUser = authStorage.getUser();
    return savedToken && savedUser ? savedUser : null;
  });

  const [token, setToken] = useState<string | null>(() => {
    const savedToken = authStorage.getToken();
    const savedUser = authStorage.getUser();
    return savedToken && savedUser ? savedToken : null;
  });
  const [isLoading, setIsLoading] = useState(false);

  const login = async (credentials: LoginCredentials): Promise<User> => {
    setIsLoading(true);
    try {
      // TODO: replace mock token with real auth once the backend is ready,
      // preferably an httpOnly cookie set by the backend instead of localStorage.
      const res = await loginApi(credentials);
      authStorage.setToken(res.token);
      authStorage.setUser(res.user);
      setToken(res.token);
      setUser(res.user);
      return res.user;
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (data: RegisterData): Promise<User> => {
    setIsLoading(true);
    try {
      // TODO: replace mock token with real auth once the backend is ready,
      // preferably an httpOnly cookie set by the backend instead of localStorage.
      const res = await registerApi(data);
      authStorage.setToken(res.token);
      authStorage.setUser(res.user);
      setToken(res.token);
      setUser(res.user);
      return res.user;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    authStorage.clear();
    setUser(null);
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        isMockEnabled: USE_MOCK,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
