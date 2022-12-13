import audio_transcription as at


def main():
    small_filename = "16-122828-0002.wav"
    large_filename = "7601-291468-0006.wav"

    audio_transcription = at.AudioTranscription()

    small_file_text = audio_transcription.standard_audio_file_transcriptor(small_filename)
    large_file_text = audio_transcription.large_audio_file_transcriptor(large_filename)

    # print("Small File Text:")
    # print(small_file_text)
    print("================")

    print("Large File Text:")
    print(large_file_text)


if __name__ == "__main__":
    main()
