import time
from gpiozero import LED, Buzzer
import re

# Configuración de pines para LEDs de cada variable
# Temperatura
led_temp_bajo = LED(2)     # LED azul
led_temp_medio = LED(3)    # LED verde
led_temp_alto = LED(4)     # LED rojo

# Humedad
led_hum_bajo = LED(17)     # LED azul
led_hum_medio = LED(27)    # LED verde
led_hum_alto = LED(22)     # LED rojo

# Distancia
led_dist_bajo = LED(10)    # LED azul
led_dist_medio = LED(9)    # LED verde
led_dist_alto = LED(11)    # LED rojo

# Buzzer
buzzer = Buzzer(5)

# Umbrales para cada variable
TEMP_BAJA, TEMP_MEDIA, TEMP_ALTA = 15, 25, 35
HUM_BAJA, HUM_MEDIA, HUM_ALTA = 30, 60, 90
DIST_CORTA, DIST_MEDIA, DIST_LARGA = 0.5, 2, 5

# Ruta del archivo de promedios en la Raspberry Pi
ruta_promedios_raspberry = '/home/raspi/taller tic/promedios.txt'


def leer_promedios():
    """Lee el último promedio registrado en el archivo de promedios y lo devuelve como un diccionario."""
    try:
        with open(ruta_promedios_raspberry, 'r') as archivo:
            ultima_linea = archivo.readlines()[-1]
            # Usamos expresiones regulares para extraer los valores de PdT, PdH y PdD
            temp_match = re.search(r'PdT = ([\d.]+)', ultima_linea)
            hum_match = re.search(r'PdH = ([\d.]+)', ultima_linea)
            dist_match = re.search(r'PdD = ([\d.]+)', ultima_linea)

            if temp_match and hum_match and dist_match:
                promedio_temp = float(temp_match.group(1))
                promedio_hum = float(hum_match.group(1))
                promedio_dist = float(dist_match.group(1))
                return {"Temperature": promedio_temp, "Humidity": promedio_hum, "Distance": promedio_dist}
            else:
                print("No se encontraron los promedios en la línea.")
                return None
    except Exception as e:
        print(f"Error al leer el archivo de promedios: {e}")
        return None


def actualizar_leds_y_buzzer(promedios):
    """Actualiza el estado de los LEDs y el buzzer según los umbrales de las variables."""
    # Apagar todos los LEDs antes de actualizar el estado
    led_temp_bajo.off()
    led_temp_medio.off()
    led_temp_alto.off()
    led_hum_bajo.off()
    led_hum_medio.off()
    led_hum_alto.off()
    led_dist_bajo.off()
    led_dist_medio.off()
    led_dist_alto.off()
    buzzer.off()

    # Temperatura
    if promedios["Temperature"] < TEMP_BAJA:
        led_temp_bajo.on()
        buzzer.beep(on_time=0.1, off_time=0.2, n=1)
    elif promedios["Temperature"] < TEMP_MEDIA:
        led_temp_medio.on()
        buzzer.beep(on_time=0.1, off_time=0.2, n=2)
    else:
        led_temp_alto.on()
        buzzer.beep(on_time=0.1, off_time=0.2, n=3)

    # Humedad
    if promedios["Humidity"] < HUM_BAJA:
        led_hum_bajo.on()
        buzzer.beep(on_time=0.2, off_time=0.3, n=1)
    elif promedios["Humidity"] < HUM_MEDIA:
        led_hum_medio.on()
        buzzer.beep(on_time=0.2, off_time=0.3, n=2)
    else:
        led_hum_alto.on()
        buzzer.beep(on_time=0.2, off_time=0.3, n=3)

    # Distancia
    if promedios["Distance"] < DIST_CORTA:
        led_dist_bajo.on()
        buzzer.beep(on_time=0.3, off_time=0.4, n=1)
    elif promedios["Distance"] < DIST_MEDIA:
        led_dist_medio.on()
        buzzer.beep(on_time=0.3, off_time=0.4, n=2)
    else:
        led_dist_alto.on()
        buzzer.beep(on_time=0.3, off_time=0.4, n=3)


def main():
    """Ejecuta el monitoreo continuo de los promedios y actualiza los LEDs y el buzzer según los umbrales."""
    while True:
        promedios = leer_promedios()
        if promedios:
            actualizar_leds_y_buzzer(promedios)

        # Esperar antes de la próxima lectura
        time.sleep(10)


if __name__ == "__main__":
    main()
