#Level 3: Project
import numpy as np
import pygame

#solve for E, the eccentric anomaly, using numerical methods
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

# position of planet as a function of time
def orbit(dt, P, eccentricity, semi_major_axis):
    t = 0.
    while t < P: #until one rotation is completed
        E = calculated_E(t, P, eccentricity) # calculate E
        r = semi_major_axis*(1-eccentricity*np.cos(E)) # calculate r
        theta = 2*np.arctan((np.sqrt((1+eccentricity)/(1-eccentricity)))*np.tan(E/2)) #calculate the angle
        x = r*np.cos(theta) # calculate the x position
        y = r*np.sin(theta) # calculate the y position
        t += dt #increment t
        yield x, y

# Initialize pygame
pygame.display.init()
screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("Apollo's Dance")
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255,255,0), (400,400), 20)  # Sun
    
    pygame.display.flip()
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()