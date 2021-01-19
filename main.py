# Por Santiago Rojas
import requests
import sys
import aiohttp
import asyncio


def main():
    print("Desafio Backend Houm")
    print("Respuesta 1.")
    print(pregunta1())
    print("Respuesta 2. Version Secuencial")
    print(pregunta2())
    print("Respuesta 2. Versión Asincrona")
    print(pregunta2_async())
    print("Respuesta 3. Versión Secuencial")
    print(pregunta3())
    print("Respuesta 3. Versión Asincrona")
    print(pregunta3_async())


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
    Answer to question 2 of Houm Challenge, secuential version.

    Multiple queries to the API are made to obtain the result. First one to get 
    the egg_groups of Raichu, then one for each egg_group. 

    Using the data structure set and returning its length, we make sure there are
    no duplicates.
    """
    try:
        arr = set()

        #get raichu egg_groups and check response
        response_raichu = requests.get("https://pokeapi.co/api/v2/pokemon-species/raichu/")
        response_raichu.raise_for_status()

        #loop through the egg_groups
        for egg_group in response_raichu.json()["egg_groups"]:

            #get species in the egg_group and check response
            response = requests.get(egg_group["url"])
            response.raise_for_status()

            #loop through each species of the egg_group
            for pokemon_specie in response.json()["pokemon_species"]:
                arr.add(pokemon_specie["name"])
    except Exception:
        print("Request fallido")
    finally:
        return len(arr)


def pregunta2_async():
    """
    Answer to question 2 of Houm Challenge, asynchronous version.

    Multiple queries to the API are made to obtain the result. First one to get 
    the egg_groups of Raichu, then one for each egg_group. The latter are done 
    asynchronically for better performance.

    Using the data structure set and returning its length, we make sure there are
    no duplicates.
    """
    try:
        arr = set()

        #get raichu egg_groups and check response
        response_raichu = requests.get("https://pokeapi.co/api/v2/pokemon-species/raichu/")
        response_raichu.raise_for_status()

        async def get_species_from_egg_group(session, url):
            """
            Async function to get the species from a specific egg_group
            """
            async with session.get(url) as response:
                wait_response = await response.json()
                return wait_response["pokemon_species"]
            
        async def get_all_species(egg_groups):
            """
            Async function to get all the species from the array of egg_groups
            """
            async with aiohttp.ClientSession() as session:
                # async tasks to be performed
                tasks = []
                for egg_group in egg_groups:
                    async_response = get_species_from_egg_group(session, egg_group["url"])
                    tasks.append(async_response)
                
                #gather all the tasks
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                return responses
        
        async_response = get_all_species(response_raichu.json()["egg_groups"])
        #run coroutines concurrently
        all_species_by_egg_group = asyncio.run(async_response)

        #responses are bundled in a matrix, each row is a egg_group species
        for egg_group_species in all_species_by_egg_group:
            for pokemon in egg_group_species:
                arr.add(pokemon["name"])

    except Exception:
        print("Request fallido")
    finally:
        return len(arr)


def pregunta3():
    """
    Answer to question 3 of Houm Challenge, secuential version.

    To get the maximum and minimum, it'll loop through the list of pokemon already
    filtered by generation, reducing the number of calls to the API.
    The id of a pokemon can be obtain from the url.
    """
    try: 
        arr = [0, sys.maxsize]
        response_fighting = requests.get("https://pokeapi.co/api/v2/type/fighting")
        response_fighting.raise_for_status()

        for pokemon in response_fighting.json()["pokemon"]:
            if get_id_from_URL(pokemon["pokemon"]["url"]) <= 151:
                response = requests.get(pokemon["pokemon"]["url"])
                response.raise_for_status()

                weight = response.json()["weight"]
                if arr[0] < weight:
                    arr[0] = weight
                if arr[1] > weight:
                    arr[1] = weight
    except Exception:
        print("Request fallido")
    finally:
        return arr


def pregunta3_async():
    """
    Answer to question 3 of Houm Challenge, asynchronical version.

    To get the maximum and minimum, it'll loop through the list of pokemon already
    filtered by generation, reducing the number of calls to the API. Each of this 
    calls to the API are made asynchronically for better performance.

    The id of a pokemon can be obtain from the url.
    """
    try:
        response_fighting = requests.get("https://pokeapi.co/api/v2/type/fighting")
        response_fighting.raise_for_status()

        async def get_pokemon(session, url):
            """
            Async function to get a pokemon from a url
            """
            async with session.get(url) as response:
                wait_response = await response.json()
                return wait_response["weight"]
        
        async def get_all_pokemon(pokemons):
            """
            Async function to gather all pokemons(<=151)
            """
            async with aiohttp.ClientSession() as session:
                #async tasks to be perfomed
                tasks = []
                for pokemon in pokemons:
                    if get_id_from_URL(pokemon["pokemon"]["url"]) <= 151:
                        tasks.append(get_pokemon(session, pokemon["pokemon"]["url"]))
                
                #gather all tasks
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                return responses
        
        async_response = get_all_pokemon(response_fighting.json()["pokemon"])
        all_pokemons = asyncio.run(async_response)
    except Exception:
        print("Request fallido")
    finally:
        return [max(all_pokemons),min(all_pokemons)]


#Auxiliary Functions
def get_id_from_URL(url):
    arr = url.split("/")
    return int(arr[-2])



main()