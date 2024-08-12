# W, some random ai bot you can talk to i guess

This project was loosely inspired by Neuro-sama. I wanted to see if I can make something similar to her on a smaller scale, and so I made W. This project is named afer a character in the popular video game, Arknights.

All the models used are ran locally, so you kinda need a decent setup to run this.

![W Picture](wlol.png)

## Things I've Used in this Project

- Speech-Recognition for Microphone recording
- OpenAI's Whisper for Audio to Text
- Ollama for using Llama3's LLM
- TTS for text to speech
- vlc-python for audio playback
- WebSockets to communicate between server and client in real time
- ffmpeg

## Things I wanna add someday

- A functioning Pause button
- Having W speak through the browser instead of using VLC
- A better model (it fucking sucks)

## Current issues

- Reloading the page breaks the backend, so you'll have to restart the entire thing over again. Currently trying to fix this.
- Sometimes empty responses will be read as 'you' or some other weird things. Dunno how this is happening.

## Usage

Uh, so yeah, first off, I wouldn't recommend trying it, but if you want, I'd tried stream-lining it to the best of my ability. It's literally all in a dev environment too, so uh yeah. All scuff and no rubber. Don't say I didn't warn you.

First off, this is a Windows only project.

Secondly, this requires a GPU with at least 8GB of VRAM, I think. And a GPU that has CUDA cores, so NVIDIA GPUs (There's a line in the `backend.py` file where you can remove the cuda requirement, but it crashes my PC so wouldn't recommend it).

Another thing is to make sure you have ffmpeg installed and put in your PATH ENV.
Here's a guide I [found](https://www.editframe.com/guides/how-to-install-and-start-using-ffmpeg-in-under-10-minutes). If you end up getting errors while running, it may be that the PATH hasn't been configured correctly (idk it's been like several months since I did this lmao).

Next you need [Ollama](https://ollama.com/), and you need to install the custom W-model (this one comes with the repo).
After you install Ollama from their site, the command to install W-'s model is:

``` terminal
ollama W -f W-model
```

You can also just use another model if you want. W is just based of Llama3's Uncensored model, which is also on Ollama.

Before installing any Python packages, remember to create and activate a venv. (.venv is the name of the folder)

``` terminal
python -m venv .venv 
.venv/Scripts/Activate`
```

Afterwards, you can install all the Python dependencies with this:

``` terminal
pip install -r requirements.txt 
```

Then run command to install the required npm packages for the frontend:

``` terminal
cd client | npm install
```

To run, if you're on Windows, you can use the `start_dev.bat` file.

When you run it the first time, it should download all the other neccessary models needed to function.

Once it's on, go to the site where the console lists it's address. It'll be like localhost with a port number. The backend should start working, and you'll be able to speak once it's done initializing.

If W can't hear your voice, make sure you default microphone is set to whatever your mic is.

Again this is a very scuffed project and I only expect this to be read by my future self in like a decade or so or maybe a couple people.

### Changelog

- (8/11/2024)

> Made it public???? idk why

- (8/10/2024)

> Web app should show messages quicker
>
> Some refactoring (okay a lot was made)

- (6/7/2024)

> Refactored 'processing.py'
