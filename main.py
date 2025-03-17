#Level 3: Project
import numpy as np

def calculated_E(t, P, eccentricity):
    n = 2 * np.pi / P # mean motion
    M = n * t # mean anomaly
    E = np.pi #initial guess

    while True: # until E is within tolerance, keep iterating
        f = E - eccentricity * np.sin(E) - M # Kepler's equation
        f_prime = 1 - eccentricity * np.cos(E) # derivative of Kepler's equation
        E_next = E - f / f_prime # calculates iterated value of E using Newton's method
        if abs(E_next - E) < 1e-6: # if E is within tolerance, stop iterating
            break
        E = E_next # update E for next iteration
    return E

def orbit(dt, P, eccentricity, semi_major_axis):
    t = 0.
    while t < P: #until one rotation is completed
        E = calculated_E(t, P, eccentricity) # calculate E
        r = semi_major_axis*(1-eccentricity*np.cos(E)) # calculate r
        theta = 2*np.arctan((np.sqrt((1+eccentricity)/(1-eccentricity)))*np.tan(E/2)) #calculate the angle
        x = r*np.cos(theta) # calculate the x position
        y = r*np.sin(theta) # calculate the y position
        t += dt