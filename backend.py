from flask_socketio import emit
import json
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

conversation: list = []
pause_loop: bool = False # Paused Loop (Maybe stop the thread instead?)
tts: TTS = None
speech: sr.Recognizer = None
whisp: whisper.Whisper = None
init_finished: bool = False
        
def init_processing():
    ''' Initializing the TTS, Speech Recog, and OpenAI Whisper. 
    
    THIS MUST BE CALLED BEFORE USING THE MAIN LOOP.'''

    global tts, speech, whisp, init_finished

    print("Initializting, Please Wait\n")
    # For TTS (Uses my Nvidia GPU for processing primarily)
    # [HAS TO USE CUDA / OTHERWISE USING CPU BLACK SCREENS MY PC]
    if torch.cuda.is_available():
        device = "cuda"
    else:
        raise Exception("Cuda is not installed and / or not in use. CPU can and WILL crash my PC.")

    # Init TTS
    tts = TTS("tts_models/en/jenny/jenny").to(device)
    # Init Speech Recog 
    speech = sr.Recognizer()
    # Init Audio to Text (OpenAI Whisper)
    whisp = whisper.load_model("base")

    init_finished = True
    print("Done Initializing\n")

# Main Loop
def main_loop():

    if not init_finished:
        raise Exception("Hasn't finished initializing yet. This was not expected. (main_loop)")

    audio = mic_processing(0) # 0 is the default microphone

    Decoded_Message = speech_to_text(audio)

    # Ignore Empty Responses
    if not Decoded_Message:
        return

    message = ollama_processing(Decoded_Message)

    tts_processing(message)

    audio_autoplay()

'''
    Helper Functions
'''

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

    emit('chat_response', get_convo()) # Send User Input

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

    emit('chat_response', get_convo()) # Send Ollama Response

    return message

def tts_processing(message: str) -> None:
    print("\n== Audio Processing ==\n")
    tts.tts_to_file(text=message, file_path="./output/output.wav")
    print("\n== Audio Finished ==\n")

def audio_autoplay() -> None:
    player = vlc.MediaPlayer("./output/output.wav")
    player.play()

def get_convo() -> str:
    global conversation

    my_input: str = ""
    w_latest_message: str = ""

    for i in reversed(conversation):
        if i['role'] == 'user':
            my_input = i['content']
            break

    for i in reversed(conversation):
        if i['role'] == 'assistant':
            w_latest_message = i['content']
            break

    data: dict = {"W": w_latest_message, "Muna": my_input}
    return json.dumps(data)