export type UserRole = 'founder' | 'talent' | 'mentor' | 'investor' | 'admin';

export interface User {
  id: string;
  email: string;
  role: UserRole;
  fullName?: string;
  avatarUrl?: string;
  isVerified?: boolean;
  createdAt: string;
}

export interface AuthSession {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
  role?: UserRole; // Used in mock mode so any email can test any role
}

export interface RegisterData {
  email: string;
  password: string;
  role: UserRole;
  fullName: string;
  agreedToTerms: boolean;
}
