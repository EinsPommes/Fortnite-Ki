from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                                 QPushButton, QLabel, QProgressBar, QGroupBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
import cv2
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fortnite KI Controller")
        self.setMinimumSize(1200, 800)
        
        # Hauptwidget und Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Linke Seite - Spielansicht und Status
        left_panel = QVBoxLayout()
        
        # Spielansicht
        self.game_view = QLabel()
        self.game_view.setMinimumSize(800, 450)
        self.game_view.setStyleSheet("border: 2px solid gray;")
        left_panel.addWidget(self.game_view)
        
        # Statusanzeige
        status_group = QGroupBox("Spielstatus")
        status_layout = QHBoxLayout()
        
        # Gesundheit
        health_layout = QVBoxLayout()
        health_layout.addWidget(QLabel("Gesundheit:"))
        self.health_bar = QProgressBar()
        self.health_bar.setStyleSheet("QProgressBar {text-align: center;}")
        health_layout.addWidget(self.health_bar)
        status_layout.addLayout(health_layout)
        
        # Schild
        shield_layout = QVBoxLayout()
        shield_layout.addWidget(QLabel("Schild:"))
        self.shield_bar = QProgressBar()
        self.shield_bar.setStyleSheet("QProgressBar {text-align: center;}")
        shield_layout.addWidget(self.shield_bar)
        status_layout.addLayout(shield_layout)
        
        # Materialien
        mats_layout = QVBoxLayout()
        mats_layout.addWidget(QLabel("Materialien:"))
        self.mats_bar = QProgressBar()
        self.mats_bar.setMaximum(999)
        self.mats_bar.setStyleSheet("QProgressBar {text-align: center;}")
        mats_layout.addWidget(self.mats_bar)
        status_layout.addLayout(mats_layout)
        
        status_group.setLayout(status_layout)
        left_panel.addWidget(status_group)
        
        layout.addLayout(left_panel)
        
        # Rechte Seite - Steuerung
        right_panel = QVBoxLayout()
        
        # KI-Steuerung
        control_group = QGroupBox("KI-Steuerung")
        control_layout = QVBoxLayout()
        
        # Start/Stop Button
        self.start_button = QPushButton("KI Starten")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.toggle_ai)
        control_layout.addWidget(self.start_button)
        
        # Trainingsmodus
        self.train_button = QPushButton("Training Starten")
        self.train_button.setCheckable(True)
        self.train_button.clicked.connect(self.toggle_training)
        control_layout.addWidget(self.train_button)
        
        # Modell laden/speichern
        self.load_button = QPushButton("Modell Laden")
        control_layout.addWidget(self.load_button)
        
        self.save_button = QPushButton("Modell Speichern")
        control_layout.addWidget(self.save_button)
        
        control_group.setLayout(control_layout)
        right_panel.addWidget(control_group)
        
        # Statistiken
        stats_group = QGroupBox("Statistiken")
        stats_layout = QVBoxLayout()
        
        self.kills_label = QLabel("Eliminierungen: 0")
        stats_layout.addWidget(self.kills_label)
        
        self.placement_label = QLabel("Platzierung: -")
        stats_layout.addWidget(self.placement_label)
        
        self.avg_placement_label = QLabel("Ø Platzierung: -")
        stats_layout.addWidget(self.avg_placement_label)
        
        stats_group.setLayout(stats_layout)
        right_panel.addWidget(stats_group)
        
        # Log-Bereich
        log_group = QGroupBox("Log")
        log_layout = QVBoxLayout()
        self.log_label = QLabel()
        self.log_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.log_label.setWordWrap(True)
        self.log_label.setStyleSheet("background-color: white; padding: 5px;")
        log_layout.addWidget(self.log_label)
        log_group.setLayout(log_layout)
        right_panel.addWidget(log_group)
        
        layout.addLayout(right_panel)
        
        # Timer für Updates
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui)
        self.update_timer.start(100)  # Alle 100ms aktualisieren
        
        self.ai_running = False
        self.training_mode = False
        
    def toggle_ai(self, checked):
        self.ai_running = checked
        self.start_button.setText("KI Stoppen" if checked else "KI Starten")
        self.log_message("KI " + ("gestartet" if checked else "gestoppt"))
        
    def toggle_training(self, checked):
        self.training_mode = checked
        self.train_button.setText("Training Stoppen" if checked else "Training Starten")
        self.log_message("Trainingsmodus " + ("aktiviert" if checked else "deaktiviert"))
        
    def update_ui(self):
        # Aktualisiere Spielansicht
        # TODO: Implementiere Screenshot-Anzeige
        
        # Aktualisiere Status
        self.health_bar.setValue(100)  # Beispielwerte
        self.shield_bar.setValue(50)
        self.mats_bar.setValue(500)
        
    def log_message(self, message):
        current_text = self.log_label.text()
        new_text = f"{message}\n{current_text}"
        # Beschränke auf die letzten 10 Zeilen
        lines = new_text.split("\n")[:10]
        self.log_label.setText("\n".join(lines))
        
    def update_game_view(self, frame):
        """Aktualisiere die Spielansicht mit einem neuen Frame."""
        if frame is not None:
            # Konvertiere das OpenCV-Frame in ein QPixmap
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(self.game_view.size(), 
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            self.game_view.setPixmap(scaled_pixmap)
            
    def update_stats(self, kills, placement, avg_placement):
        """Aktualisiere die Statistikanzeige."""
        self.kills_label.setText(f"Eliminierungen: {kills}")
        self.placement_label.setText(f"Platzierung: {placement}")
        self.avg_placement_label.setText(f"Ø Platzierung: {avg_placement:.1f}")
