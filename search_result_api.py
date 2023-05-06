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
        



# for run the api uvicorn translator_api:app
