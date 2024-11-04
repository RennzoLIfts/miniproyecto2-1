import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import paramiko
import logging

# Configuración de conexión y rutas de archivos
host = 'raspi3'
port = 22
usuario = 'raspi'
contraseña = 'raspi'

ruta_archivo_raspberry = '/home/raspi/taller tic/log.txt'
ruta_promedios_raspberry = '/home/raspi/taller tic/promedios.txt'
ruta_archivo_pc = r'C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\log.txt'
ruta_promedios_pc = r'C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\promedios.txt'

# Logger para los promedios
promedios_logger = logging.getLogger("promedios_logger")
promedios_logger.setLevel(logging.INFO)

# Handler para el archivo de log de promedios
promedios_handler = logging.FileHandler(ruta_promedios_pc)
promedios_formatter = logging.Formatter('%(asctime)s - %(message)s')
promedios_handler.setFormatter(promedios_formatter)
promedios_logger.addHandler(promedios_handler)

# Logger separado para `paramiko` (archivo independiente para logs de conexión)
paramiko_logger = logging.getLogger("paramiko")
paramiko_handler = logging.FileHandler(
    r'C:\Users\Alvar\OneDrive\Escritorio\miniproyecto2\paramiko.log')
paramiko_logger.addHandler(paramiko_handler)
paramiko_logger.setLevel(logging.INFO)


def leer_datos():
    """Lee todos los datos disponibles en el archivo de log, los agrupa por intervalos de 5 minutos y los interpola."""
    datos = []

    with open(ruta_archivo_pc, 'r') as archivo:
        for linea in archivo:
            try:
                partes = linea.split(',')
                timestamp = datetime.strptime(
                    partes[0].strip(), "%Y-%m-%d %H:%M:%S")
                temperatura = float(partes[1].split('=')[1].strip())
                humedad = float(partes[2].split('=')[1].strip())
                distancia = float(partes[3].split('=')[1].strip())

                datos.append({
                    "Timestamp": timestamp,
                    "Temperature": temperatura,
                    "Humidity": humedad,
                    "Distance": distancia
                })

            except (IndexError, ValueError) as e:
                print(f"Error al procesar la línea: {linea.strip()}\n{e}")
                continue

    df = pd.DataFrame(datos)
    df.set_index("Timestamp", inplace=True)
    df = df.resample("5T").mean()
    df.interpolate(method='time', inplace=True)
    return df


def mostrar_grafico(datos):
    """Genera y muestra el gráfico de temperatura, humedad y distancia en intervalos de 5 minutos."""
    plt.figure(figsize=(10, 6))
    plt.plot(datos.index, datos["Temperature"], label="Temperatura (°C)")
    plt.plot(datos.index, datos["Humidity"], label="Humedad (%)")
    plt.plot(datos.index, datos["Distance"], label="Distancia (m)")
    plt.xlabel("Tiempo")
    plt.ylabel("Valores")
    plt.title("Datos de Sensores (Agrupados cada 5 minutos)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def mostrar_tabla(datos):
    """Calcula y muestra los valores mínimos, máximos y promedio de cada variable."""
    print("\n--- Resumen de Datos Agrupados (Cada 5 minutos) ---")
    print(f"Temperatura - Mín: {datos['Temperature'].min():.3f}, Máx: {
          datos['Temperature'].max():.3f}, Prom: {datos['Temperature'].mean():.3f}")
    print(f"Humedad - Mín: {datos['Humidity'].min():.3f}, Máx: {
          datos['Humidity'].max():.3f}, Prom: {datos['Humidity'].mean():.3f}")
    print(f"Distancia - Mín: {datos['Distance'].min():.3f}, Máx: {
          datos['Distance'].max():.3f}, Prom: {datos['Distance'].mean():.3f}")


def guardar_promedios_y_enviar(datos):
    try:
        # Calcular los promedios
        promedio_temp = datos["Temperature"].mean()
        promedio_hum = datos["Humidity"].mean()
        promedio_dist = datos["Distance"].mean()

        # Registrar solo los promedios en el log de promedios
        promedios_logger.info(f"PdT = {promedio_temp:.3f}, PdH = {
                              promedio_hum:.3f}, PdD = {promedio_dist:.3f}")

    except RuntimeError as error:
        promedios_logger.error(f'Error: {error}')

    except Exception as error:
        promedios_logger.error(f'Error: {error}')

    print("Promedios registrados en el archivo de log en tu PC.")

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port, username=usuario, password=contraseña)

        sftp = client.open_sftp()
        sftp.put(ruta_promedios_pc, ruta_promedios_raspberry)
        sftp.close()
        client.close()

        print("Archivo de promedios acumulados enviado a la Raspberry Pi.")
    except Exception as e:
        print(f"Error al enviar el archivo: {e}")


def menu():
    """Muestra el menú principal de opciones."""
    while True:
        print("\nSeleccione una opción:")
        print("1. Mostrar gráfico")
        print("2. Mostrar tabla de valores")
        print("3. Enviar archivo de promedios acumulados a la Raspberry Pi")
        print("4. Terminar el proceso")

        opcion = input("Opción: ")

        datos = leer_datos()

        if opcion == '1':
            if not datos.empty:
                mostrar_grafico(datos)
            else:
                print("No se encontraron datos en el log.")
        elif opcion == '2':
            if not datos.empty:
                mostrar_tabla(datos)
            else:
                print("No se encontraron datos en el log.")
        elif opcion == '3':
            if not datos.empty:
                guardar_promedios_y_enviar(datos)
            else:
                print("No se encontraron datos en el log.")
        elif opcion == '4':
            print("Terminando el proceso...")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")


menu()
