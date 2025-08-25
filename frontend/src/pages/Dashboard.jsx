import React, { useState, useEffect } from 'react';
import { metricsService } from '../api/metrics';
import ProgressChart from '../components/ProgressChart';
import { TrendingUp, TrendingDown, Target, Calendar, BarChart3, RefreshCw } from 'lucide-react';
import { mockProgressData, mockSummaryStats } from '../utils/mockData';

const Dashboard = () => {
  const [progressData, setProgressData] = useState([]);
  const [summaryStats, setSummaryStats] = useState({
    totalVersions: 0,
    averageScore: 0,
    bestScore: 0,
    improvementRate: 0,
    lastAnalysisDate: null
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  // Buscar dados de progresso
  const fetchProgressData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Tentar buscar dados reais do backend
      try {
        const [timeSeriesData, summaryData] = await Promise.all([
          metricsService.getTimeSeriesMetrics(),
          metricsService.getSummaryStats()
        ]);
        
        setProgressData(timeSeriesData.time_series || []);
        setSummaryStats(summaryData);
      } catch (backendError) {
        console.warn('Backend não disponível, usando dados de exemplo:', backendError);
        // Usar dados de exemplo se o backend não estiver disponível
        setProgressData(mockProgressData);
        setSummaryStats(mockSummaryStats);
      }
      
      setLastRefresh(new Date());
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      setError('Erro ao carregar dados de progresso. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  // Carregar dados ao montar o componente
  useEffect(() => {
    fetchProgressData();
  }, []);

  // Função para atualizar dados (chamada após novo upload)
  const refreshData = () => {
    fetchProgressData();
  };

  // Função para formatar taxa de melhoria
  const formatImprovementRate = (rate) => {
    if (rate === 0) return '0%';
    const sign = rate > 0 ? '+' : '';
    return `${sign}${rate.toFixed(1)}%`;
  };

  // Função para obter cor baseada no score
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <RefreshCw className="animate-spin h-8 w-8 text-blue-600 mx-auto mb-4" />
            <p className="text-gray-600">Carregando dados de progresso...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <p className="text-red-800 mb-4">{error}</p>
          <button
            onClick={fetchProgressData}
            className="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 transition-colors"
          >
            Tentar Novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header do Dashboard */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard de Progresso</h1>
            <p className="text-gray-600 mt-2">
              Acompanhe a evolução do seu currículo ao longo do tempo
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={refreshData}
              className="flex items-center space-x-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Atualizar</span>
            </button>
            <div className="text-sm text-gray-500">
              Última atualização: {lastRefresh.toLocaleTimeString('pt-BR')}
            </div>
          </div>
        </div>
      </div>

      {/* Cards de Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BarChart3 className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total de Versões</p>
              <p className="text-2xl font-bold text-gray-900">{summaryStats.totalVersions}</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Target className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Score Médio</p>
              <p className={`text-2xl font-bold ${getScoreColor(summaryStats.averageScore)}`}>
                {summaryStats.averageScore.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-purple-500">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Melhor Score</p>
              <p className={`text-2xl font-bold ${getScoreColor(summaryStats.bestScore)}`}>
                {summaryStats.bestScore.toFixed(1)}%
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-orange-500">
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              {summaryStats.improvementRate >= 0 ? (
                <TrendingUp className="h-6 w-6 text-orange-600" />
              ) : (
                <TrendingDown className="h-6 w-6 text-orange-600" />
              )}
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Taxa de Melhoria</p>
              <p className={`text-2xl font-bold ${
                summaryStats.improvementRate >= 0 ? 'text-green-600' : 'text-red-600'
              }`}>
                {formatImprovementRate(summaryStats.improvementRate)}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Gráfico de Progresso */}
      <div className="mb-8">
        <ProgressChart 
          data={progressData} 
          title="Evolução das Métricas do Currículo"
        />
      </div>

      {/* Informações Adicionais */}
      {progressData.length > 0 && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Informações do Progresso</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Período de Análise</h4>
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <Calendar className="h-4 w-4" />
                <span>
                  {new Date(progressData[0].timestamp).toLocaleDateString('pt-BR')} - 
                  {new Date(progressData[progressData.length - 1].timestamp).toLocaleDateString('pt-BR')}
                </span>
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Status Geral</h4>
              <div className="flex items-center space-x-2">
                {summaryStats.improvementRate > 0 ? (
                  <TrendingUp className="h-4 w-4 text-green-600" />
                ) : summaryStats.improvementRate < 0 ? (
                  <TrendingDown className="h-4 w-4 text-red-600" />
                ) : (
                  <div className="h-4 w-4 bg-gray-400 rounded-full" />
                )}
                <span className={`text-sm font-medium ${
                  summaryStats.improvementRate > 0 ? 'text-green-600' : 
                  summaryStats.improvementRate < 0 ? 'text-red-600' : 'text-gray-600'
                }`}>
                  {summaryStats.improvementRate > 0 ? 'Em melhoria' : 
                   summaryStats.improvementRate < 0 ? 'Precisa de atenção' : 'Estável'}
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Mensagem quando não há dados */}
      {progressData.length === 0 && !loading && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-8 text-center">
          <BarChart3 className="h-16 w-16 text-blue-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-blue-900 mb-2">
            Comece sua jornada de otimização
          </h3>
          <p className="text-blue-700 mb-4">
            Faça upload do seu primeiro currículo para começar a acompanhar seu progresso
          </p>
          <p className="text-sm text-blue-600">
            O gráfico aparecerá aqui assim que você tiver análises para mostrar
          </p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
