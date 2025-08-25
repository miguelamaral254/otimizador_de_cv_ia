import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ProgressChart = ({ data, title = "Evolução do Currículo" }) => {
  // Transformar dados para o formato esperado pelo Recharts
  const chartData = data.map((item, index) => ({
    version: item.version_id || `v${index + 1}`,
    score: item.metrics?.score || 0,
    clarity: item.metrics?.clarity || 0,
    relevance: item.metrics?.relevance || 0,
    keywords: item.metrics?.keywords || 0,
    structure: item.metrics?.structure || 0,
    personalization: item.metrics?.personalization || 0,
    date: new Date(item.timestamp).toLocaleDateString('pt-BR')
  }));

  if (!data || data.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
        <div className="text-center text-gray-500 py-8">
          <p>Nenhum dado de progresso disponível</p>
          <p className="text-sm">Faça upload de um currículo para ver sua evolução</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          
          <XAxis 
            dataKey="version" 
            stroke="#666"
            tick={{ fontSize: 12 }}
            label={{ value: "Versão", position: "insideBottom", offset: -5 }}
          />
          
          <YAxis 
            stroke="#666"
            tick={{ fontSize: 12 }}
            domain={[0, 100]}
            label={{ value: "Pontuação", angle: -90, position: "insideLeft", offset: 10 }}
          />
          
          <Tooltip 
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #ccc',
              borderRadius: '8px',
              boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
            }}
            formatter={(value, name) => [
              `${value}%`, 
              {
                'score': 'Score Geral',
                'clarity': 'Clareza',
                'relevance': 'Relevância',
                'keywords': 'Palavras-chave',
                'structure': 'Estrutura',
                'personalization': 'Personalização'
              }[name] || name
            ]}
            labelFormatter={(label) => `Versão: ${label}`}
          />
          
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            formatter={(value) => ({
              'score': 'Score Geral',
              'clarity': 'Clareza',
              'relevance': 'Relevância',
              'keywords': 'Palavras-chave',
              'structure': 'Estrutura',
              'personalization': 'Personalização'
            }[value] || value)}
          />
          
          {/* Score Geral - linha principal */}
          <Line 
            type="monotone" 
            dataKey="score" 
            stroke="#2563eb" 
            strokeWidth={3}
            activeDot={{ r: 8, stroke: '#2563eb', strokeWidth: 2, fill: '#fff' }}
            name="score"
          />
          
          {/* Métricas individuais */}
          <Line 
            type="monotone" 
            dataKey="clarity" 
            stroke="#10b981" 
            strokeWidth={2}
            strokeDasharray="5 5"
            activeDot={{ r: 6 }}
            name="clarity"
          />
          
          <Line 
            type="monotone" 
            dataKey="relevance" 
            stroke="#f59e0b" 
            strokeWidth={2}
            strokeDasharray="5 5"
            activeDot={{ r: 6 }}
            name="relevance"
          />
          
          <Line 
            type="monotone" 
            dataKey="keywords" 
            stroke="#8b5cf6" 
            strokeWidth={2}
            strokeDasharray="5 5"
            activeDot={{ r: 6 }}
            name="keywords"
          />
          
          <Line 
            type="monotone" 
            dataKey="structure" 
            stroke="#ef4444" 
            strokeWidth={2}
            strokeDasharray="5 5"
            activeDot={{ r: 6 }}
            name="structure"
          />
          
          <Line 
            type="monotone" 
            dataKey="personalization" 
            stroke="#06b6d4" 
            strokeWidth={2}
            strokeDasharray="5 5"
            activeDot={{ r: 6 }}
            name="personalization"
          />
        </LineChart>
      </ResponsiveContainer>
      
      {/* Estatísticas resumidas */}
      {data.length > 0 && (
        <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <p className="text-sm text-gray-600">Total de Versões</p>
            <p className="text-2xl font-bold text-blue-600">{data.length}</p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">Score Médio</p>
            <p className="text-2xl font-bold text-green-600">
              {Math.round(data.reduce((acc, item) => acc + (item.metrics?.score || 0), 0) / data.length)}%
            </p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">Melhor Score</p>
            <p className="text-2xl font-bold text-purple-600">
              {Math.round(Math.max(...data.map(item => item.metrics?.score || 0)))}%
            </p>
          </div>
          <div className="text-center">
            <p className="text-sm text-gray-600">Última Análise</p>
            <p className="text-lg font-semibold text-gray-800">
              {new Date(data[data.length - 1].timestamp).toLocaleDateString('pt-BR')}
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProgressChart;
