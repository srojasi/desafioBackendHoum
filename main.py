# Por Santiago Rojas
import requests
import sys

def main():
    print("Desafio Backend Houm")
    print("Respuesta 1.")
    print(pregunta1())
    #print("Respuesta 2.")
    #print(pregunta2())
    #print("Respuesta 3.")
    #print(pregunta3())

def pregunta1():
    """
    Answer to question 1 of Houm Challenge

    Returns the amount of pokemons with the substring "at" and an aditional "a"
    en its name. If the name has more than one aditional "a", the name will not
    be considered.
    """
    try:
        cnt = 0
        #get all pokemons names from api
        response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1118")

        #check for correct response
        response.raise_for_status()

        #loop through each pokemon name, and check the conditions
        for pokemon in response.json()["results"]:
            if "at" in pokemon["name"] and pokemon["name"].count("a") == 2:
                cnt += 1
    except Exception:
        print("Request fallido")
    finally:
        return cnt


def pregunta2():
    """
    Funcion para responder a la pregunta 2 del desafio backend de Houm.

    Se realizan multiples consultas a la API, una para obtener los egg_groups de raichu y 
    una consulta por cada egg_group obtenido anteriormente.

    Se retorna el el largo del arreglo que contiene todos los nombres de los pokemones que
    pueden procrear con raichu, el arreglo se crea para asegurarse que no hayan duplicados
    (si no, se podria hacer un contador nomas)
    """
    #Obtener egg_groups de raichu
    responseRaichu = requests.get("https://pokeapi.co/api/v2/pokemon-species/raichu/")
    if not responseRaichu:
        print('Request fallido')

    
    #Con los egg_groups, obtenemos las especies
    arr=[] #Arreglo que va contener todas las especies de pokemon buscadas
    for egg_group in responseRaichu.json()["egg_groups"]: #Se itera por los egg_groups
        response = requests.get(egg_group["url"])
        if response:
            for pokemon_specie in response.json()["pokemon_species"]:
                #Revision de duplicados
                if not pokemon_specie["name"] in arr:
                    arr.append(pokemon_specie["name"])           
        else:
            print('Request fallido')


    #Se retorna el largo del arreglo, un numero
    return len(arr)

def pregunta3():
    """
    Funcion para responder a la pregunta 3 del desafio backend de Houm.

    Para obtener el maximo y el minimo, se iterara una sola vez por el listado pokemones
    ya filtrados por generacion, reduciendo la cantidad de consultas a la API.
    Se puede obtener la id del pokemon desde la url de este.
    """
    arr = [0, sys.maxsize]
    responseFighting = requests.get("https://pokeapi.co/api/v2/type/fighting")
    if not responseFighting:
        print('Request fallido')

    for pokemon in responseFighting.json()["pokemon"]:
        if int(get_id_from_URL(pokemon["pokemon"]["url"])) <= 151:
            response = requests.get(pokemon["pokemon"]["url"])
            if response:
                peso = response.json()["weight"]
                if arr[0] < peso:
                    arr[0] = peso
                if arr[1] > peso:
                    arr[1] = peso
            else:
                print('Request fallido')

    return arr

#Funciones Auxiliares
def get_id_from_URL(url):
    arr = url.split("/")
    return arr[-2]

main()

