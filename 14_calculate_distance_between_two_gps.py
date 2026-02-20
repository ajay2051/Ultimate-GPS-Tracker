import math

earth_radius = 6371000

def calculate_distance(lat_1, lon_1, lat_2, lon_2):
    lat_1 = lat_1 * 2 * math.pi / 360
    lon_1 = lon_1 * 2 * math.pi / 360
    lat_2 = lat_2 * 2 * math.pi / 360
    lon_2 = lon_2 * 2 * math.pi / 360

    theta = 2 * math.asin(math.sqrt(math.sin(lat_2 - lat_1)**2 + math.cos(lat_1)*math.cos(lat_2)*math.sin(lon_2-lon_1)/2)**2)
    distance = earth_radius * theta
    return distance

def calculate_heading(lat_1, lon_1, lat_2, lon_2):
    lat_1 = lat_1 * 2 * math.pi / 360
    lon_1 = lon_1 * 2 * math.pi / 360
    lat_2 = lat_2 * 2 * math.pi / 360
    lon_2 = lon_2 * 2 * math.pi / 360

    delta_lon = lon_2 - lon_1
    x_cordinate = math.sin(delta_lon) * math.cos(lat_2)
    y_cordinate = math.cos(lat_1)*math.sin(lat_2)-math.sin(lat_1)*math.cos(lat_2)*math.cos(delta_lon)
    beta = math.atan2(y_cordinate, x_cordinate)
    beta_degree = beta * 360 / math.pi
    return beta_degree

lat_1 = float(input("Latitude_1: "))
lon_1 = float(input("Longitude_1: "))
lat_2 = float(input("Latitude_2: "))
lon_2 = float(input("Longitude_2: "))

distance = calculate_distance(lat_1, lon_1, lat_2, lon_2)
heading = calculate_heading(lat_1, lon_1, lat_2, lon_2)