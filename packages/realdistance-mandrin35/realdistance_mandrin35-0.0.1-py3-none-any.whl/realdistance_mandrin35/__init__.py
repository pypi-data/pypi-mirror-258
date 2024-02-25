from math import sin, cos, atan2, sqrt, pi as PI


def distance(lt1,ln1, lt2,ln2):
    R = 6371000 # earth radius
    theta1 = lt1 * PI / 180
    theta2 = lt2 * PI / 180
    delta_theta = (lt2 -lt1) * PI / 180
    delta_fi = (ln2 - ln1) * PI / 180
    part1 = (sin(delta_theta/2.0) ** 2) 
    part2 = (cos(theta1) * cos(theta2) *(sin(delta_fi/2.0) **2 ))
    a = part1 + part2
    c = 2* atan2(sqrt(a), sqrt(1-a))
    # return in meters
    return R * c
