import logging

logging.basicConfig(
    filename = '/home/raspi/taller tic/log.txt',
    level = logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
    
)

logging.debug('Este es un mensaje de depuracion')
logging.info('este es un mensaje informativo')
logging.warning('Este es un mensaje de advertencia')
logging.error('Este es un mensaje de error')
logging.critical('Este es un mensaje critico')
    