import apiClient from './client';

/**
 * Serviço para buscar métricas e dados de progresso do usuário
 */
export const metricsService = {
  /**
   * Busca série temporal de métricas do usuário
   * @returns {Promise} Dados de progresso em série temporal
   */
  async getTimeSeriesMetrics() {
    try {
      const response = await apiClient.get('/api/metrics/time-series');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar métricas de progresso:', error);
      throw error;
    }
  },

  /**
   * Busca métricas filtradas por período e score
   * @param {Object} filters - Filtros de busca
   * @param {string} filters.start_date - Data de início (opcional)
   * @param {string} filters.end_date - Data de fim (opcional)
   * @param {number} filters.min_score - Score mínimo (opcional)
   * @param {number} filters.max_score - Score máximo (opcional)
   * @returns {Promise} Dados filtrados de progresso
   */
  async getFilteredMetrics(filters = {}) {
    try {
      const params = new URLSearchParams();
      
      if (filters.start_date) params.append('start_date', filters.start_date);
      if (filters.end_date) params.append('end_date', filters.end_date);
      if (filters.min_score !== undefined) params.append('min_score', filters.min_score);
      if (filters.max_score !== undefined) params.append('max_score', filters.max_score);

      const response = await apiClient.get(`/api/metrics/time-series/filtered?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar métricas filtradas:', error);
      throw error;
    }
  },

  /**
   * Busca estatísticas resumidas do usuário
   * @returns {Promise} Estatísticas resumidas
   */
  async getSummaryStats() {
    try {
      const response = await apiClient.get('/api/metrics/time-series');
      const data = response.data;
      
      return {
        totalVersions: data.total_versions,
        averageScore: data.average_score,
        bestScore: data.best_score,
        improvementRate: data.improvement_rate,
        lastAnalysisDate: data.time_series.length > 0 ? data.time_series[data.time_series.length - 1].timestamp : null
      };
    } catch (error) {
      console.error('Erro ao buscar estatísticas resumidas:', error);
      throw error;
    }
  }
};

export default metricsService;
