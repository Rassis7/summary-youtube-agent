import moviepy.editor as mp
import speech_recognition as sr
import os
from pydub import AudioSegment
from pathlib import Path


def get_local_file(path_str: str):
    p = Path(path_str).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {p}")
    if not p.is_file():
        raise IsADirectoryError(f"Isso não é um arquivo: {p}")
    return p


def extract_audio_from_video(video_path, output_audio_path):
    try:
        os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

        formatted_video_path = os.path.join(os.getcwd(), video_path)
        video = mp.VideoFileClip(formatted_video_path)
        video.audio.write_audiofile(output_audio_path)
    except Exception as e:
        print(f"Erro ao extrair áudio do vídeo: {e}")
        raise


def chunk_audio_and_save(audio_path, chunk_length=60000):
    try:
        audio = AudioSegment.from_wav(audio_path)
        length_audio = len(audio)
        chunk_paths = []

        os.makedirs("files/chunks", exist_ok=True)

        for i, chunk in enumerate(range(0, length_audio, chunk_length)):
            chunk_audio = audio[chunk : chunk + chunk_length]
            chunk_path = f"files/chunks/temp_chunk_{i}.wav"
            chunk_audio.export(chunk_path, format="wav")
            chunk_paths.append(chunk_path)
        return chunk_paths
    except Exception as e:
        print(f"Erro ao dividir o áudio: {e}")
        raise


def transcribe_audio_to_text(audio_path, text_output_path, language="pt-BR"):
    try:
        recognizer = sr.Recognizer()

        chunk_file_paths = chunk_audio_and_save(audio_path)
        # Remove the old transcription file if it exists
        if os.path.exists(text_output_path):
            os.remove(text_output_path)

        for i, file_path in enumerate(chunk_file_paths):

            audio_file = sr.AudioFile(file_path)
            with audio_file as source:
                audio_data = recognizer.record(source)

                try:
                    text = recognizer.recognize_google(audio_data, language=language)
                    with open(text_output_path, "a", encoding="utf-8") as text_file:
                        text_file.write(text + "\n")
                        print(f"✅ Saved chunk {i + 1}/{len(chunk_file_paths)}")
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand the audio")
                except sr.RequestError as e:
                    print(
                        f"Could not request results from Google Speech Recognition service; {e}"
                    )
    except Exception as e:
        print(f"Erro ao transcrever o áudio: {e}")
        raise
