#googletrans-3.1.0a0

from typing import Optional
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS
from fastapi.responses import FileResponse

from fastapi import FastAPI, File, UploadFile
import googletrans
from googletrans import Translator
from fastapi.middleware.cors import CORSMiddleware
translator = Translator()
import shutil
import os
lan = googletrans.LANGUAGES
#print(lan)
keys = list(lan.keys())
vals = list(lan.values())


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/text-to-speech/{text}")
def text_to_speech(text: str):
    tts = gTTS(text)
    audio_file = 'text_to_speech.mp3'
    tts.save(audio_file)
    return FileResponse(audio_file, media_type='audio/mpeg')

@app.post("/speech-to-text/")
async def speech_to_text(audio_file: UploadFile = File(...), lang: Optional[str] = "en-US"):
    file_location = audio_file.filename
    with open(file_location, "wb") as file_object:
        shutil.copyfileobj(audio_file.file, file_object)
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_location) as source:
        audio = recognizer.record(source)
    os.remove(file_location)
    text = recognizer.recognize_google(audio, language=lang)
    return {"text": text}


@app.post("/translators/")
async def tra(sentence,lang):
        lang = lang.lower()
        return translator.translate(sentence,dest=keys[vals.index(lang)]).text



from woocommerce import API

wcapi = API(
    url="https://nsautotrading.co.uk",
    consumer_key="ck_05994a5bb7046e5da665ab8708d51a488236f922",
    consumer_secret="cs_20c4803581ed724f850ffd2ce34fcf1c8339cb68",
    version="wc/v3"
)

@app.post("/woo_make_order/")
def make_order(data):
    print(type(data))
    return wcapi.post("orders", data).json()
        



# for run the api uvicorn translator_api:app
