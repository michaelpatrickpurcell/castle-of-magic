import numpy as np
from itertools import product, combinations

bell = ("silent", "ringing")
book = ("closed", "open")
candle = ("unlit", "lit")
arcana = list(product(bell, book, candle))

kida = ("none", "dragon", "eagle", "wolf")
marus = ("none", "dragon", "eagle", "wolf")
sorrell = ("none", "dragon", "eagle", "wolf")
countries = list(product(kida, marus, sorrell))

amulet = (0,1,2,3,4,5)
crown = (0,1,2,3,4,5)
scepter = (0,1,2,3,4,5)
regalia = product(amulet, crown, scepter)
regalia = list(filter(lambda x: len(set(x)) > 1, regalia))


homeland = ("kida", "marus", "sorrell", "hydra")
guilds = ("dragon", "eagle", "wolf")
characters = list(product(homeland, guilds))
characters.append(("monster","monster"))

character_dict = {i: character for i,character in enumerate(characters)}
character_rev_dict = {character: i for i,character in enumerate(characters)}

six_characters = list(combinations(characters, 6))

six_player_games = product(six_characters, arcana, countries, regalia)
n = len(six_characters) * len(arcana) * len(countries) * len(regalia)
#game_list = list(six_player_games)

def six_player_scores(game):
    characters = game[0]
    scores = {c:0 for c in characters}
    arcana = game[1]
    guilds = game[2]
    regalia = game[3]
    for i,character in enumerate(characters):
        for country, guild in zip(*(("kida", "marus", "sorrell"), guilds)):
            if guild == character[1]:
                scores[character] += 1
                if country == character[0]:
                    scores[character] += 1
        for country, j in zip(*(("kida", "marus", "sorrell"), regalia)):
            if j == i:
                scores[character] += 1
                if country == character[0]:
                    scores[character] += 0
    if arcana == ("silent", "closed", "unlit"):
        # Monster rampages
        for c in characters:
            if c[0] == "monster":
                scores[c] = 10
            elif c[0] == "hydra":
                scores[c] = 1
            else:
                scores[c] = 0
    elif arcana == ("silent", "closed", "lit"):
        # Candle controls monster
        scores[characters[regalia[2]]] += 1
    elif arcana == ("silent", "open", "unlit"):
        # Book controls monster
        scores[characters[regalia[1]]] += 1
    elif arcana == ("silent", "open", "lit"):
        # Bell killed
        c = characters[regalia[0]]
        scores[c] = 0
        for c in characters:
            if c[0] == "monster":
                scores[c] = 10
            elif c[0] == "hydra":
                scores[c] += 1
    elif arcana == ("ringing", "closed", "unlit"):
        # Bell controls monster
        scores[characters[regalia[0]]] += 1
    elif arcana == ("ringing", "closed", "lit"):
        # Book killed
        c = characters[regalia[1]]
        scores[c] = 0
        for c in characters:
            if c[0] == "monster":
                scores[c] = 10
            elif c[0] == "hydra":
                scores[c] += 1
    elif arcana == ("ringing", "open", "unlit"):
        # Candle killed
        c = characters[regalia[2]]
        scores[c] = 0
        for c in characters:
            if c[0] == "monster":
                scores[c] = 10
            elif c[0] == "hydra":
                scores[c] += 1
    elif arcana == ("ringing", "open", "lit"):
        # Monster banished
        pass
    else:
        raise ValueError("Invalid arcana setting")
    return scores


# Each row corresponds to a possible game
# Each column corresponds to a given character
# The values correspond to a given characters score in a given game


results = -1*np.ones((n, len(characters)))
for i in range(n):
    if i % 1000000 == 0:
        print(i)
    game = next(six_player_games)
    scores = six_player_scores(game)
    for c in scores:
        results[i][character_rev_dict[c]] = scores[c]

winning_scores = np.max(results, axis=1)

wins = np.zeros(results.shape[1])
for i in range(results.shape[1]):
    print(i)
    wins[i] = np.sum(results[:,i] == winning_scores)
