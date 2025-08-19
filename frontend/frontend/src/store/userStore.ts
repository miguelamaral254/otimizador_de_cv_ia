import { create } from 'zustand';

interface User {
    id: string;
    email: string;
    name: string;
    createdAt: string;
}

interface UserState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;
}

interface UserActions {
    setUser: (user: User | null) => void;
    setLoading: (loading: boolean) => void;
    setError: (error: string | null) => void;
    login: (email: string, password: string) => Promise<boolean>;
    logout: () => void;
    clearError: () => void;
}

type UserStore = UserState & UserActions;

export const useUserStore = create<UserStore>((set) => ({
    // Estado inicial
    user: null,
    isAuthenticated: false,
    isLoading: false,
    error: null,

    // Ações
    setUser: (user) => set({
        user,
        isAuthenticated: !!user,
        error: null
    }),

    setLoading: (isLoading) => set({ isLoading }),

    setError: (error) => set({ error }),

    clearError: () => set({ error: null }),

    login: async (email) => {
        set({ isLoading: true, error: null });

        try {
            // Aqui você faria a chamada para a API
            // Por enquanto, vamos simular um login bem-sucedido
            await new Promise(resolve => setTimeout(resolve, 1000)); // Simular delay

            const mockUser: User = {
                id: '1',
                email,
                name: 'Usuário Logado',
                createdAt: new Date().toISOString(),
            };

            // Simular token
            localStorage.setItem('authToken', 'mock-token');

            set({
                user: mockUser,
                isAuthenticated: true,
                isLoading: false,
                error: null
            });

            return true;
        } catch (error) {
            set({
                error: 'Falha na autenticação',
                isLoading: false
            });
            return false;
        }
    },

    logout: () => {
        localStorage.removeItem('authToken');
        set({
            user: null,
            isAuthenticated: false,
            error: null
        });
    },
}));
