import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil


class AudioTranscription:
    '''
    This class can use the free API from Google to recognize a speech and return the text of an audio.
    '''
    r = sr.Recognizer()

    @classmethod
    def standard_audio_file_transcriptor(cls, path, language="en-US"):
        '''
        This method is used to get a standard audio file and return the transcript.
        :param language: The language of the audio file
        :param path: Audio file path
        :return: Transcript of the audio file
        '''

        # Opening the audio file
        with sr.AudioFile(path) as source:
            # Loading the audio to memory
            audio_data = cls.r.record(source)

            try:
                # Sending the loaded data to Google servers and getting the response.
                text = cls.r.recognize_google(audio_data, language=language)
            except sr.UnknownValueError as e:
                print(f'Error: {e}')
                return "Operation Failed."

            return text

    @classmethod
    def large_audio_file_transcriptor(cls, path, min_silence_len=500, keep_silence=500, language="en-US"):
        '''
        This method is used for getting the transcript of a large audio file (Usually more than 10MB)
        :param language: The language of the audio file.
        :param path: Audio file path
        :param min_silence_len: A number for the minimum silence length for splitting audio
        :param keep_silence: A number that tells the splitter how much silence should add
        :return: Transcript of the audio file
        '''

        # Opening the audio file using pydub and based on file extension
        sound = cls.__get_sound(path)

        if sound is None:
            return "Illegal file."

        # Splitting audio file into chunks
        chunks = split_on_silence(sound,
                                  min_silence_len=min_silence_len,
                                  silence_thresh=sound.dBFS - 14,
                                  keep_silence=keep_silence)

        # A new folder name for saving audio chunks
        folder_name = "audio_chunks"

        # Creating the folder if not exits.
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        else:
            # Removing the previous folder with all its files and creating an empty folder again.
            shutil.rmtree(folder_name)
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
                    text = cls.r.recognize_google(audio_data, language=language)
                except sr.UnknownValueError as e:
                    print(f"Error: {e}")
                    text = ""

                whole_text += f"{text}\n"

        return whole_text

    @classmethod
    def __get_sound(cls, path):
        # Getting file extension
        file_name, extension = os.path.splitext(path)

        # Using match cases for faster detection of the extension and load sound.
        match extension:
            case '.mp3':
                sound = AudioSegment.from_mp3(path)
            case '.wav':
                sound = AudioSegment.from_wav(path)
            case '.ogg':
                sound = AudioSegment.from_ogg(path)
            case default:
                return None
        return sound

