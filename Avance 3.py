## Iniciar con el login
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

DatosInicio=registro()
