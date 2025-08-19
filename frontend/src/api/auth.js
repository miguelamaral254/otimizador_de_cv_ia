import apiClient from './client'

export const authAPI = {
    login: async (email, password) => {
        const response = await apiClient.post('/auth/login', { email, password })
        return response.data
    },

    register: async (userData) => {
        const response = await apiClient.post('/auth/register', userData)
        return response.data
    },

    getProfile: async () => {
        const response = await apiClient.get('/auth/profile')
        return response.data
    },

    updateProfile: async (userData) => {
        const response = await apiClient.put('/auth/profile', userData)
        return response.data
    }
}
