# Speech to Text Using Python
This project is a simple project that can get the transcript of any voice file in any language using [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) library and Google Speech Recognition API.

## Project Files:
- Audio files
- audio_transcription.py
- main.py

### audio_transcription.py:
#### `AudioTranscription` Class:
This class can use the free API from Google to recognize a speech and return the text of an audio.
##### Class Methods:
- `standard_audio_file_transcriptor`:
  -- This method is used to get a standard audio file and return the transcript.
- `large_audio_file_transcriptor`:
  -- This method is used for getting the transcript of a large audio file (Usually more than 10MB)
  
  
## How to use this project?
Clone this repository into whatever location you want. Open the project folder in your Terminal (Windows/mac OS/Linux) or CMD (Windows), or PowerShell (Windows).

If you want to know how to open your project folder in the terminal, follow the links:
- [Windows Guide](https://www.wikihow.com/Open-a-Folder-in-Cmd)
- [Linux Guide](https://opensource.com/article/21/8/linux-change-directories)
- [macOS Guide](https://www.maketecheasier.com/open-folder-in-finder-from-mac-terminal)

After navigating to your project directory, run this command.
`venv\Scripts\activete`

You can use this project by replacing your files and running the `python main.py`.

If you have any questions or need help, you can find me at [mail@amir-nejad.com](mailto:mail@amir-nejad.com).
