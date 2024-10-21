from dotenv import load_dotenv  
import os 
import base64
from requests import post , get 
import json
import requests 

HISTORIAL = []  
load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET =os.getenv('CLIENT_SECRET')

def get_token():  
   #Esta funcion obtiene la token de acceso a la API de Spotify
   auth_string = CLIENT_ID + ":" + CLIENT_SECRET
   auth_bytes = auth_string.encode("utf-8") 
   auth_base64= str(base64.b64encode(auth_bytes), "utf-8")

   url = "https://accounts.spotify.com/api/token"
   headers = {
      "Authorization" : "Basic " + auth_base64,
      "Content-Type" : "application/x-www-form-urlencoded"
   }
   data = {'grant_type' : "client_credentials"}
   result=post(url, headers=headers, data=data )
   json_result = json.loads(result.content)
   token = json_result["access_token"]  
   return token
def get_auth_header(token):
   #Esta funcion devuelve el formato requerido para hacer solicitudes, utilizando el token obtenido por la funcion pasada 
   return{"Authorization" : "Bearer " + token}
def search_artist(token,artist):
   #Esta funcion encuentra el id de un artista a partir de su nombre, proporcionado por el usuario en la funcion mostrar_stats()
   url= "https://api.spotify.com/v1/search"
   headers = get_auth_header(token)
   query= f"?q= {artist} &type=artist&limit=1" 

   query_url = url + query
   result = get(query_url, headers=headers)
   json_result = json.loads(result.content)["artists"]["items"]
 
   if len(json_result) == 0:
      print(f"No se ha encontrado al artista llamado/a {artist}")
      return None
   
   return json_result[0]
def get_song(token, artist_id):
   #Esta funcion proporciona los top tracks del artista a partir del artist_id
   url= f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
   headers=get_auth_header(token)
   result=get(url, headers=headers)
   json_result=json.loads(result.content)["tracks"]
   return json_result
def get_stats(artist_id, token):
   #En este funcion se obtienen las estadisticas del artista 
   url = f"https://api.spotify.com/v1/artists/{artist_id}"
   headers=get_auth_header(token)
   result=get(url, headers=headers)
   artist_data=result.json()
   stats = {
   "nombre": artist_data['name'],
   "popularidad": artist_data['popularity'],
   "seguidores": artist_data['followers']['total'],
   "generos": artist_data['genres']
   }
   return stats 

TOKEN =get_token()

def obtener_preferencias_usuario():
    #En esta funcion se le solicitara al usuario sus preferencias, que se utilizara para recomendar canciones
    generos = input("Introduce tus géneros musicales favoritos, separados por comas: (El numero maximo de generos y artistas combinados es 5)")
    artistas = input("Introduce tus artistas favoritos, separados por comas: ")
    
    generos_lista = [genero.strip() for genero in generos.split(",")]
    artistas_lista = [artista.strip() for artista in artistas.split(",")]
    
    total= len(generos_lista) + len(artistas_lista)

    if total > 5:
       print("Haz excedido el limite que permite el API de Spotify, 5 exactos combinando generos y artistas ")
    else: 
     return generos_lista, artistas_lista
def obtener_recomendaciones(token, generos, artistas):
    #Aqui se obtiene la lista de recomnedaciones, basandose en los artistas y generos que el usuario proporciono en obtener_preferencias_usuario
    artist_ids = convert_art2id(token, artistas)
    if not artist_ids and not generos:
       print("debes ingresar por lo mnenos un artista o genero valido")
       return [] 

    url = "https://api.spotify.com/v1/recommendations"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "seed_genres": ",".join(generos),  
        "seed_artists": ",".join(artist_ids),  
        "limit": 10  
    }

    result = requests.get(url, headers=headers, params=params)
    
    if result.status_code == 200:
        recomendaciones = result.json()['tracks']
        return recomendaciones
    else:
        print(f"Error al obtener recomendaciones: {result.status_code}")
        return []
def mostrar_stats():
    #Este es el modulo de estadisticas, el usuario introduce el nombre del artista el programa te dara las estadisticas del artista
    while True:
        artist = input("Ingresa el artista del que deseas obtener las estadísticas, o escribe 'volver' para regresar al menú: ")

        if artist.lower() == "volver":
            return 

        artist_data = search_artist(TOKEN, artist)

        if artist_data:
            artist_stats = get_stats(artist_data['id'], TOKEN)
            print(f"\nEstadísticas del artista {artist_stats['nombre']}:")
            print(f"- Popularidad: {artist_stats['popularidad']}")
            print(f"- Seguidores: {artist_stats['seguidores']}")
            print(f"- Géneros: {artist_stats['generos']}\n")

           
            top_tracks = get_song(TOKEN , artist_data['id'])
            print(f"Top Tracks de {artist_stats['nombre']}:")
            tracks_list = []
            for idx, track in enumerate(top_tracks, start=1):
                print(f"{idx}. {track['name']}")
                tracks_list.append(track['name'])

            data = {
            "tipo": "estadísticas",
            "artista": artist_stats['nombre'],
            "seguidores": artist_stats['seguidores'],
            "popularidad": artist_stats['popularidad'],
            "generos": artist_stats['generos'],
            "canciones_populares": tracks_list  
        }
        HISTORIAL.append(data)      
def convert_art2id(token, artistas):
    #Esta funcion trabaja dentro de obtener recomendaciones, se utiliza para convertir una lista de artistas a una lista de id's
    artist_ids = []

    for artista in artistas:
        artist_data = search_artist(token, artista)  
        if artist_data:
            artist_ids.append(artist_data['id'])
        else:
            print(f"No se encontró el artista: {artista}")
 
    return artist_ids
def mostrar_recomendaciones(recomendaciones):
   #Esta funcion recibe lo que obtener_recomendaciones obtuvo y muestra al usuario las recomendaciones en formato de lista
   if recomendaciones: 
      print("Estas son tus recomendaciones musicales: ")
      for idx, track in enumerate(recomendaciones, start=1):
         print(f"{idx}. {track['name']} - {track['artists'][0]['name']}")
   else:
      print("no se encontraron recomendaciones") 
def get_genres(token):
    #Esta funcion muestra al usuario los generos disponibles que reconoce spotify
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    if result.status_code == 200:
        genres = result.json()['genres']
        print("Generos válidos:", genres)
    else:
        print(f"Error al obtener géneros: {result.status_code}")
def mostrar_historial():
#Esta funcion muestra el historial al usuario, dentro del menu
  if not HISTORIAL: 
        print("El historial está vacío.")
        return
    
  print("\nHistorial de Búsquedas y Recomendaciones:")
  for idx, item in enumerate(HISTORIAL, start=1):
        if "tipo" in item:
            if item["tipo"] == "estadísticas":
                print(f"{idx}. Estadísticas del artista {item['artista']}:")
                print(f"   - Popularidad: {item['popularidad']}")
                print(f"   - Seguidores: {item['seguidores']}")
                print(f"   - Géneros: {', '.join(item['generos'])}")
                print(f"   - Canciones más populares: {', '.join(item['canciones_populares'])}")
            elif item["tipo"] == "recomendaciones":
                print(f"{idx}. Recomendaciones basadas en géneros {', '.join(item['generos'])} y artistas {', '.join(item['artistas'])}:")
                print(f"   - Canciones recomendadas: {', '.join(item['recomendaciones'])}")
def menu():
   #Esta funcion es el corazon del programa, muestra un menu  que despliega al usuario multiples modulo a las que este puede ingresar
   while True:
    eleccion=input('''
   ♪ Bienvenido al programa musical ♪
   Este es el menu, selecciona el numero del programa que deseeas:
   1. Estadisticas de un artista ♫
   2. Recomendador de musica ♫
   3. Historial de solicitudes 
                   
   Si quieres salir solo escribe salir   
   ''')

    if eleccion == "1":
      mostrar_stats()

    elif eleccion == "2":
       recomendador_de_musica()
    
    elif eleccion == "3":
      mostrar_historial()

    elif eleccion.lower() == "salir":
      print("Saliendo del programa.... ")
      break
def recomendador_de_musica():
   #Esta funcion sirve para juntar varias funciones auxiliares que pertenecen al modulo de recomendacion de musica
   get_genres(TOKEN)
   generos, artistas = obtener_preferencias_usuario()
   recomendaciones = obtener_recomendaciones(TOKEN, generos, artistas)
   mostrar_recomendaciones(recomendaciones)

menu()
