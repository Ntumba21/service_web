from .params import TradParams, DictionnaryParams, DictionnaryLineParams
from .models import Trad, Dictionnary, DictionnaryLine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

def create_trad(db: Session, params: TradParams, trad: str):
    # Crée une nouvelle entrée dans la table `Trad`
    new_trad = Trad(word=params.word, trad=trad, dictionnary=params.dictionnary)
    db.add(new_trad)
    db.commit()
    db.refresh(new_trad)
    return new_trad

def create_dictionnary(db: Session, params: DictionnaryParams):
    # Crée un nouveau dictionnaire dans la table `Dictionnary`
    new_dictionnary = Dictionnary(name=params.name)
    db.add(new_dictionnary)
    db.commit()
    db.refresh(new_dictionnary)
    return new_dictionnary

def create_dictionnary_line(db: Session, letter: str, trad: str, dictionnary_id: int):
    # Ajoute une nouvelle ligne de traduction dans la table `DictionnaryLine`
    new_dictionnary_line = DictionnaryLine(letter=letter, trad=trad, dictionnary_id=dictionnary_id)
    db.add(new_dictionnary_line)
    db.commit()
    db.refresh(new_dictionnary_line)
    return new_dictionnary_line

def get_trad_by_id(db: Session, trad_id: int):
    # Récupère une traduction par son ID
    return db.query(Trad).filter(Trad.id == trad_id).first()

def update_trad(db: Session, trad_id: int, new_trad: Trad):
    # Met à jour une traduction dans la table `Trad` par son ID
    db_trad = db.query(Trad).filter(Trad.id == trad_id).first()
    if db_trad:
        db_trad.word = new_trad.word
        db_trad.trad = new_trad.trad
        db_trad.dictionnary = new_trad.dictionnary
        db.commit()
        db.refresh(db_trad)
        return db_trad
    return None

def delete_trad(db: Session, trad_id: int):
    # Supprime une traduction de la table `Trad` par son ID
    db_trad = db.query(Trad).filter(Trad.id == trad_id).first()
    if db_trad:
        db.delete(db_trad)
        db.commit()
        return True
    return False

def get_trad_by_letter(db: Session, letter: str, dictionnary_id: int):
    # Récupère une traduction par lettre et ID de dictionnaire
    return db.query(DictionnaryLine).filter(
        DictionnaryLine.letter == letter,
        DictionnaryLine.dictionnary_id == dictionnary_id
    ).first()

def delete_dictionnary_by_id(db: Session, dictionnary_id: int):
    # Supprime un dictionnaire par son ID
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

def delete_dictionnary_line_by_id(db: Session, dictionnary_line_id: int):
    # Supprime une ligne de traduction par son ID
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

def create_translation(db: Session, word: str, translated_word: str, dictionnary_name: str):
    # Crée une nouvelle traduction et l'enregistre dans la table `Trad`
    new_translation = Trad(word=word, trad=translated_word, dictionnary=dictionnary_name)
    db.add(new_translation)
    db.commit()
    db.refresh(new_translation)
    return new_translation

def get_all_trads(db: Session):
    # Récupère toutes les traductions de la table `Trad`
    return db.query(Trad).all()

def update_dictionnary_by_id(db: Session, dictionnary_id: int, new_name: str):
    # Update a dictionary by its ID
    try:
        db_dictionnary = db.query(Dictionnary).filter(Dictionnary.id == dictionnary_id).first()
        if db_dictionnary:
            db_dictionnary.name = new_name
            db.commit()
            db.refresh(db_dictionnary)
            return db_dictionnary
        return None
    except SQLAlchemyError as e:
        print(f"SQLAlchemy Error: {e}")
        return None

