from gpiozero import DistanceSensor
import time
import logging
import board
import adafruit_dht
import subprocess

logging.basicConfig(
    filename = '/home/raspi/taller tic/log.txt',
    level = logging.INFO ,
    format = '%(asctime)s - %(levelname)s - %(message)s'
    )

script_path = '/home/raspi/taller tic/correct_sensor.sh'

result = subprocess.run([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

dhtDevice = adafruit_dht.DHT11(board.D16)


ds = DistanceSensor(20 , 21 , max_distance = 3, threshold_distance = 0.1)




while True:

    
    try:
        
        distancia_sensor = ds.distance 
        temperatura_celsius = dhtDevice.temperature
        humedad_ambiente = dhtDevice.humidity
        logging.info(f'La temperatura es de {temperatura_celsius:.3f}° celsius , La humedad en el ambiente es de {humedad_ambiente:.3f}%  , Objeto Más Cercano a {distancia_sensor:.3f} metros de distancia')
        time.sleep(3)
        
        
        
    except RuntimeError as error:
        logging.error(f'Error: {error}')
        time.sleep(3.0)
        continue
    
    except Exception as error:
        logging.error(f'Erorr:{error}')
        
    
    time.sleep(3)
    
if dhtDevice:
    ddhtDevice.exit()








        