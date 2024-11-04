import paramiko
import time

host = 'raspi3'
port = 22
usuario = 'raspi'
contraseña = 'raspi'

ruta_archivo_raspberry = '/home/raspi/taller tic/log.txt'
ruta_archivo_pc = r'C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\log.txt'

def descargar_archivo():
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        client.connect(host, port, username=usuario, password=contraseña)

        sftp = client.open_sftp()

        sftp.get(ruta_archivo_raspberry, ruta_archivo_pc)

        print('Archivo descargado')

        sftp.close()
        client.close()

    except Exception as error:
        print(f'Error al intentar conectar: {error}')


while True:
    descargar_archivo()
    time.sleep(3)

    respuesta = input("¿Deseas detener la descarga? (s/n): ").lower()
    if respuesta == "s":

        print("Descarga de logging detenida.")
        break
