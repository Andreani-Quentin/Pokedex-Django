from django.shortcuts import render
import requests


def index(request, id):
    check = str(request).find("=")


    if check != -1:
        test = str(request).split("=")
        numPoke = test[1]
        num = ""
        for c in numPoke:
            if c.isdigit():
                num = num + c
        id = num

    # On initialise le context
    context = {}
    # On initialise le retour des erreurs
    context["error"] = ""
    # Vérification de l'id afin de n'utiliser que les 151 premier Pokémon
    id = int(id)
    context["next"] = str(id + 1)
    context["previous"] = str(id - 1)
    id = id - 1

    if id > 149:
        context["last"] = 1

    if id < 1:
        context["first"] = 1

    if (id < 151 and id > -1):
        id = str(id)

        r = requests.get("https://pokeapi.co/api/v2/pokemon?offset=" + id + "&limit=1")
        results = r.json()

        for i in results['results']:
            context['name'] = i['name'].capitalize()
            context['url'] = i['url']

        p = requests.get(context['url'])
        pokeContent = p.json()

        for t in pokeContent['types']:
            context['poketypes'] = t['type']['name'].capitalize()

        stats = pokeContent['stats']

        context['hp'] = stats[0]["base_stat"]
        context['speed'] = stats[5]["base_stat"]
        context['attack'] = stats[1]["base_stat"]
        context['defense'] = stats[2]["base_stat"]
        context['pokeheight'] = pokeContent['height']
        context['pokeweight'] = pokeContent['weight']
        context['specialAttack'] = stats[3]["base_stat"]
        context['specialDefense'] = stats[4]["base_stat"]

        images = pokeContent['sprites']
        context['sprite'] = images["front_default"]

        # print(context)
    else:
        context["error"] = "Erreur d'id de Pokemon veuillez choisir un pokémon entre 1 et 151"

    return render(request, "index.html", context)
