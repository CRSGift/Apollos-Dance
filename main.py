# Level 3: Project: Apollo's Dance

import numpy as np # type: ignore
import pygame # type: ignore
import planets

dt = 50000
t = 0.0

# Solve for E, the eccentric anomaly, using numerical methods
def calculated_E(t, P, eccentricity):
    n = 2 * np.pi / P # mean motion
    M = n * t # mean anomaly
    E = np.pi # initial guess

    while True: # until E is within tolerance, keep iterating
        f = E - eccentricity * np.sin(E) - M # Kepler's equation
        f_prime = 1 - eccentricity * np.cos(E) # derivative of Kepler's equation
        E_next = E - f / f_prime # calculates iterated value of E using Newton's method
        if abs(E_next - E) < 1e-6: # if E is within tolerance, stop iterating
            break
        E = E_next # update E for next iteration
    return E

# Initialize pygame
pygame.display.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Apollo's Dance")
clock = pygame.time.Clock()

# calculate scaling factors for each planet so that they are evenly spaced at t = 0
scaling_factors = {}
for index, planet in enumerate(planets.planets_data):
    scaling_factors[planet] = (60 + (36.25 * index)) / (planets.planets_data[planet][2])
print(scaling_factors)

# Main loop
running = True
while running:
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255,255,0), (400,400), 30)  # the sun

    for planet, (P, eccentricity, semi_major_axis, radius, color) in (planets.planets_data.items()): # iterate through the list of planets
        E = calculated_E(t, P, eccentricity) # calculate E
        r = semi_major_axis*(1-eccentricity*np.cos(E)) # calculate r
        theta = 2*np.arctan((np.sqrt((1+eccentricity)/(1-eccentricity)))*np.tan(E/2)) # calculate the angle
        scaled_r = r*scaling_factors[planet] # scale r based on the display
        x = scaled_r*np.cos(theta) # calculate the x position
        y = scaled_r*np.sin(theta) # calculate the y position
        pygame.draw.circle(screen, color, (int(x + 400), int(y + 400)), radius)

    pygame.display.flip() # update the display
    clock.tick(60) # limit to 60 fps
    t += dt #increment t
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()