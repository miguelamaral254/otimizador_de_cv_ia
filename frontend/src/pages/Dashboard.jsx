import React, { useState, useEffect } from 'react';
import { useAuthStore } from '../store/authStore';
import { curriculumAPI, metricsAPI } from '../api/client';

const Dashboard = () => {
  const { user } = useAuthStore();
  const [activeTab, setActiveTab] = useState('upload');
  const [uploadedCV, setUploadedCV] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [cvHistory, setCvHistory] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Carregar dados reais do backend
  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Carregar currículos do usuário
      const curricula = await curriculumAPI.listCurricula();

      // Se não há currículos, não é erro - apenas lista vazia
      if (curricula && curricula.length > 0) {
        setCvHistory(curricula.map((cv, index) => ({
          id: cv.id,
          version: `v${index + 1}.0`,
          date: new Date(cv.upload_date).toLocaleDateString('pt-BR'),
          filename: cv.filename,
          file_path: cv.file_path
        })));
      } else {
        // Usuário ainda não fez uploads - não é erro
        setCvHistory([]);
      }

      // Carregar métricas
      try {
        const metricsData = await metricsAPI.getTimeSeriesMetrics();
        setMetrics(metricsData);
      } catch (metricsErr) {
        // Se não há métricas, não é erro crítico
        console.log('Usuário ainda não tem métricas:', metricsErr.message);
        setMetrics([]);
      }
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
      // Só mostra erro se for algo realmente problemático
      if (err.response?.status !== 404) {
        setError('Erro ao carregar dados do dashboard');
      } else {
        // 404 significa que não há dados ainda - não é erro
        setCvHistory([]);
        setMetrics([]);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedCV({
        name: file.name,
        size: file.size,
        type: file.type,
        file: file
      });
    }
  };

  const handleAnalyze = async () => {
    if (!uploadedCV?.file || !jobDescription.trim()) {
      alert('Por favor, faça upload de um CV e insira a descrição da vaga.');
      return;
    }

    setIsAnalyzing(true);
    setError(null);

    try {
      // Upload e análise real via API
      const result = await curriculumAPI.uploadCurriculum(
        uploadedCV.file,
        jobDescription
      );

      setAnalysisResult({
        score: result.analysis?.pontuacoes?.pontuacao_geral || 75,
        suggestions: result.analysis?.feedback_qualitativo?.split('. ') || [
          'Análise concluída com sucesso',
          'Verifique as sugestões de melhoria'
        ],
        keywords: result.analysis?.palavras_chave || [],
        missingSkills: result.analysis?.sugestoes_melhoria || []
      });

      // Recarregar dados após nova análise
      await loadDashboardData();

    } catch (err) {
      console.error('Erro na análise:', err);
      setError('Erro ao analisar o currículo. Tente novamente.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const renderUploadSection = () => (
    <div className="space-y-6">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Upload do Currículo</h3>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={handleFileUpload}
            className="hidden"
            id="cv-upload"
          />
          <label htmlFor="cv-upload" className="cursor-pointer">
            <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
              <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <p className="mt-1 text-sm text-gray-600">
              {uploadedCV ? `Arquivo selecionado: ${uploadedCV.name}` : 'Clique para selecionar um arquivo'}
            </p>
            <p className="mt-1 text-xs text-gray-500">PDF, DOC ou DOCX até 10MB</p>
          </label>
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Descrição da Vaga</h3>
        <textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Cole aqui a descrição da vaga para análise..."
          className="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        />
      </div>

      <button
        onClick={handleAnalyze}
        disabled={!uploadedCV?.file || !jobDescription.trim() || isAnalyzing}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
      >
        {isAnalyzing ? 'Analisando...' : 'Analisar e Otimizar CV'}
      </button>
    </div>
  );

  const renderAnalysisResult = () => (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Resultado da Análise</h3>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-4">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      {analysisResult && (
        <div className="space-y-6">
          {/* Score */}
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full">
              <span className="text-2xl font-bold text-white">{analysisResult.score}</span>
            </div>
            <p className="mt-2 text-sm text-gray-600">Score de compatibilidade</p>
          </div>

          {/* Sugestões */}
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Sugestões de Melhoria:</h4>
            <ul className="space-y-2">
              {analysisResult.suggestions.map((suggestion, index) => (
                <li key={index} className="flex items-start">
                  <svg className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-gray-700">{suggestion}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Palavras-chave */}
          {analysisResult.keywords.length > 0 && (
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Palavras-chave identificadas:</h4>
              <div className="flex flex-wrap gap-2">
                {analysisResult.keywords.map((keyword, index) => (
                  <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                    {keyword}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Habilidades em falta */}
          {analysisResult.missingSkills.length > 0 && (
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Habilidades que podem ser adicionadas:</h4>
              <div className="flex flex-wrap gap-2">
                {analysisResult.missingSkills.map((skill, index) => (
                  <span key={index} className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );

  const renderHistorySection = () => (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Histórico de Versões</h3>

      {isLoading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Carregando currículos...</p>
        </div>
      ) : cvHistory.length > 0 ? (
        <div className="space-y-4">
          {cvHistory.map((version) => (
            <div key={version.id} className="border border-gray-200 rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h4 className="font-medium text-gray-900">{version.version}</h4>
                  <p className="text-sm text-gray-500">{version.date}</p>
                  <p className="text-xs text-gray-400">{version.filename}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <svg className="mx-auto h-16 w-16 text-gray-300 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h4 className="text-lg font-medium text-gray-900 mb-2">Bem-vindo ao seu Dashboard!</h4>
          <p className="text-gray-600 mb-2">Você ainda não fez upload de currículos.</p>
          <p className="text-sm text-gray-500">Faça upload do seu primeiro currículo para começar a otimizá-lo com IA.</p>
        </div>
      )}
    </div>
  );

  const renderChartSection = () => (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Evolução do CV</h3>

      {isLoading ? (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Carregando métricas...</p>
        </div>
      ) : metrics && metrics.time_series && metrics.time_series.length > 0 ? (
        <div className="space-y-6">
          {/* Estatísticas */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{metrics.total_versions}</div>
              <div className="text-sm text-gray-600">Total de Versões</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{metrics.average_score}%</div>
              <div className="text-sm text-gray-600">Score Médio</div>
            </div>
            <div className="text-center p-4 bg-purple-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{metrics.best_score}%</div>
              <div className="text-sm text-gray-600">Melhor Score</div>
            </div>
            <div className="text-center p-4 bg-orange-50 rounded-lg">
              <div className="text-2xl font-bold text-orange-600">{metrics.improvement_rate}%</div>
              <div className="text-sm text-gray-600">Taxa de Melhoria</div>
            </div>
          </div>

          {/* Gráfico */}
          <div className="h-64 flex items-end justify-center space-x-4">
            {metrics.time_series.map((entry, index) => (
              <div key={index} className="flex flex-col items-center">
                <div
                  className="w-12 bg-gradient-to-t from-blue-500 to-purple-600 rounded-t-lg transition-all duration-500"
                  style={{ height: `${entry.metrics.score * 2}px` }}
                ></div>
                <div className="mt-2 text-center">
                  <div className="text-sm font-medium text-gray-900">{entry.metrics.score}%</div>
                  <div className="text-xs text-gray-500">{entry.version_id}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-8 text-gray-500">
          <p>Nenhuma métrica disponível.</p>
          <p className="text-sm">Analise currículos para ver a evolução.</p>
        </div>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Bem-vindo, {user?.username || 'Usuário'}! Gerencie seus currículos e análises.</p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-md mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'upload', label: 'Upload & Análise', icon: '📤' },
                { id: 'history', label: 'Histórico', icon: '📚' },
                { id: 'chart', label: 'Evolução', icon: '📊' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Content */}
        <div className="grid lg:grid-cols-2 gap-6">
          {activeTab === 'upload' && (
            <>
              <div>{renderUploadSection()}</div>
              <div>{renderAnalysisResult()}</div>
            </>
          )}

          {activeTab === 'history' && (
            <div className="lg:col-span-2">{renderHistorySection()}</div>
          )}

          {activeTab === 'chart' && (
            <div className="lg:col-span-2">{renderChartSection()}</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
