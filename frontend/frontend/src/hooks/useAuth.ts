import { useState, useEffect } from 'react';

interface User {
    id: string;
    email: string;
    name: string;
}

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
}

export const useAuth = () => {
    const [authState, setAuthState] = useState<AuthState>({
        user: null,
        isAuthenticated: false,
        isLoading: true,
    });

    useEffect(() => {
        // Verificar se há um token válido no localStorage
        const token = localStorage.getItem('authToken');
        if (token) {
            // Aqui você faria uma chamada para validar o token
            // Por enquanto, vamos simular um usuário logado
            setAuthState({
                user: {
                    id: '1',
                    email: 'usuario@exemplo.com',
                    name: 'Usuário Exemplo',
                },
                isAuthenticated: true,
                isLoading: false,
            });
        } else {
            setAuthState({
                user: null,
                isAuthenticated: false,
                isLoading: false,
            });
        }
    }, []);

    const login = async (email: string) => {
        try {
            // Aqui você faria a chamada para a API de login
            // Por enquanto, vamos simular um login bem-sucedido
            const mockUser = {
                id: '1',
                email,
                name: 'Usuário Logado',
            };

            localStorage.setItem('authToken', 'mock-token');
            setAuthState({
                user: mockUser,
                isAuthenticated: true,
                isLoading: false,
            });

            return { success: true };
        } catch (error) {
            return { success: false, error: 'Falha na autenticação' };
        }
    };

    const logout = () => {
        localStorage.removeItem('authToken');
        setAuthState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
        });
    };

    return {
        ...authState,
        login,
        logout,
    };
};
