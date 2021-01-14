# Por Santiago Rojas
import requests
import sys

def main():
    print("Desafio Backend Houm")
    print("Respuesta 1.")
    print(pregunta1())
    print("Respuesta 2.")
    print(pregunta2())
    print("Respuesta 3.")
    print(pregunta3())

def pregunta1():
    """
    Funcion para responder a la pregunta 1 del desafio backend de Houm

    Se retorna la cantidad de pokemones con el substring "at" y una "a" adicional
    en su nombre. Si el nombre tiene más de una "a" adicional, no se contara.

    (Se utilizo contains y replace para resolver la pregunta, tambien se puede
    obtener el mismo resultado utilizando expresiones regulares)
    """
    cnt = 0
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1118")

    if response:
        #se itera por cada uno de los nombres de los pokemones
        for pokemon in response.json()["results"]:

            if pokemon["name"].__contains__("at"):
                #Se elimina la primera aparicion de "at" en el nombre
                name_sin_at = pokemon["name"].replace("at","",1)

                if name_sin_at.__contains__("a"):
                    #Se elimina la primera aparicion de "a" en el nombre sin "at"
                    name_clean = name_sin_at.replace("a","",1)

                    if not name_clean.__contains__("a"):
                        #Si el nombre no contiene ninguna "a" adicional, se cuenta
                        cnt+=1
    else:
        print('Request fallido')
    
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

