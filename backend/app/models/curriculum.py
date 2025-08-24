from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Curriculum(Base):
    """Modelo principal para currículos enviados pelos usuários."""
    
    __tablename__ = "curriculum"
    
    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Arquivo
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # Em bytes
    
    # Metadados
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="curriculum")
    versions = relationship("CurriculumVersion", back_populates="curriculum", cascade="all, delete-orphan")
    analyses = relationship("CurriculumAnalysis", back_populates="curriculum", cascade="all, delete-orphan")
    metrics = relationship("Metrics", back_populates="curriculum", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Curriculum(id={self.id}, title='{self.title}', user_id={self.user_id})>"


class CurriculumVersion(Base):
    """Modelo para controle de versões de currículos."""
    
    __tablename__ = "curriculum_versions"
    
    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    curriculum_id = Column(Integer, ForeignKey("curriculum.id"), nullable=False)
    
    # Versão
    version_number = Column(Integer, nullable=False)
    version_name = Column(String(100), nullable=True)  # Ex: "v1.0", "Versão Final"
    
    # Arquivo
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    
    # Metadados
    changes_description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    curriculum = relationship("Curriculum", back_populates="versions")
    analysis = relationship("CurriculumAnalysis", back_populates="version", uselist=False, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<CurriculumVersion(id={self.id}, version={self.version_number}, curriculum_id={self.curriculum_id})>"


class CurriculumAnalysis(Base):
    """Modelo para análises de currículos realizadas pela IA."""
    
    __tablename__ = "curriculum_analyses"
    
    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    curriculum_id = Column(Integer, ForeignKey("curriculum.id"), nullable=False)
    version_id = Column(Integer, ForeignKey("curriculum_versions.id"), nullable=True)
    
    # Análise com spaCy
    spacy_analysis = Column(JSON, nullable=True)  # Resultados do spaCy
    
    # Análise com Google Gemini
    gemini_analysis = Column(JSON, nullable=True)  # Resultados do Gemini
    
    # Métricas quantitativas
    action_verbs_count = Column(Integer, default=0)
    quantified_results_count = Column(Integer, default=0)
    keywords_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    # Feedback da IA
    strengths = Column(JSON, nullable=True)  # Lista de pontos fortes
    weaknesses = Column(JSON, nullable=True)  # Lista de pontos fracos
    suggestions = Column(JSON, nullable=True)  # Sugestões de melhoria
    
    # Metadados
    analysis_date = Column(DateTime(timezone=True), server_default=func.now())
    processing_time = Column(Float, nullable=True)  # Tempo de processamento em segundos
    
    # Relacionamentos
    curriculum = relationship("Curriculum", back_populates="analyses")
    version = relationship("CurriculumVersion", back_populates="analysis")
    
    def __repr__(self):
        return f"<CurriculumAnalysis(id={self.id}, curriculum_id={self.curriculum_id}, score={self.overall_score})>"
