Descripción de proyecto

Este programa tiene como objetivo proporcionar a los usuarios estadísticas relevantes de un artista en específico al igual que recomendar canciones, utilizando la API de Spotify. Al iniciar, el usuario ingresará a un menu que cuenta con 3 modulos, estadisticas de un usuario, recomendación de canciones y historial. El modulo de estadisticas de un usuario se encargará de buscar y recuperar datos importantes del artista, como su popularidad, número de seguidores, y los géneros musicales con los que está asociado. El modulo de recomendación de canciones solicita al usuario una lista de generos y artistas que usará para guiarse con las recomendaciones, por lo que el programa desplegara un listado de canciones junto a su artista, el historial estara disponible a partir de que se haga una petición del modulo de estadisticas.

Me parece interesante este proyecto debido a que ya existen programas que ya cuentan con esta función pero siempre se puede mejorar algo que ya existe.

El algoritmo consistirá de lo siguiente:
Entradas:
-Menu: eleccion (integer)
-Modulo de estadisticas: artista (string)
-Modulo de recomendacion: generos (string) , artista (string) 
Salida:
-Estadisticas del artista escogido 
-Recomendaciones del artista
-Historial

Proceso:

    1. Entrar al programa
    2. Se le presenta al usuario 3 opciones que escoger, estadisticas de un artista, recomendacion de canciones, o historial (no disponible si no hay datos en el historial)
     -. Modulo de estadisticas: se le solicita al usuario el nombre del artista que quiera obtener del artista 
     -. Modulo de recomendacion de canciones: se le solicita al usuario que ingrese los generos y artistas del que se quiere guiar con la recomendacion 
     -. Historial: el historial cuenta con todos los datos guardados del modulo de estadisticas.
    3. El usuario tiene capacidad de volver al menu o salir directamente 

Para poder acceder al archivo se tendra que descargar las siguientes librerias:
python-dotenv
requests

comandos para poder instalar las librerias necesitadas para ejecutar el archivo (en cmd):
pip install python-dotenv
pip install requests
