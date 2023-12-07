from .params import TradParams, DictionnaryParams, DictionnaryLineParams
from .models import Trad, Dictionnary, DictionnaryLine
from sqlalchemy.orm import Session

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

def create_trad(db: Session, params: TradParams, trad: str):
    new_trad = Trad(word=params.word, trad=trad, dictionnary=params.dictionnary)
    db.add(new_trad)
    db.commit()
    db.refresh(new_trad)
    return new_trad

# Fonction pour créer un dictionnaire
def create_dictionnary(db: Session, params: DictionnaryParams):
    new_dictionnary = Dictionnary(name=params.name)
    db.add(new_dictionnary)
    db.commit()
    db.refresh(new_dictionnary)
    return new_dictionnary

# Fonction pour créer une ligne de traduction
def create_dictionnary_line(db: Session, letter: str, trad: str, dictionnary_id: int):
    new_dictionnary_line = DictionnaryLine(letter=letter, trad=trad, dictionnary_id=dictionnary_id)
    db.add(new_dictionnary_line)
    db.commit()
    db.refresh(new_dictionnary_line)
    return new_dictionnary_line

# Fonction pour obtenir une traduction par son ID
def get_trad_by_id(db: Session, trad_id: int):
    return db.query(Trad).filter(Trad.id == trad_id).first()

# Fonction pour mettre à jour une traduction
def update_trad(db: Session, trad_id: int, new_trad: Trad):
    db_trad = db.query(Trad).filter(Trad.id == trad_id).first()
    if db_trad:
        db_trad.word = new_trad.word
        db_trad.trad = new_trad.trad
        db_trad.dictionnary = new_trad.dictionnary
        db.commit()
        db.refresh(db_trad)
        return db_trad
    return None

# Fonction pour supprimer une traduction
def delete_trad(db: Session, trad_id: int):
    db_trad = db.query(Trad).filter(Trad.id == trad_id).first()
    if db_trad:
        db.delete(db_trad)
        db.commit()
        return True
    return False

# Fonction pour obtenir une traduction par lettre
def get_trad_by_letter(db: Session, letter: str, dictionnary_id: int):
    return db.query(DictionnaryLine).filter(
        DictionnaryLine.letter == letter,
        DictionnaryLine.dictionnary_id == dictionnary_id
    ).first()

# Supprimer un dictionnaire par son ID
def delete_dictionnary_by_id(db: Session, dictionnary_id: int):
    try:
        db_dictionnary = db.query(Dictionnary).filter(Dictionnary.id == dictionnary_id).first()
        if db_dictionnary:
            db.delete(db_dictionnary)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return False

# Supprimer une ligne de traduction
def delete_dictionnary_line_by_id(db: Session, dictionnary_line_id: int):
    try:
        db_dictionnary_line = db.query(DictionnaryLine).filter(DictionnaryLine.id == dictionnary_line_id).first()
        if db_dictionnary_line:
            db.delete(db_dictionnary_line)
            db.commit()
            return True
        return False
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return False


