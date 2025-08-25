import { create } from 'zustand';
import { persist } from 'zustand/middleware';

// Funções de API diretas para evitar dependência circular
const authAPI = {
    login: async (credentials) => {
        const formData = new FormData();
        // O backend espera username, mas vamos usar o email como username
        formData.append('username', credentials.email);
        formData.append('password', credentials.password);

        const response = await fetch('http://localhost:8000/api/auth/login', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            let errorMessage = 'Erro no login';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || errorMessage;
            } catch (e) {
                console.error('Erro ao parsear resposta de erro:', e);
            }
            throw new Error(errorMessage);
        }

        return response.json();
    },

    register: async (userData) => {
        const response = await fetch('http://localhost:8000/api/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        });

        if (!response.ok) {
            let errorMessage = 'Erro no registro';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || errorMessage;
            } catch (e) {
                console.error('Erro ao parsear resposta de erro:', e);
            }
            throw new Error(errorMessage);
        }

        return response.json();
    },

    getCurrentUser: async (token) => {
        const response = await fetch('http://localhost:8000/api/auth/me', {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            let errorMessage = 'Erro ao obter usuário';
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || errorMessage;
            } catch (e) {
                console.error('Erro ao parsear resposta de erro:', e);
            }
            throw new Error(errorMessage);
        }

        return response.json();
    },
};

const useAuthStore = create(
    persist(
        (set, get) => ({
            // Estado
            user: null,
            token: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,

            // Ações
            login: async (credentials) => {
                set({ isLoading: true, error: null });
                try {
                    const response = await authAPI.login(credentials);

                    // Obter dados do usuário
                    const userData = await authAPI.getCurrentUser(response.access_token);

                    set({
                        user: userData,
                        token: response.access_token,
                        isAuthenticated: true,
                        isLoading: false,
                        error: null
                    });

                    return { success: true };
                } catch (error) {
                    const errorMessage = error.message || 'Erro ao fazer login';
                    set({
                        isLoading: false,
                        error: errorMessage
                    });
                    return { success: false, error: errorMessage };
                }
            },

            register: async (userData) => {
                set({ isLoading: true, error: null });
                try {
                    // O backend espera username, então vamos usar o email como username
                    const registerData = {
                        email: userData.email,
                        username: userData.email, // Usar o email completo como username
                        password: userData.password
                    };

                    await authAPI.register(registerData);

                    // Fazer login automaticamente após o registro
                    return await get().login({
                        email: userData.email,
                        password: userData.password
                    });
                } catch (error) {
                    console.error('Erro no registro:', error);
                    const errorMessage = error.message || 'Erro ao criar conta';
                    set({
                        isLoading: false,
                        error: errorMessage
                    });
                    return { success: false, error: errorMessage };
                }
            },

            logout: () => {
                set({
                    user: null,
                    token: null,
                    isAuthenticated: false,
                    isLoading: false,
                    error: null
                });
            },

            updateUser: (userData) => {
                set({ user: userData });
            },

            updateToken: (token) => {
                set({ token });
            },

            clearError: () => {
                set({ error: null });
            },

            // Getters
            getToken: () => get().token,
            getUser: () => get().user,
            getIsAuthenticated: () => get().isAuthenticated,
            getIsLoading: () => get().isLoading,
            getError: () => get().error
        }),
        {
            name: 'auth-storage',
            partialize: (state) => ({
                user: state.user,
                token: state.token,
                isAuthenticated: state.isAuthenticated
            })
        }
    )
);

export { useAuthStore };
export default useAuthStore;
