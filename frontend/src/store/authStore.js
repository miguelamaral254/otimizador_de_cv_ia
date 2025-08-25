import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export const useAuthStore = create(
    persist(
        (set, get) => ({
            // Estado
            user: null,
            token: null,
            isAuthenticated: false,

            // Ações
            login: (userData, token) => {
                set({
                    user: userData,
                    token: token,
                    isAuthenticated: true
                })
            },

            logout: () => {
                set({
                    user: null,
                    token: null,
                    isAuthenticated: false
                })
            },

            updateUser: (userData) => {
                set({ user: userData })
            },

            updateToken: (token) => {
                set({ token: token })
            },

            // Getters
            getToken: () => get().token,
            getUser: () => get().user,
            getIsAuthenticated: () => get().isAuthenticated
        }),
        {
            name: 'auth-storage', // nome da chave no localStorage
            partialize: (state) => ({
                user: state.user,
                token: state.token,
                isAuthenticated: state.isAuthenticated
            })
        }
    )
)
