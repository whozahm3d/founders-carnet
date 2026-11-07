import type { User, UserRole, LoginCredentials, RegisterData } from '@/types/auth';

const TOKEN_KEY = 'carnet_token';
const USER_KEY = 'carnet_user';

const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK !== 'false';
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export interface AuthResponse {
  token: string;
  user: User;
}

const isBrowser = () => typeof window !== 'undefined';

/** Session persistence. Safe to call during SSR (returns null / no-ops). */
export const authStorage = {
  getToken(): string | null {
    if (!isBrowser()) return null;
    try {
      return window.localStorage.getItem(TOKEN_KEY);
    } catch {
      return null;
    }
  },
  setToken(token: string): void {
    if (!isBrowser()) return;
    try {
      window.localStorage.setItem(TOKEN_KEY, token);
    } catch {
      /* storage unavailable */
    }
  },
  getUser(): User | null {
    if (!isBrowser()) return null;
    try {
      const raw = window.localStorage.getItem(USER_KEY);
      return raw ? (JSON.parse(raw) as User) : null;
    } catch {
      return null;
    }
  },
  setUser(user: User): void {
    if (!isBrowser()) return;
    try {
      window.localStorage.setItem(USER_KEY, JSON.stringify(user));
    } catch {
      /* storage unavailable */
    }
  },
  clear(): void {
    if (!isBrowser()) return;
    try {
      window.localStorage.removeItem(TOKEN_KEY);
      window.localStorage.removeItem(USER_KEY);
    } catch {
      /* storage unavailable */
    }
  },
};

function nameFromEmail(email: string): string {
  const local = email.split('@')[0] || 'User';
  return local
    .split(/[._-]+/)
    .filter(Boolean)
    .map((p) => p.charAt(0).toUpperCase() + p.slice(1))
    .join(' ');
}

function buildMockUser(email: string, role: UserRole, fullName?: string): User {
  return {
    id: `mock-${role}-${email.toLowerCase()}`,
    email,
    role,
    fullName: fullName || nameFromEmail(email),
    isVerified: true,
    createdAt: new Date().toISOString(),
  };
}

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function request<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    let message = 'Request failed. Please try again.';
    try {
      const data = await res.json();
      if (typeof data?.detail === 'string') message = data.detail;
      else if (typeof data?.message === 'string') message = data.message;
    } catch {
      /* non-JSON error body */
    }
    throw new Error(message);
  }
  return (await res.json()) as T;
}

export async function loginApi(credentials: LoginCredentials): Promise<AuthResponse> {
  if (USE_MOCK) {
    await delay(300);
    const role = credentials.role ?? 'founder';
    return {
      token: `mock-token-${role}-${Date.now()}`,
      user: buildMockUser(credentials.email, role),
    };
  }
  return request<AuthResponse>('/auth/login', {
    email: credentials.email,
    password: credentials.password,
  });
}

export async function registerApi(data: RegisterData): Promise<AuthResponse> {
  if (USE_MOCK) {
    await delay(400);
    if (!data.agreedToTerms) {
      throw new Error('You must agree to the terms to create an account.');
    }
    return {
      token: `mock-token-${data.role}-${Date.now()}`,
      user: buildMockUser(data.email, data.role, data.fullName),
    };
  }
  return request<AuthResponse>('/auth/register', data);
}
