// Dados de exemplo para teste do gráfico de progresso
export const mockProgressData = [
  {
    version_id: "v1",
    timestamp: "2024-01-15T10:00:00Z",
    metrics: {
      score: 65,
      clarity: 70,
      relevance: 60,
      keywords: 55,
      structure: 75,
      personalization: 65
    }
  },
  {
    version_id: "v2",
    timestamp: "2024-02-01T14:30:00Z",
    metrics: {
      score: 72,
      clarity: 75,
      relevance: 68,
      keywords: 70,
      structure: 78,
      personalization: 70
    }
  },
  {
    version_id: "v3",
    timestamp: "2024-02-15T09:15:00Z",
    metrics: {
      score: 78,
      clarity: 80,
      relevance: 75,
      keywords: 78,
      structure: 82,
      personalization: 75
    }
  },
  {
    version_id: "v4",
    timestamp: "2024-03-01T11:45:00Z",
    metrics: {
      score: 82,
      clarity: 85,
      relevance: 80,
      keywords: 82,
      structure: 85,
      personalization: 80
    }
  },
  {
    version_id: "v5",
    timestamp: "2024-03-15T16:20:00Z",
    metrics: {
      score: 87,
      clarity: 88,
      relevance: 85,
      keywords: 88,
      structure: 90,
      personalization: 85
    }
  }
];

export const mockSummaryStats = {
  totalVersions: 5,
  averageScore: 76.8,
  bestScore: 87,
  improvementRate: 33.8,
  lastAnalysisDate: "2024-03-15T16:20:00Z"
};
