from dotenv import load_dotenv  
import os 
import base64
from requests import post , get 
import json

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

# IDEA>>>>>country=input('De que pais deseas los top tracks?, introducir el pais correctamente')
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
result = search_artist(token, "Dannylux")
artist_id = result["id"]
songs = get_song(token, artist_id)

for idx, song in enumerate(songs):
   print(f"{idx + 1 }. {song ['name']}")
    
def registro():
    username=str(input("Ingrese su nombre de usuario: "))
    contraseña=str(input("Ingrese una contraseña segura: "))
    
registro()

def mostrar_stats():
 
 while True: 
   artist=input("Ingresa el artista del que deseas obtener las estadisticas, si deseas salir solo escribe salir :")

   if artist.lower() == "salir":
      print("Saliendo del programa :C")
      break

   artist=search_artist(token,artist)

   if artist:
      artist_stats= get_stats(artist[id],token)
      print(f"\n Estadisticas del artista {artist_stats['nombre']}:")
      print(f"-Popularidad: {artist_stats['popularidad']}")
      print(f"-Seguidores: {artist_stats['seguidores']}")
      print(f"-Generos: {artist_stats['generos']}\n")

mostrar_stats()