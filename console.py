from audio_transcription import AudioTranscription
import os


def main():
    small_filename = "source/Recording.wav"
    large_filename = "source/Recording (4).wav"
    persian_filename = "source/Recording (8).mp3"

    audio_transcription = AudioTranscription()

    # Transcription for a standard audio file
    small_file_text = audio_transcription.standard_audio_file_transcriptor(path=small_filename)

    # Transcription for a large audio file
    large_file_text = audio_transcription.large_audio_file_transcriptor(path=large_filename)

    # Transcription for a Persian audio file
    persian_file_text = audio_transcription.large_audio_file_transcriptor(path=persian_filename, language='fa-IR')

    os.system('cls')

    print("Small File Text:")
    print(small_file_text)
    print("================")

    print("Large File Text:")
    print(large_file_text)
    print("================")

    print("Persian File Text:")
    print(persian_file_text)


if __name__ == "__main__":
    main()
