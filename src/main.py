from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from .models import Dictionnary, DictionnaryLine, Base
from .repository import (
    get_all_trads,
    create_translation,
    create_dictionnary,
    create_dictionnary_line,
    delete_dictionnary_by_id,
    delete_dictionnary_line_by_id,
    create_trad,
    get_trad_by_letter,
    update_dictionnary_by_id
)
from .params import DictionnaryParams, TradParams

# Création des tables dans la base de données
Base.metadata.create_all(bind=engine)

# Initialisation de l'application FastAPI
app = FastAPI()

# Fonction pour obtenir la session de la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint racine de l'API
@app.get('/')
def read_root():
    return {'message': 'Welcome to the API!'}

# Récupérer toutes les traductions
@app.get('/trads')
def get_all_translations(db: Session = Depends(get_db)):
    translations = get_all_trads(db)
    return {'translations': translations}

# Traduction d'un mot dans un dictionnaire spécifique
@app.post('/translate/{word}', tags=["Translation"])
async def translate_word(word: str, dictionnary_name: str, db: Session = Depends(get_db)):
    # Vérification de l'existence du dictionnaire
    dictionnary = db.query(Dictionnary).filter(Dictionnary.name == dictionnary_name).first()
    if not dictionnary:
        raise HTTPException(status_code=404, detail="Dictionnary not found")

    translations = []
    translated_word = ''.join([get_trad_by_letter(db, letter, dictionnary.id).trad if get_trad_by_letter(db, letter, dictionnary.id) else 'Translation not found' for letter in word])

    # Récupération des traductions pour chaque lettre du mot
    for letter in word:
        translation = get_trad_by_letter(db, letter, dictionnary.id)
        translated_letter = translation.trad if translation else 'Translation not found'
        translations.append({'letter': letter, 'translation': translated_letter})

    # Enregistrement de la traduction dans la table `trads`
    create_translation(db, word, translated_word, dictionnary_name)

    return {'word': word, 'translations': translations, 'translated_word': translated_word}

# Récupérer toutes les lignes d'un dictionnaire
@app.get('/dictionary/{dictionary_name}', tags=["Dictionary"])
async def get_dictionary(dictionary_name: str, db: Session = Depends(get_db)):
    dictionary = db.query(Dictionnary).filter(Dictionnary.name == dictionary_name).first()
    if not dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")

    dictionary_lines = db.query(DictionnaryLine).filter(DictionnaryLine.dictionnary_id == dictionary.id).all()
    return dictionary_lines

# Créer un nouveau dictionnaire
@app.post('/dictionnaries')
def create_new_dictionnary(name: str, db: Session = Depends(get_db)):
    new_dictionnary = create_dictionnary(db, DictionnaryParams(name=name))
    return {'message': 'Dictionnary created successfully', 'new_dictionnary_id': new_dictionnary.id}
        
# Supprimer un dictionnaire par son ID
@app.delete('/dictionnaries/{dictionnary_id}')
def delete_dictionnary_by_id_api(dictionnary_id: int, db: Session = Depends(get_db)):
    deleted = delete_dictionnary_by_id(db, dictionnary_id)
    if deleted:
        return {'message': f"Dictionnary with ID: {dictionnary_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Dictionnary with ID: {dictionnary_id} not found")

# Créer une nouvelle ligne de traduction
@app.post('/dictionnarylines')
def create_new_dictionnary_line(letter: str, trad: str, dictionnary_id: int, db: Session = Depends(get_db)):
    new_dictionnary_line = create_dictionnary_line(db, letter=letter, trad=trad, dictionnary_id=dictionnary_id)
    return {'message': 'Dictionnary line created successfully', 'new_dictionnary_line_id': new_dictionnary_line.id}

# Supprimer une ligne de traduction par son ID
@app.delete('/dictionnarylines/{dictionnary_line_id}')
def delete_dictionnary_line_by_id_api(dictionnary_line_id: int, db: Session = Depends(get_db)):
    deleted = delete_dictionnary_line_by_id(db, dictionnary_line_id)
    if deleted:
        return {'message': f"Dictionnary line with ID: {dictionnary_line_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Dictionnary line with ID: {dictionnary_line_id} not found")

# Update a dictionary by its ID
@app.put('/dictionnaries/{dictionnary_id}')
def update_dictionnary(dictionnary_id: int, new_name: str, db: Session = Depends(get_db)):
    updated_dictionnary = update_dictionnary_by_id(db, dictionnary_id, new_name)
    if updated_dictionnary:
        return {'message': f"Dictionnary with ID: {dictionnary_id} updated successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Dictionnary with ID: {dictionnary_id} not found")
