# Por Santiago Rojas
import requests

def main():
    print("Desafio Backend Houm")
    print("Respuesta 1.")
    print("Respuesta 2.")
    print(pregunta2())
    print("Respuesta 3.")


def pregunta2() -> int:
    """
    Funcion para responder a la pregunta 2 del desafio backend de Houm.

    """
    #Obtener egg_groups de raichu
    responseRaichu = requests.get("https://pokeapi.co/api/v2/pokemon-species/raichu/")
    print(responseRaichu)
    if responseRaichu:
        print('Request is successful.')
        print(responseRaichu.json()["id"])
        print(responseRaichu.json()["egg_groups"])
        #egg_groups = responseRaichu.json()["egg_groups"]
    else:
        print('Request returned an error.')

    
    #Con los egg_groups, obtenemos las especies
    arr=[]
    for egg_group in responseRaichu.json()["egg_groups"]:
        response = requests.get(egg_group["url"])
        if response:
            print('Request is successful.')
            for pokemon_specie in response.json()["pokemon_species"]:
                #Check for duplicates
                if not pokemon_specie["name"] in arr:
                    arr.append(pokemon_specie["name"])           
        else:
            print('Request returned an error.')

    print(arr)
    print(len(arr))

    #response = requests.get("https://pokeapi.co/api/v2/egg-group")

    
    #print(response.json())
    return 0


#Funciones Auxiliares
#def checkResponse(response)



main()

