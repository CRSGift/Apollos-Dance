# Level 3: Project: Apollo's Dance
# 2D Planetary Solar System Simulation

import numpy as np
import pygame
import planets

#initial conditions
t = 0.0
knob_x = 250
dragging = False

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

# calculate scaling factors for each planet so that they are evenly spaced at t = 0
scaling_factor = {}
for index, planet in enumerate(planets.planets_data):
    scaling_factor[planet] = (50 + (45 * index)) / (planets.planets_data[planet][2])

# Initialize pygame
pygame.display.init()
pygame.font.init()
pygame.display.set_caption("Apollo's Dance")
screen = pygame.display.set_mode((800,800))
font = pygame.font.Font(None, 15)
clock = pygame.time.Clock()

# create a surface for trails
trail_surface = pygame.Surface((800,800))
trail_surface.set_colorkey((0,0,0)) # set the color black to be transparent
trail_surface.fill((0,0,0)) # start with a transparent surface

# Main loop
running = True
while running:
    screen.fill((0,0,0))
    pygame.draw.circle(screen, (255,204,51), (400,400), 30)  # the Sun

    for planet, (P, eccentricity, semi_major_axis, radius, color) in (planets.planets_data.items()): # iterate through the list of planets
        E = calculated_E(t, P, eccentricity) # calculate E
        r = semi_major_axis*(1-eccentricity*np.cos(E)) # calculate r
        theta = 2*np.arctan((np.sqrt((1+eccentricity)/(1-eccentricity)))*np.tan(E/2)) # calculate the angle
        scaled_r = r*scaling_factor[planet] # scale r based on the display
        x = scaled_r*np.cos(theta) # calculate the x position
        y = scaled_r*np.sin(theta) # calculate the y position
        
        pygame.draw.circle(screen, color, (int(x + 400), int(y + 400)), radius) # draw the planet
        pygame.draw.circle(trail_surface, color, (int(x + 400), int(y + 400)), 1) # draw the trail

        label = font.render(planet, True, (255, 255, 255)) # white text
        screen.blit(label, (int(x + 400) - label.get_width() // 2, int(y + 400) + radius + 5)) # overlay the text underneath the planet

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if mouse is clicking on the knob
            if abs(event.pos[0] - knob_x) <= 10 and abs(event.pos[1] - 50) <= 10:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                knob_x = max(250, min(event.pos[0], 550)) # move the knob if dragging
    
    screen.blit(trail_surface, (0, 0)) # overlay(blit) the trail surface onto the main screen

    # create a slider for dt, allowing for the user to slow down or speed up the simulation
    pygame.draw.line(screen, (255, 255, 255), (250, 50), (550, 50), 3) # draw the track
    pygame.draw.circle(screen, (255, 0, 0), (knob_x, 50), 10) # draw the knob
    
    pygame.display.flip() # update the display
    clock.tick(60) # limit to 60 fps

    dt = 5000 + (((knob_x - 250)/ 300)*(5e6)) # calculate dt based on the knob position
    t += dt #increment t
pygame.quit()