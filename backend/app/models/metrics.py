"""
Modelo para métricas de currículos.
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class Metrics(Base):
    """Modelo para métricas de currículos."""
    
    __tablename__ = "metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    curriculum_id = Column(Integer, ForeignKey("curriculum.id"), nullable=False)
    
    # Scores das análises
    action_verbs_score = Column(Float, default=0.0)
    quantification_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    curriculum = relationship("Curriculum", back_populates="metrics")
    
    def __repr__(self):
        return f"<Metrics(id={self.id}, curriculum_id={self.curriculum_id}, overall_score={self.overall_score})>"
