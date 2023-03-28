#googletrans-3.1.0a0

from fastapi import FastAPI
import googletrans
from googletrans import Translator
from fastapi.middleware.cors import CORSMiddleware
translator = Translator()

lan = googletrans.LANGUAGES
#print(lan)
keys = list(lan.keys())
vals = list(lan.values())


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translators/")
async def tra(sentence,lang):
        lang = lang.lower()
        return translator.translate(sentence,dest=keys[vals.index(lang)]).text
        



# for run the api uvicorn translator_api:app
