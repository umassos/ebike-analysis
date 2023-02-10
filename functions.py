import math

def closest_station(x, y, names, towns, points):
    closest_distance = float("inf")
    closest_name = ""
    closest_town = ""
    for i, point in enumerate(points):
        distance = math.sqrt((x - point[0])**2 + (y - point[1])**2)
        if distance < closest_distance:
            closest_distance = distance
            closest_name = names[i]
            closest_town = towns[i]
    return closest_name, closest_town