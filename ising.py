import numpy as np
import math
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets
from PyQt6.QtCore import Qt

# In the real world, the values of the energy stored in individual atoms, the Boltzmann constant, and the J-coupling constant are very very small
# If I was to set the values of these parameters in the code to their real world values, the code would break down
# Python can't handle such infintesimally small quantities, so I'm making certain approximations in here
# Since the energy needed to flip the spin of an atom is of about the same order as the Boltzmann constant (10e-23), their ratio is around 1
# That is why I am setting them both to 1
# Also, since I'm ignoring the physical values of these constants, I also have to ignore the actual Kelvin scale for temperature
# T here is just an arbitrary "hotness" indicator, taking values between 1 and 15.
# I have left the parameters themselves in the calculations for physical clarity

# pyqtgraph and pyqt stuff. i have no idea if im doing things the most optimal way or not. took me basically a whole day to figure this stuff out

app = QtWidgets.QApplication([])
win = QtWidgets.QWidget()
win.setWindowTitle('Ising Model Animation')
win.resize(1600, 800)
vlayout = QtWidgets.QVBoxLayout()
hlayout = QtWidgets.QHBoxLayout()
win.setLayout(vlayout)
plot = pg.PlotWidget(title='Ising Model Animation')
plot.setAspectLocked(True)
hlayout.addWidget(plot)
img = pg.ImageItem()
plot.addItem(img)
colors = [(0, 0, 255, 255),(255, 0, 0, 255)] # -1 is blue, +1 is red 
map = pg.ColorMap(pos=[1.0, 1.0], color=colors)
img.setColorMap(map)

# slider for real-time temperature adjustment
sld = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
sld.setRange(1,100)
sld.setValue(40)
label = QtWidgets.QLabel(f"Temperature: {sld.value() / 25}")

# graph that shows the current magnetization (average value of all the grid's -1s and +1s)
graph = pg.PlotWidget(title='Magnetization')
graph.setYRange(-1, 1)
mag_curve = graph.plot(pen='g')
hlayout.addWidget(graph)

vlayout.addLayout(hlayout)

vlayout.addWidget(sld)
vlayout.addWidget(label)

# tired of dealing with input() prompts, i feel like 100 is a good size for a grid
size = 100
grid = np.random.choice([-1, 1], size=(size, size))
mag_data = np.zeros(500)

def update():
    global grid
    Kb = 1
    J = 1
    T = sld.value() / 25
    label.setText(f"Temperature: {T:.1f}")
    for _ in range(1500):
        i = np.random.randint(0, size)
        j = np.random.randint(0, size)
        up = (i - 1) % size # Previously, i was using try and except, in case of i or j being 0. that felt kind of stupid, was probably slowing down the program
        down = (i + 1) % size # One thing about this modulo method is, it makes the grid wrap around, kind of like a torus.
        left = (j - 1) % size # The elements on the edges are "aligned" with the opposite end of the grid
        right = (j + 1) % size # Technically, that isn't how the system "physically" works, but I feel like it looks more elegant.
        delta_E = 2*J*(grid[up,j] + grid[down,j] + grid[i,left] + grid[i,right])*grid[i,j]
        if delta_E <= 0:
            grid[i,j] *= -1
        else:
            if math.exp(-(delta_E)/(Kb*T)) > np.random.rand():
                grid[i,j] *= -1
            else:
                None
    img.setImage(grid)
    current_mag = np.sum(grid) / (size*size)
    mag_data[:-1] = mag_data[1:]
    mag_data[-1] = current_mag
    mag_curve.setData(mag_data)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(16)

win.show()
app.exec()