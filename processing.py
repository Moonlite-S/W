import json
from flask_socketio import emit
import ollama
import speech_recognition as sr
import torch
import vlc
import whisper
import os
from TTS.api import TTS

# TODO:
# - After the first several responses, process is alot faster. How can I make the process already fast enough?
# - Sometimes the first couple of words when the audio is processed gets cut off. Fix that.

conversation = []
pause_loop = False # Paused Loop (Maybe stop the thread instead?)
tts = None
speech = None
whisp = None
init_finished = False

def init_processing():
    global tts, speech, whisp, init_finished

    print("Initializting, Please Wait\n")
    # For TTS (Uses my Nvidia GPU for processing primarily)
    # [HAS TO USE CUDA / OTHERWISE USING CPU BLACK SCREENS MY PC]
    if torch.cuda.is_available():
        device = "cuda"
    else:
        raise Exception("Cuda is not installed and / or not in use. CPU can and WILL crash my PC.")

    # Init TTS
    tts = TTS("tts_models/en/jenny/jenny",progress_bar=True, gpu=True).to(device)
    # Init Speech Recog 
    speech = sr.Recognizer()
    # Init Audio to Text (OpenAI Whisper)
    whisp = whisper.load_model("base")

    init_finished = True
    print("Done Initializing\n")


# Main Loop
def main_loop():
    while True:
        if not init_finished:
            print("Hasn't finished initializing yet")
            return

        audio = mic_processing(0)

        Decoded_Message = speech_to_text(audio)

        emit('chat_response', json.dumps({'Decoded_Message': Decoded_Message, 'test': "test"}))

        # Ignore Empty Responses
        if not Decoded_Message:
            return

        message = ollama_processing(Decoded_Message)

        tts_processing(message)

        audio_autoplay()

def mic_processing(mic_source_index: int) -> sr.AudioData:
        with sr.Microphone(mic_source_index) as mic_source:
            speech.adjust_for_ambient_noise(mic_source, duration=1)
            print("\n== Listening for Responses ==\n")
            audio = speech.listen(mic_source)
            print("\n== Not listening right now ==\n")
        
        return audio

def speech_to_text(audio: sr.AudioData) -> str:
    with open("./input/input.wav", "wb") as f:
        f.write(audio.get_wav_data())

    result = whisp.transcribe("./input/input.wav")
    Decoded_Message = result['text']

    # Just in case Whisper tries to read the previous response
    if os.path.exists("./input/input.wav"):
        os.remove("./input/input.wav")
    else:
        print("\n(Nothing to Delete)\n")

    print(f'\n{Decoded_Message}\n') 

    return Decoded_Message

def ollama_processing(Decoded_Message: str) -> str:
    conversation.append(
        {
            'role': 'user',
            'content': Decoded_Message
        }
    )

    print("\n== Responding... ==\n")
    response = ollama.chat(model='W', messages=conversation, stream=True)
    message = ""

    for chunk in response:
        # print(chunk['message']['content'], end='', flush=True)
        message += chunk['message']['content']

    conversation.append(
        {
            'role': 'assistant',
            'content': message
        }
    )

    return message

def tts_processing(message: str):
    print("\n== Audio Processing ==\n")
    tts.tts_to_file(text=message, file_path="./output/output.wav")
    print("\n== Audio Finished ==\n")

def audio_autoplay():
    player = vlc.MediaPlayer("./output/output.wav")
    player.play()