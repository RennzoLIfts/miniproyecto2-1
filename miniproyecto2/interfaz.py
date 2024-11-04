import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDial, QLCDNumber, QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap
 
class LEDControlApp(QWidget):
    def __init__(self):
        super().__init__()
       

        self.setWindowTitle("Control de LEDs")
       
        # Layout principal
        layout = QVBoxLayout()
 
        # Botón para encender/apagar el LED digital (simulación)
        self.btn_toggle_led = QPushButton("ENCENDER LEDs")
        self.btn_toggle_led.clicked.connect(self.toggle_led)
        layout.addWidget(self.btn_toggle_led)
        self.led_on = True  # Estado inicial del LED (encendido)
 
        # Dial para ajustar la luminosidad del LED (simulación)
        self.dial_brightness = QDial()
        self.dial_brightness.setRange(0, 100)
        self.dial_brightness.valueChanged.connect(self.change_brightness)
        layout.addWidget(self.dial_brightness)
 
        # QLCDNumber para mostrar el valor del dial
        self.lcd_display = QLCDNumber()
        layout.addWidget(self.lcd_display)
 
        # Conectar el dial para mostrar el valor en el LCD
        self.dial_brightness.valueChanged.connect(self.lcd_display.display)
 
        # Imágenes y textos
        self.images = [{"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen1.png", "text": "Perrito Feliz"},
                       {"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen2.png", "text": "Perritos bebes"},
                       {"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen3.png", "text": "Perrito Gordito"},  
                       {"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen4.png", "text": "Perrito Alto"},
                       {"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen5.png", "text": "Perrito Jugando"},
                       {"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen6.png", "text": "Perrito Triste"},
                       {"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen7.png", "text": "Perrito pequeño"},
                       {"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen8.png", "text": "Perrito corriendo"},
                       {"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen9.png", "text": "Perrito comiendo"},
                       {"image": r"C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\fotosinterfaz\imagen10.png", "text": "Perrito Dormilón"}]
           
        # QLabel para mostrar la imagen y el texto
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)
 
        self.text_label = QLabel()
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_label)
 
        # Botón para activar/desactivar el temporizador de cambio de imagen
        self.btn_toggle_timer = QPushButton("INICIAR CAMBIO DE IMAGENES")
        self.btn_toggle_timer.clicked.connect(self.toggle_timer)
        layout.addWidget(self.btn_toggle_timer)
       
        # Configuración del temporizador para cambiar imágenes
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_image)
 
        # Configuración final de la ventana
        self.setLayout(layout)
 
        # Tamaño fijo de las imágenes
        self.image_size = 200  # Ajusta este valor para cambiar el tamaño de las imágenes
 
    # Función para simular el encendido/apagado del LED digital
    def toggle_led(self):
        self.led_on = not self.led_on
        if self.led_on:
            self.btn_toggle_led.setText("ENCENDER LEDs")
            print("LED DIGITAL APAGADO")
        else:
            self.btn_toggle_led.setText("APAGAR LEDs")
            print("LED DIGITAL ENCENDIDO")
 
    # Función para simular el cambio de luminosidad del LED
    def change_brightness(self, value):
        print(f"Brillo ajustado a: {value}")
 
    # Función para alternar el temporizador de cambio de imagen
    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn_toggle_timer.setText("INICIAR CAMBIO DE IMAGEN")
        else:
            self.change_image()
            self.timer.start(5000)  # Cambia cada segundo
            self.btn_toggle_timer.setText("DETENER CAMBIO DE IMAGEN")
 
    # Función para cambiar la imagen y el texto en la interfaz
    def change_image(self):
        selected_image = random.choice(self.images)
        pixmap = QPixmap(selected_image["image"])
        scaled_pixmap = pixmap.scaled(self.image_size, self.image_size, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)
        self.text_label.setText(selected_image["text"])
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LEDControlApp()
    window.show()
    sys.exit(app.exec())