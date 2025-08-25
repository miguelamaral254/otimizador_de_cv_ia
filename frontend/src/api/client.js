import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Criar instância do axios
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000, // 30 segundos
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor para adicionar token de autenticação
apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('auth-storage')
            ? JSON.parse(localStorage.getItem('auth-storage')).state.token
            : null;

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Interceptor para tratar erros de resposta
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expirado ou inválido
            const authStore = useAuthStore.getState();
            authStore.logout();
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// API de Autenticação
export const authAPI = {
    // Login
    login: async (credentials) => {
        const formData = new FormData();
        formData.append('username', credentials.email); // Backend usa username
        formData.append('password', credentials.password);

        const response = await apiClient.post('/api/auth/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
        return response.data;
    },

    // Registro
    register: async (userData) => {
        const response = await apiClient.post('/api/auth/register', userData);
        return response.data;
    },

    // Obter usuário atual
    getCurrentUser: async () => {
        const response = await apiClient.get('/api/auth/me');
        return response.data;
    },
};

// API de Currículos
export const curriculumAPI = {
    // Upload de currículo
    uploadCurriculum: async (file, jobDescription = null) => {
        const formData = new FormData();
        formData.append('file', file);
        if (jobDescription) {
            formData.append('job_description', jobDescription);
        }

        const response = await apiClient.post('/api/curriculum/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    // Listar currículos do usuário
    listCurricula: async () => {
        const response = await apiClient.get('/api/curriculum/list');
        return response.data;
    },

    // Obter currículo por ID
    getCurriculum: async (id) => {
        const response = await apiClient.get(`/api/curriculum/${id}`);
        return response.data;
    },

    // Analisar texto
    analyzeText: async (text) => {
        const response = await apiClient.post('/api/curriculum/analyze-text', { text });
        return response.data;
    },

    // Testar Agno
    testAgno: async () => {
        const response = await apiClient.get('/api/curriculum/test-agno');
        return response.data;
    },
};

// API de Métricas
export const metricsAPI = {
    // Obter série temporal de métricas
    getTimeSeriesMetrics: async () => {
        const response = await apiClient.get('/api/metrics/time-series');
        return response.data;
    },

    // Obter métricas filtradas
    getFilteredMetrics: async (filters = {}) => {
        const params = new URLSearchParams();
        Object.entries(filters).forEach(([key, value]) => {
            if (value !== null && value !== undefined) {
                params.append(key, value);
            }
        });

        const response = await apiClient.get(`/api/metrics/time-series/filtered?${params}`);
        return response.data;
    },
};

// API de Health Check
export const healthAPI = {
    checkHealth: async () => {
        const response = await apiClient.get('/health');
        return response.data;
    },
};

export default apiClient;
