import os
import sys
from datetime import datetime

from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog, QComboBox, QWidget, \
    QLabel, QSizePolicy, QGridLayout

from audio_transcription import AudioTranscription


class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.initialize_widgets()

        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.button, 0, 1)
        self.layout.addWidget(self.combo_label, 1, 0)
        self.layout.addWidget(self.combo_box, 1, 1)
        self.layout.addWidget(self.submit_button, 2, 0)

        self.setLayout(self.layout)
        self.show()

    def initialize_widgets(self):
        self.filename = ""
        self.language = "en-US"

        self.label = QLabel("Choose an audio file. Allowed files: .mp3, .ogg, and .wav", self)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Choose File", self)
        self.button.clicked.connect(lambda: self.openDialog())

        self.combo_label = QLabel("Choose audio language:", self)
        self.combo_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.combo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["English", "Persian"])
        self.combo_box.currentTextChanged.connect(lambda: self.setLanguage())

        self.submit_button = QPushButton("Get Transcription", self)
        self.submit_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        self.submit_button.clicked.connect(lambda: self.getTranscription())
        self.submit_button.setDisabled(True)

    def openDialog(self):
        fname = QFileDialog.getOpenFileName(
            self,
            "Open Audio File",
            "",
            "MP3 Files (*.mp3);; WAV Files (*.wav);; OGG Files (*.ogg)",
        )

        self.filename = fname[0]
        self.label.setText(f"{fname[0]}\n{fname[1]}")

        self.submit_button.setDisabled(False)

    def setLanguage(self):
        if str(self.combo_box.currentText()) == "Persian":
            self.language = "fa-IR"

    def getTranscription(self):
        audio_transcription = AudioTranscription()

        size = os.stat(self.filename).st_size / (1024 * 1024)

        self.submit_button.setDisabled(True)
        self.submit_button.setText("Processing...")

        print(self.filename)
        print(self.language)

        app.processEvents()
        if size > 5:
            transcription = audio_transcription.large_audio_file_transcriptor(self.filename, self.language)
        else:
            transcription = audio_transcription.standard_audio_file_transcriptor(self.filename, self.language)

        print(transcription)
        self.submit_button.setText("Writing output file...")
        app.processEvents()

        now_datetime = datetime.now()

        output_file = f"transcription_{now_datetime.year}{now_datetime.month}{now_datetime.day}_{now_datetime.hour}{now_datetime.minute}_{now_datetime.second}_{now_datetime.microsecond}.txt"

        try:
            with open(output_file, 'w', encoding="UTF-8") as f:
                f.write(transcription)
        except Exception as e:
            print(e)

        self.submit_button.setText(f"Output file saved as {output_file}")

        restart_button = QPushButton("Try for Another File")
        restart_button.setStyleSheet("QPushButton { font-size: 1.3em; font-weight: bold; }")
        restart_button.clicked.connect(lambda: self.restart())

        self.layout.addWidget(restart_button)

    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_gui = Window()
    main_gui.setWindowTitle("Speech Recognition App")
    main_gui.setFixedWidth(500)
    main_gui.show()
    sys.exit(app.exec())
