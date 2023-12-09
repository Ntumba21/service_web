from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Trad(Base):
    # Table des traductions
    __tablename__ = "trads"

    # Colonnes de la table Trad
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(40))  # Mot à traduire
    trad = Column(String(255))  # Traduction du mot
    dictionnary = Column(String(40))  # Dictionnaire associé

class Dictionnary(Base):
    # Table des dictionnaires
    __tablename__ = "dictionnaries"

    # Colonnes de la table Dictionnary
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), unique=True, index=True)  # Nom du dictionnaire

    # Relation avec la table DictionnaryLine
    lines = relationship("DictionnaryLine", back_populates="dictionnary")

class DictionnaryLine(Base):
    # Table des lignes de dictionnaire
    __tablename__ = "dictionnaries_lines"

    # Colonnes de la table DictionnaryLine
    id = Column(Integer, primary_key=True, index=True)
    letter = Column(String(2))  # Lettre
    trad = Column(String(5))  # Traduction de la lettre
    dictionnary_id = Column(Integer, ForeignKey("dictionnaries.id"))  # Clé étrangère vers la table Dictionnary

    # Relation avec la table Dictionnary
    dictionnary = relationship("Dictionnary", back_populates="lines")
