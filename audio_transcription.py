import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence


class AudioTranscription:
    '''
    This class can use the free API from Google to recognize a speech and return the text of an audio.
    '''
    r = sr.Recognizer()

    @classmethod
    def standard_audio_file_transcriptor(cls, path):
        '''
        This method is used to get a standard audio file and return the transcript.
        :param path: Audio file path
        :return: Transcript of the audio file
        '''

        # Opening the audio file
        with sr.AudioFile(path) as source:
            # Loading the audio to memory
            audio_data = cls.r.record(source)

            # Sending the loaded data to Google servers and getting the response.
            text = cls.r.recognize_google(audio_data)

            return text

    @classmethod
    def large_audio_file_transcriptor(cls, path, min_silence_len = 500, keep_silence=500):
        '''
        This method is used for getting the transcript of a large audio file (Usually more than 10MB)
        :param path: Audio file path
        :param min_silence_len: A number for the minimum silence length for splitting audio
        :param keep_silence: A number that tells the splitter how much silence should add
        :return: Transcript of the audio file
        '''

        # Opening the audio file using pydub and based on file extension
        if str(path).endswith('.wav'):
            sound = AudioSegment.from_wav(path)
        elif str(path).endswith('.mp3'):
            sound = AudioSegment.from_mp3(path)
        elif str(path).endswith('.ogg'):
            sound = AudioSegment.from_ogg(path)
        else:
            return "Illegal file format."

        # Splitting audio file into chunks
        chunks = split_on_silence(sound,
                                  min_silence_len=min_silence_len,
                                  silence_thresh=sound.dBFS-14,
                                  keep_silence=keep_silence)

        # A new folder name for saving audio chunks
        folder_name = "audio_chunks"

        # Creating the folder if not exits.
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        # Final text output.
        whole_text = ""

        # Iterating over each audio chunk to get the transcript
        for i, audio_chunk in enumerate(chunks, start=1):
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")

            # Exporting the audio chunk as a separated audio file
            audio_chunk.export(chunk_filename, format="wav")

            # Opening the audio file
            with sr.AudioFile(chunk_filename) as source:
                # Loading audio to memory
                audio_data = cls.r.record(source)

                try:
                    # Sending the loaded data to Google servers and getting the response
                    text = cls.r.recognize_google(audio_data)
                except sr.UnknownValueError as e:
                    print(f"Error: {e}")

                whole_text += f"{text}\n"

        return whole_text