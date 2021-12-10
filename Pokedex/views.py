from django.shortcuts import render
import requests


def index(request, id):
    # On initialise le context
    context = {}
    # On initialise le retour des erreurs
    context["error"] = ""

    # Système de vérification d'url pour la fonction de recherche
    check = str(request).find("=")
    if check != -1:
        test = str(request).split("=")
        numPoke = test[1]
        num = ""
        for c in numPoke:
            if c.isdigit():
                num = num + c
        id = num

    # Récupération de l'ID du Pokémon
    id = int(id)
    # On le stock à + 1 ou - 1 pour le système de navigation
    context["next"] = str(id + 1)
    context["previous"] = str(id - 1)
    # L'API PokeAPI envoie les pokémon à partir de 0 mais nous voulons à partir de 1
    id = id - 1

    # Petite vérification de l'id pour le système de navigation si on arrive au 151ème Pokémon
    if id > 149:
        context["last"] = 1
    # Petite vérification de l'id pour le système de navigation si on est au premier Pokémon
    if id < 1:
        context["first"] = 1
    # On utilise la vue uniquement si on est dans les 151 premiers Pokémon
    if (id < 151 and id > -1):
        # On transforme l'ID en String pour l'url
        id = str(id)
        # On récupère le pokémon via l'API
        r = requests.get("https://pokeapi.co/api/v2/pokemon?offset=" + id + "&limit=1")
        # On récupère le résultat
        results = r.json()

        # À partir d'ici tout une phase de récupération d'information
        # On récupère le nom et l'url du Pokémon pour ensuite récupérer ses informations
        for i in results['results']:
            context['name'] = i['name'].capitalize()
            context['url'] = i['url']

        p = requests.get(context['url'])
        pokeContent = p.json()

        types = {}
        for t in pokeContent['types']:
            name = t['type']['name'].capitalize()
            types[name] = name.capitalize()

        context["poketypes"] = types

        stats = pokeContent['stats']

        context['hp'] = stats[0]["base_stat"]
        context['speed'] = stats[5]["base_stat"]
        context['attack'] = stats[1]["base_stat"]
        context['defense'] = stats[2]["base_stat"]
        context['pokeheight'] = pokeContent['height']
        context['pokeweight'] = pokeContent['weight']
        context['specialAttack'] = stats[3]["base_stat"]
        context['specialDefense'] = stats[4]["base_stat"]

        # On récupère l'image
        images = pokeContent['sprites']
        context['sprite'] = images["front_default"]
    else:
        context["error"] = "Erreur d'id de Pokemon veuillez choisir un pokémon entre 1 et 151"

    return render(request, "index.html", context)
