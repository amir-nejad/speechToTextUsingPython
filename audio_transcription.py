import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


class AudioTranscription:
    r = sr.Recognizer()

    @classmethod
    def standard_audio_file_transcriptor(cls, path):

        with sr.AudioFile(path) as source:
            audio_data = cls.r.record(source)

            text = cls.r.recognize_google(audio_data)

            return text

    @classmethod
    def large_audio_file_transcriptor(cls, path):

        if str(path).endswith('.wav'):
            sound = AudioSegment.from_wav(path)
        elif str(path).endswith('.mp3'):
            sound = AudioSegment.from_mp3(path)
        elif str(path).endswith('.ogg'):
            sound = AudioSegment.from_ogg(path)
        else:
            return "Illegal file format."

        chunks = split_on_silence(sound,
                                  min_silence_len=500,
                                  silence_thresh=sound.dBFS-14,
                                  keep_silence=500)

        folder_name = "audio_chunks"

        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        whole_text = ""

        for i, audio_chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")

            with sr.AudioFile(chunk_filename) as source:
                audio_data = cls.r.record(source)

                try:
                    text = cls.r.recognize_google(audio_data)
                except sr.UnknownValueError as e:
                    print(f"Error: {e}")

                whole_text += f"{text}\n"

        return whole_text