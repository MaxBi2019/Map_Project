"""
Maksym Bilyk -- All __modules reserved__
"""
from math import sin, cos, radians, sqrt, atan2
from random import shuffle


import folium
from data import city_set, country_set, data_base, code_dct
from loadingtools import loader, FUNNY_MESSAGES
from chatbot import to_end
from config import locations_file, world_file


NUM_OF_TOP = 10  # Number of nearby locations from 1 to 100
BAR_NUMBER = 100  # Number of bars in loader
MESSAGE_NUM = 7  # Number of funny messages


def get_titude(coord=0):
    """

    Parameters
    ----------
    coord = int [1] #latitude
    or
    coord = int [2] #longtitude


    Returns
    -------
    int [latitude] or int [longtitude]

    """
    msg = ["Latitude", "Longtitude"][coord]
    error = True
    while error:
        tude = input(f"{msg}\n>>> ").strip()
        try:
            tude = float(tude)
            if -180 <= tude <= 180:
                error = False
            else:
                print(f"{msg} should be from -180 to 180")
        except ValueError:
            print(f"Wrong input, {msg} should a float from -180 to 180")
    return tude


def distance(arg_1, arg_2):
    """

    Parameters
    ----------
    arg_1 = tuple(float, float) [location]
    arg_2 = tuple(float, float) [location]


    Returns
    -------
    float [distance]
    ---------------
    >>> distance((13, 12), (20, 25))
    1588.4503481022784
    >>> distance((53, 12), (128, 40))
    8051.72411702148
    >>> distance((13, 10), (47, 38))
    4592.447815048486
    """
    r_const = 6371e3
    lat_1, lon_1 = arg_1
    lat_2, lon_2 = arg_2
    delta_lat, delta_lon = abs(lat_1 - lat_2), abs(lon_1 - lon_2)
    alfa = sin(radians(delta_lat) / 2) ** 2 + \
           cos(radians(lat_1)) * cos(radians(lat_2)) * sin(radians(delta_lon) / 2) ** 2
    beta = 2 * atan2(sqrt(alfa), sqrt(1 - alfa))
    dist = r_const * beta
    return dist / 1000


def manage_data(arg, current_loc):
    """

    Parameters
    ----------
    arg = tuple(str, str) [city, country]
    current_loc = tuple(float, float) [location]


    Returns
    -------
    float [dist], tuple(float, float) [coordinates]
    """
    coords = tuple(map(float, data_base[arg].split(":")))
    dist = distance(current_loc, coords)
    return dist, coords


def combinations(lst_a, lst_b):
    """

    Parameters
    ----------
    lst_a = str [city]
    lst_b = str [country]


    Returns
    -------
    list(tuple(str, str), ..., tuple(str, str)) [(city, country), ..., (city, country)]
    """
    comb_set = set()
    for elm_a in lst_a:
        for elm_b in lst_b:
            if (elm_a, elm_b) in data_base:
                comb_set.add((elm_a, elm_b))
            if (elm_b, elm_a) in data_base:
                comb_set.add((elm_b, elm_a))
    return comb_set


def get_top_n(city_data, cities):
    """

    Parameters
    ----------
    city_data = dict(str: (str, int), ...,(str, int))
    [city: (film, year), (film, year),]

    cities = list((float, str, (float, float)), ..., (float, str, (float, float)))
    [(distance, city, location)..., ]


    Returns
    -------
    list((float, float), (str, str), ((str, str), ..., ), ...,)
    [(location, (city, country) ((title, year), ..,), ...,)]
    """
    repeated, top = [], []
    lst = sorted(city_data)
    for indx in range(1000):
        if lst[indx][2] not in repeated:
            top += [lst[indx]]
            repeated += [lst[indx][2]]
    top_n = top[:NUM_OF_TOP]
    final = []
    for cts in top_n:
        coords = cts[2]
        films = cities[cts[1]]
        final += [(coords, cts[1], films)]
    return final


def dino(current_loc, start=1, end=1241786):
    """

    Parameters
    ----------
    current_loc = tuple(float, float)
    start = int
    end = int


    Returns
    -------
    list((float, float), str, {(str, int), ..., }, ...,)
    [(location, city, {(title, year), ..,}, ...,)],

    dict(str: int, ..., )
    [(country: number of films, ..., )]

    """
    cities = {}
    city_data = []
    current_percent = 0
    shuffle(FUNNY_MESSAGES)
    with open(locations_file, encoding="utf-8", mode="r", errors="ignore") as database:
        mock = database.readline()[:10]
        while mock != "=" * 10:
            mock = database.readline()[:10]
        for num, line in enumerate(database):
            if num * (100 / end) > current_percent:
                current_percent += 1
                loader(BAR_NUMBER, current_percent, FUNNY_MESSAGES[:MESSAGE_NUM])
            if start <= num <= end:
                line = line.strip()
                *title_n_year, geo_data = location_ext(line)
                title_n_year = tuple(title_n_year)
                geo_data = set(geo_data)
                pairs = combinations(geo_data & city_set, geo_data & country_set)
                for cell in pairs:
                    if cell in cities:
                        cities[cell].add(title_n_year)
                    else:
                        geo_location = manage_data(cell, current_loc)
                        cities[cell] = {title_n_year}
                        city_data += [(geo_location[0], cell, geo_location[1])]
            if num > end:
                break
        return get_top_n(city_data, cities), get_statistics(cities)


def location_ext(arg):
    r"""

    Parameters
    ----------
    arg = str


    Returns
    -------
    str, int, (float, float) [title, year, location]
    -----------------------------------------------
    >>> location_ext("Film\t(2007)\tUSA")
    ('Film', 2007, ['USA'])
    >>> location_ext("Film\t(2007)\tUSA, New York")
    ('Film', 2007, ['USA', 'New York'])
    >>> location_ext("Film\t(????)\t{21092, 3323}\tUSA")
    ('Film', '????', ['USA'])
    """
    num = arg.find("    ")
    year = "????"
    right = False
    for indx in range(num, len(arg)-5):
        if arg[indx] == "(" and (arg[indx + 5] in [")", "/"]):
            if arg[indx + 1:indx + 5].isdigit():
                temp = arg[indx + 1:indx + 5]
                if int(temp) > 1500:
                    year = temp
                    right = arg[indx+5] == ")"
                    break
    anum = "(" + year + ")"*right
    title = arg.split(anum)[0].strip()
    location = arg.split(anum)[-1].strip()
    location = location.split("\t")[-1].split(", ")
    year = int(year) if year.isdigit() else year
    return title, year, location


def color_order(films, num_n=NUM_OF_TOP):
    """

    Parameters
    ----------
    films = list(((float, float), (str, str), {(str, int), ..., }), ...,)
    [(location, (city, country), {(title, year), ..,}, ...,)]
    num_n = int [top num locations]

    Returns
    -------
    list(int, ...)
    --------------
    >>> color_order([((2, 2), ("Lviv", "Ukraine"), {("film_1", 2002)})], 1)
    [('darkred', 'darkRed')]
    >>> color_order([((3, 3), ("BR", "Grm"), {("film_1", 2002)}), ((1, 1), ("Lv", "Ukr"),\
                                             {("film_2", 2005)})], 2)
    [('darkred', 'darkRed'), ('lightgreen', 'lime')]
    >>> color_order([((3, 3), ("BR", "Grm"), {("film_1", 2002)}), ((1, 1), ("Lv", "Ukr"),\
                                             {("film_2", 2005), ("film_3", 2001)})], 2)
    [('lightgreen', 'lime'), ('darkred', 'darkRed')]
    """
    const = num_n - 6
    numbers = (const//4, const%4) if const > 0 else (0, 0)
    colors = [('lightgreen', "lime")]*((num_n > 1) + numbers[0]) +\
              [('green', "limegreen")]*((num_n > 4) + numbers[0]) +\
              [('darkgreen', "darkgreen")]*((num_n > 2) + numbers[0]) +\
              [('lightred', "lightCoral")]*((num_n > 5) + numbers[0]) +\
              [('red', "red")]*((num_n > 3) + numbers[1]) +\
              [('darkred', "darkRed")]
    film_number = [len(elm[2]) for elm in films]
    order = [0] * num_n
    for indx in range(num_n-1, 0, -1):
        order[film_number.index(max(film_number))] = indx
        film_number[film_number.index(max(film_number))] = 0
    colors = [colors[indx] for indx in order]
    return colors


def layer_creator(stat):
    """
    Parameters
    ----------
    stat = dict(str: int, ..., ) [(country: number of films, ..., )]


    Returns
    -------
    object second_layer
    """
    top = []
    flm_inf = {}
    for elm in stat:
        if elm in code_dct:
            flm_inf[code_dct[elm]] = stat[elm]
            top += [stat[elm]]
    top.sort()
    delta = [top[indx] for indx in range((len(top) // 4), len(top), (len(top) // 4))] + [top[-1]]
    second_layer = folium.FeatureGroup(name="Films_Countries")
    second_layer.add_child(folium.GeoJson(data=open(world_file, 'r',\
                                          encoding='utf-8-sig').read(),\
                                          style_function=lambda arg: {'fillColor': 'darkred'\
                                          if arg['properties']['ISO2'] in flm_inf\
                                          and flm_inf[arg['properties']['ISO2']] >= delta[3]\
                                          else 'orange' if arg['properties']['ISO2'] in flm_inf\
                                          and flm_inf[arg['properties']['ISO2']] >= delta[2]\
                                          else 'yellow' if arg['properties']['ISO2'] in flm_inf\
                                          and flm_inf[arg['properties']['ISO2']] >= delta[1]\
                                          else 'darkgreen' if arg['properties']['ISO2'] in flm_inf\
                                          and flm_inf[arg['properties']['ISO2']] >= delta[0]\
                                          else 'lightgreen' if arg['properties']['ISO2'] in flm_inf\
                                          and flm_inf[arg['properties']['ISO2']] > 0\
                                          else 'white'}))
    return second_layer


def make_a_map(films, loc, stat):
    """

    Parameters
    ----------
    films = list((float, float), str, {(}(str, int), ..., }, ...,)
    [(location, city, {(title, year), ..,}, ...,)]

    loc = (float, float) [(latitude, longtitude)]
    stat = dict(str: int, ..., ) [(country: number of films, ..., )]


    Returns
    -------
    None
    """
                     # font,  border, padding, height
    artstile = ([16, 26, "Georgia"], 8, 2, 120)

    order = color_order(films)
    main_map = folium.Map(location=loc, zoom_start=10)
    first_layer = folium.FeatureGroup(name="FILMS")
    for key, col in zip(films, order):
        movies = list(key[2])
        movies = [(elm[0], 10000) if elm[1] == "????" else elm for elm in movies]
        movies.sort(key=lambda x: x[1])
        movies = [(elm[0], "????") if elm[1] == 10000 else elm for elm in movies]
        texts = [str(indx + 1) + ".) " + elm[0] + " - (" + str(elm[1]) + "),<br>"
                 for indx, elm, in enumerate(movies)]
        film_max = max([len(elm) for elm in texts])
        scroll = f"<div style=\"height:{artstile[3]}px;" \
                 f"width:{film_max};" \
                 f"border:{artstile[1]}px solid {col[1]};" \
                 f"padding:{artstile[2]}%" \
                 f"font:{artstile[0][0]}px/{artstile[0][1]}px Georgia, {artstile[0][2]}, Serif;" \
                 f"overflow:auto;\">" \
                 + key[1][0] + ", " + key[1][1] + "<br>" + "Films: " + str(len(movies)) \
                 + "<br>" + "".join(texts)[:-5] + "</div>"
        first_layer.add_child(folium.Marker(location=key[0],
                                            popup=folium.Popup(scroll, \
                                            max_width=film_max * 6, \
                                            min_width=film_max * 6), \
                                            fill_color="red", \
                                            icon=folium.Icon(color=col[0]), \
                                            fill_opacity=0.5))

    second_layer = layer_creator(stat)
    main_map.add_child(first_layer)
    main_map.add_child(second_layer)
    main_map.add_child(folium.LayerControl())
    print("\nMap is ready!!!")
    main_map.save((input("Input name: ") or "unititled") + ".html")


def get_statistics(data):
    """

    Parameters
    ----------
    data = dict((str, str): {(str, int), ...,)}, ...,) [{(city, country): {(film, year),...,)},...)]


    Returns
    -------
    dict(str: int, ..., ) [(country: number of films, ..., )]
    ---------------------------------------------------------
    >>> get_statistics({("Lviv", "Ukraine"): {("film_1", 2000), ("film_3", 2005), \
                                              ("film_2", 1900)}})
    {'Ukraine': 3}
    >>> get_statistics({("Roma", "Italy"): {("film_1", 2000)}, \
                        ("Berlin", "Germany"): {("film_2", 188)}})
    {'Italy': 1, 'Germany': 1}
    >>> get_statistics({("Boston", "USA"): {}})
    {'USA': 0}
    """
    ststcs = {}
    for elm in data:
        if elm[1] not in ststcs:
            ststcs[elm[1]] = len(data[elm])
        else:
            ststcs[elm[1]] += len(data[elm])
    return ststcs


def main():
    """
    Main body
    """
    msg = "Enter your location"
    print(msg + "\n" + "=" * len(msg))
    current_loc = (get_titude(0), get_titude(1))
    print("\nStart analyzing the DATA")
    information, stat = dino(current_loc)
    make_a_map(information, current_loc, stat)


if __name__ == "__main__":
    from doctest import testmod as test
    test()
    DONT_STOP = True
    while DONT_STOP:
        main()
        DONT_STOP = not to_end()
