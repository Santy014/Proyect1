from dotenv import load_dotenv  
import os 
import base64
from requests import post , get 
import json
import requests 

historial= []  
load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret =os.getenv('CLIENT_SECRET')

def get_token():  
   auth_string = client_id + ":" + client_secret
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
   return{"Authorization" : "Bearer " + token}
def search_artist(token,artist):
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
   url= f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
   headers=get_auth_header(token)
   result=get(url, headers=headers)
   json_result=json.loads(result.content)["tracks"]
   return json_result
def get_stats(artist_id, token):
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

token = get_token()

def obtener_preferencias_usuario():
    generos = input("Introduce tus géneros musicales favoritos, separados por comas: ")
    artistas = input("Introduce tus artistas favoritos, separados por comas: ")
    
    generos_lista = [genero.strip() for genero in generos.split(",")]
    artistas_lista = [artista.strip() for artista in artistas.split(",")]
    
    return generos_lista, artistas_lista
def obtener_recomendaciones(token, generos, artistas):
    

    url = "https://api.spotify.com/v1/recommendations"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "seed_genres": ",".join(generos),  # Géneros que el usuario ingresó
        "seed_artists": ",".join(artistas),  # Artistas que el usuario ingresó
        "limit": 10  # Limitar a 10 recomendaciones
    }

    result = requests.get(url, headers=headers, params=params)
    
    if result.status_code == 200:
        recomendaciones = result.json()['tracks']
        return recomendaciones
    else:
        print(f"Error al obtener recomendaciones: {result.status_code}")
        return []
def artista_en_historial(artista, historial):
 for registro in historial:
    if registro[0] == artista:
       return True
 return False 
def mostrar_stats():
    while True:
        artist = input("Ingresa el artista del que deseas obtener las estadísticas, o escribe 'volver' para regresar al menú: ")

        if artist.lower() == "volver":
            return 

        
        if artista_en_historial(artist, historial):
            print(f"Ya has solicitado las estadísticas de {artist}. Mostrando estadísticas desde el historial.")
            
           
            for registro in historial:
                if registro[0] == artist:
                    print(f"Estadísticas del artista {registro[0]}:")
                    for estadistica in registro[1]:
                        print(f"- {estadistica[0]}: {estadistica[1]}")
            continue

        
        artist_data = search_artist(token, artist)

        if artist_data:
            artist_stats = get_stats(artist_data['id'], token)
            print(f"\nEstadísticas del artista {artist_stats['nombre']}:")
            print(f"- Popularidad: {artist_stats['popularidad']}")
            print(f"- Seguidores: {artist_stats['seguidores']}")
            print(f"- Géneros: {artist_stats['generos']}\n")

           
            top_tracks = get_song(token, artist_data['id'])
            print(f"Top Tracks de {artist_stats['nombre']}:")
            tracks_list = []
            for idx, track in enumerate(top_tracks, start=1):
                print(f"{idx}. {track['name']}")
                tracks_list.append(track['name'])

            
            historial.append([artist_stats['nombre'], [
                ["Seguidores", artist_stats['seguidores']],
                ["Popularidad", artist_stats['popularidad']],
                ["Géneros", artist_stats['generos']],
                ["Canciones más populares", tracks_list]
            ]])
        else:
            print("No se encontró el artista.")


        
def eliminar_artista_historial():
    if len(historial) == 0:
        print("El historial está vacío.")
        return
    
    print("Artistas en el historial:")
    for idx, registro in enumerate(historial):
        print(f"{idx + 1}. {registro[0]}")
    
    try:
        eleccion = int(input("Ingresa el número del artista que deseas eliminar del historial: "))
        if 1 <= eleccion <= len(historial):
            artista_eliminado = historial.pop(eleccion - 1)
            print(f"El artista {artista_eliminado[0]} ha sido eliminado del historial.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número.")
def menu():
   while True:
    eleccion=input('''
   ♪ Bienvenido al programa musical ♪
   Este es el menu, selecciona el numero del programa que deseeas:
   1. Estadisticas de un artista ♫
   2. Recomendador de musica ♫
   
   Si quieres salir solo escribe salir   
   ''')

    if eleccion == "1":
      mostrar_stats()

    elif eleccion == "2":
      obtener_recomendaciones()

    elif eleccion.lower() == "salir":
      print("Saliendo del programa.... ")
      break
    
menu()