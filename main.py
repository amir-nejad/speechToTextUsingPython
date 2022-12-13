from audio_transcription import AudioTranscription
import os


def main():
    small_filename = "Recording.wav"
    large_filename = "Recording (4).wav"

    audio_transcription = AudioTranscription()

    # Transcription for a standard audio file
    small_file_text = audio_transcription.standard_audio_file_transcriptor(small_filename)

    # Transcription for a large audio file
    large_file_text = audio_transcription.large_audio_file_transcriptor(large_filename)

    os.system('cls')

    print("Small File Text:")
    print(small_file_text)
    print("================")

    print("Large File Text:")
    print(large_file_text)


if __name__ == "__main__":
    main()
