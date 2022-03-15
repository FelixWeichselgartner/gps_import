from math import sin, cos, pi
import numpy as np
from matplotlib import pyplot as plt


def read_latitude_longitude(filename='measure.txt'):
    coordinates = None
    with open(filename) as urlimp:
        text = urlimp.readline()
        text = text.replace('\n', '')
        coor = text.split('%5B%5B%5B%5B')
        coor = coor[1:]
        coor = coor[0]
        coor = coor.split('%5D%5D%2C%22%')
        coor = coor[:len(coor)]
        text = coor[0]
        coor = text.split('%5D%2C%5B')
        coordinates = list()
        for c in coor:
            a = c.split('%2C')
            #                  latitude,     longitude
            coordinates.append(np.array([float(a[0]), float(a[1])]))
    return coordinates


def latlon2kart(latlon):
    lat = latlon[0]
    lon = latlon[1]
    return latlong2kart(lat, lon)


def latlong2kart(lat, lon):
    # https://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
    r = 6.3781e6 + 454
    latrad = lat / 180 * pi
    lonrad = lon / 180 * pi
    x = r * cos(latrad) * cos(lonrad)
    y = r * cos(latrad) * sin(lonrad)
    z = r * sin(latrad)
    return np.vstack([x, y, z])


def latlong2local(latlong):
    """
    first convert from latitude and longitude to earth cartesian 
    then convert from earth cartesian to local cartesian with origin from first point in latlong
    """

    kart = list()
    for ll in latlong:
        kart.append(latlon2kart(ll))

    # calculate transformation matrix
    origin_index = 0
    origin = kart[origin_index]

    xaxis = latlon2kart(latlong[origin_index] + np.array([0, 0.00001])) - origin
    xaxis = xaxis / np.linalg.norm(xaxis)
    zaxis = origin
    zaxis = zaxis / np.linalg.norm(zaxis)
    yaxis = np.cross(zaxis.T, xaxis.T).T
    yaxis = yaxis / np.linalg.norm(yaxis)

    R_el = np.hstack([xaxis, yaxis, zaxis])
    R_le = np.linalg.inv(R_el)
    print(R_le)
    print(np.linalg.det(R_le))

    locals = list()
    for k in kart:
        b = R_le @ (k - origin)
        locals.append(b)
    
    return locals


def plot_map(locals):
    x = list()
    y = list()
    for l in locals:
        ll = l.tolist()
        myx = ll[0]
        myx = myx[0]
        myy = ll[1]
        myy = myy[0]
        x.append(myx)
        y.append(myy)
    plt.axis('equal')
    plt.plot(x, y, marker='o', linestyle='-', c='red')
    plt.plot()
    plt.show()


def gauss_area_formula(points):
    A = 0
    for i in range(len(points)):
        pi = points[i]
        yi = pi[1]
        xi = pi[0]
        pi1modn = points[(i + 1) % len(points)]
        yi1modn = pi1modn[1]
        xi1modn = pi1modn[0]
        A += (yi + yi1modn) * (xi - xi1modn)
    A = abs(A)
    A /= 2
    return A


def tester():
    latlong = read_latitude_longitude('measure_italy.txt')
    locals =  latlong2local(latlong)
    print(f'area is {gauss_area_formula(locals)}')
    plot_map(locals)    


if __name__ == '__main__':
    tester()
