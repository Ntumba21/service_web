from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Dictionnary, DictionnaryLine
from .repository import create_dictionnary, create_dictionnary_line, delete_dictionnary_by_id, delete_dictionnary_line_by_id, create_trad
from .params import TradParams

Dictionnary.metadata.create_all(bind=engine)
DictionnaryLine.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def read_root():
    return {'message': 'Welcome to the API!'}

@app.get('/trads')
def get_all_trads(db: Session = Depends(get_db)):
    trads = db.query(Trad).all()
    return {'trads': trads}

#Traduction d'un mot
@app.get('/translate/{word}', tags=["Translation"])
async def translate_word(word: str, dictionary_name: str, db: Session = Depends(get_db)):
    dictionary = db.query(Dictionnary).filter(Dictionnary.name == dictionary_name).first()
    if not dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")

    translations = []
    translated_word = ''.join([get_trad_by_letter(db, letter, dictionary.id).trad if get_trad_by_letter(db, letter, dictionary.id) else 'Translation not found' for letter in word])

    for letter in word:
        translation = get_trad_by_letter(db, letter, dictionary.id)
        translated_letter = translation.trad if translation else 'Translation not found'
        translations.append({'letter': letter, 'translation': translated_letter})

    return {'word': word, 'translations': translations, 'translated_word': translated_word}

#Récuperer les traductions d'un dictionnaire
@app.get('/dictionary/{dictionary_name}', tags=["Dictionary"])
async def get_dictionary(dictionary_name: str, db: Session = Depends(get_db)):
    dictionary = db.query(Dictionnary).filter(Dictionnary.name == dictionary_name).first()
    if not dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")

    dictionary_lines = db.query(DictionnaryLine).filter(DictionnaryLine.dictionnary_id == dictionary.id).all()
    return dictionary_lines

#Créer une traduction
@app.post('/trad')
def create_new_trad(request: TradParams, db: Session = Depends(get_db)):
    new_trad = create_trad(db, request)  
    return {'message': 'Trad created successfully', 'new_trad_id': new_trad.id}    

# Création d'un dictionnaire
@app.post('/dictionaries', tags=["Dictionaries"])
def create_new_dictionary(name: str, db: Session = Depends(get_db)):
    new_dictionary = create_dictionnary(db, DictionnaryParams(name=name))
    return {'message': 'Dictionary created successfully', 'new_dictionary_id': new_dictionary.id}

#Supprimer un dictionnaire par son ID            
@app.delete('/dictionnaries/{dictionnary_id}')
def delete_dictionnary_by_id_api(dictionnary_id: int, db: Session = Depends(get_db)):
    deleted = delete_dictionnary_by_id(db, dictionnary_id)
    if deleted:
        return {'message': f"Dictionnary with ID: {dictionnary_id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Dictionnary with ID: {dictionnary_id} not found")

# Ajouter une ligne de traduction
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


