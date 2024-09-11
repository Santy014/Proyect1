from dotenv import load_dotenv  
import os 
import base64
from requests import post , get 
import json

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret= os.getenv("CLIENT_SECRET")

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

token = get_token()
result = search_artist(token, "Dannylux")
artist_id = result["id"]
songs = get_song(token, artist_id)

for idx, song in enumerate(songs):
   print(f"{idx + 1 }. {song ['name']}")
    
class Usuario:
 def inicio(perfil,usuario,contraseña):
    perfil.usuario= usuario
    perfil.contraseña=contraseña
    perfil.artfav= []
    perfil.canfav= []
    perfil.generosfav= []

def agregar_art_fav(perfil, artista):
    perfil.artista_fav.append(artista)

def agregar_cancion_fav(perfil, cancion):
    perfil.cancion_fav.append(cancion)

def agregar_cancion_fav(perfil, genero):
    perfil.genero_fav.append(genero)

def registro():
    username=input("Ingrese su nombre de usuario: ")
    contraseña=input("Ingrese una contraseña segura: ")
    return Usuario(username,contraseña)
