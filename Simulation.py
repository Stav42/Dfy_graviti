import math
import random
from numpy.linalg import norm
import numpy as np
import scipy
from scipy.integrate import ode
import matplotlib.pyplot as plot


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Planets:
    def __init__(self, location, velocity, name):
        self.location = location
        self.velocity = velocity
        self.name = name



def calculate_acc(state, time, planet1, planet2, planet3):
    xt,yt, dxdt, dydt = state
    planets = [planet1,planet2,planet3]
    ddxddt = 0
    ddyddt = 0
    for body in planets:
        r = np.sqrt((body.location.x - xt) ** 2 + (body.location.y - yt) ** 2)
        tm = 1 / (r ** 3)
        ddxddt += tm * (body.location.x - xt)
        ddyddt += tm * (body.location.y - yt)

    f = [dxdt, dydt, ddxddt, ddyddt ]
    return f

def dr_dt(t, y, p1, p2, p3):
    """Integration of the governing vector differential equation.
    d2r_dt2 = -(mu/R^3)*r with d2r_dt2 and r as vecotrs.
    Initial position and velocity are given.
    y[0:1] = position components
    y[2:] = velocity components"""


    mu = 1

    rp1 = np.array([p1.location.x, p1.location.y])
    rp2 = np.array([p2.location.x, p2.location.y])
    rp3 = np.array([p3.location.x, p3.location.y])

    dy0 = y[2]
    dy1 = y[3]

    #print(y[0], y[1])

    r1 = np.sqrt((y[0] - p1.location.x) ** 2 + (y[1] - p1.location.y) ** 2)
    r2 = np.sqrt((y[0] - p2.location.x) ** 2 + (y[1] - p2.location.y) ** 2)
    r3 = np.sqrt((y[0] - p3.location.x) ** 2 + (y[1] - p3.location.y) ** 2)

    accx = -((mu / (r1 ** 3)) * (y[0] - p1.location.x)) - ((mu / (r2 ** 3)) * (y[0] - p2.location.x)) - ((mu / (r3 ** 3)) * (y[0] - p3.location.x))
    accy = -((mu / (r1 ** 3)) * (y[1] - p1.location.y)) - ((mu / (r2 ** 3)) * (y[1] - p2.location.y)) - ((mu / (r3 ** 3)) * (y[1] - p3.location.y))


    dy2 = accx
    dy3 = accy

    return [dy0, dy1, dy2, dy3]

def update_velocity(targetbody, time_step, acceleration):
    targetbody.velocity.x += acceleration.x * time_step
    targetbody.velocity.y += acceleration.y * time_step


def update_location(targetbody, time_step):
    targetbody.location.x += targetbody.velocity.x * time_step
    targetbody.location.y += targetbody.velocity.y * time_step


def run_simulation(planets):


    y0 = [0.5, 0, 1.8 * math.cos(80 * math.pi / 180), 1.8 * math.sin(80 * math.pi / 180) ]
    times = np.arange(0, 15,0.0001)
    sol = scipy.integrate.solve_ivp(dr_dt, [0, 15], y0, method='BDF', t_eval=times, args = (planets[0], planets[1], planets[2]), rtol = 1e-5, atol = 1e-4)    #plot.plot(values[:, 0], values[:, 1])
    #plot.show()

    return sol


def plot_output(bodies, motions, outfile=None):
    fig = plot.figure()
    colours = ['r', 'b', 'g', 'y', 'm', 'c']
    ax = fig.add_subplot(1, 1, 1)
    max_range = 0
    print(motions.y[0])
    for index, current_body in enumerate(bodies):
        plotx = bodies[index].location.x
        ploty = bodies[index].location.y
        plot.scatter(plotx, ploty, c=random.choice(colours), label="planet"+str(index),
                         s=22)
    ax.plot(motions.y[0], motions.y[1], c=random.choice(colours),
            label="unit_mass")
    plot.scatter(0.5, 0, label="unit_mass", s=22)

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.legend()

    if outfile:
        plot.savefig(outfile)
    else:
        plot.show()


unit_mass = {"location": Point(0.5, 0),
             "velocity": Point(1.8 * math.cos(80 * math.pi / 180), 1.8 * math.sin(80 * math.pi / 180))}
Planet1 = {"location": Point(0, 1), "velocity": Point(0, 0)}
Planet2 = {"location": Point(1 * math.cos(-30 * math.pi / 180), 1 * math.sin(-30 * math.pi / 180)),
           "velocity": Point(0, 0)}
Planet3 = {"location": Point(1 * math.cos(150 * math.pi / 180), 1 * math.sin(-150 * math.pi / 180)),
           "velocity": Point(0, 0)}


if __name__ == "__main__":
    # build list of planets in the simulation, or create your own
    planets = (
        Planets(location=Planet1["location"], velocity=Planet1["velocity"], name="Planet1"),
        Planets(location=Planet2["location"], velocity=Planet2["velocity"], name="Planet2"),
        Planets(location=Planet3["location"], velocity=Planet3["velocity"], name="Planet3"),
    )

    planet1 = [
        Planets(location=Planet1["location"], velocity=Planet1["velocity"], name="Planet1"),
        Planets(location=Planet2["location"], velocity=Planet2["velocity"], name="Planet2"),
        Planets(location=Planet3["location"], velocity=Planet3["velocity"], name="Planet3"),
    ]

    targetbody = Planets(location=unit_mass["location"], velocity=unit_mass["velocity"], name="unit_mass")
    motions = run_simulation(planets)
    plot_output(planet1,motions)
