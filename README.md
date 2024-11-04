# miniproyecto2
Este es el codigo utilizado, junto con las funciones más importantes y su explicación. partiendo por las funciones base tenemos a

toggle_led(): Esta función alterna entre encender y apagar un LED digital simulado. Cambia el texto del botón entre "ENCENDER LEDs" y "APAGAR LEDs" y muestra mensajes de estado en la consola.
Funcionalidad relevante: Es una simulación de encendido y apagado, con un cambio de texto en el botón según el estado del LED.

change_brightness(value): Esta función ajusta la luminosidad del LED simulado según el valor del dial. Muestra en consola el nivel de brillo seleccionado.
Funcionalidad relevante: Simula el ajuste de luminosidad del LED con el dial, y el valor se visualiza en un display LCD (QLCDNumber), haciendo que los usuarios vean los cambios en tiempo real.

toggle_timer(): Esta función activa o desactiva el temporizador que controla el cambio automático de las imágenes en pantalla.
Funcionalidad relevante: Controla el temporizador (QTimer) que determina el cambio automático de imágenes cada 5 segundos (configurable). Al detener el temporizador, cambia el texto del botón a "INICIAR CAMBIO DE IMAGEN", y al activarlo, lo cambia a "DETENER CAMBIO DE IMAGEN".

change_image(): Esta función Cambia la imagen y el texto mostrados en la interfaz de usuario de manera aleatoria. 
Funcionalidad relevante: Selecciona al azar una imagen y un texto de una lista de diccionarios self.images, redimensiona la imagen y actualiza la visualización. Esto permite una presentación cíclica y dinámica de imágenes.
