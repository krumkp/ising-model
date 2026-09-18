import numpy as np
import math

# In the real world, the values of the energy stored in individual atoms, the Boltzmann constant, and the J-coupling constant are very very small
# If I was to set the values of these parameters in the code to their real world values, the code would break down
# Python can't handle such infintesimally small quantities, so I'm making certain approximations in here
# Since the energy needed to flip the spin of an atom is of about the same order as the Boltzmann constant (10e-23), their ratio is around 1
# That is why I am setting them both to 1
# Also, since I'm ignoring the physical values of these constants, I also have to ignore the actual Kelvin scale for temperature
# T here is just an arbitrary "hotness" indicator, taking values between 1 and 15.
# I have left the parameters themselves in the calculations for physical clarity
Kb = 1 
J = 1
size = [0, 0]
size[0] = int(input("Size of square grid: "))
size[1] = size[0]
a = [-1, 1]
T = 8
grid = np.random.choice(a, size=(size[0], size[1]))
i = np.random.randint(0, high=(size[1]))
j = np.random.randint(0, high=(size[1]))

print(i, j, grid, grid[i,j], sep='\n')

try:
    up = grid[i-1,j]
except IndexError:
    up = 0

try:
    down = grid[i+1,j]
except IndexError:
    down = 0

try:
    left = grid[i,j-1]
except IndexError:
    left = 0

try:
    right = grid[i,j+1]
except IndexError:
    right = 0

delta_E = 2*J*(up + down + left + right)*grid[i,j]
res = 'no flip'
if delta_E <= 0:
    grid[i,j] = grid[i,j]*-1
    res = 'flip1' # Flipping, because it would lower the overall energy of the system
else:
    if math.exp(-(delta_E)/(Kb*T)) - np.random.rand() > 0:
        grid[i,j] = grid[i,j]*-1
        res = 'flip2' # Flipping brought on by thermal fluctuations
    else:
        None

print(up, down, left, right, delta_E, grid, res, sep='\n')