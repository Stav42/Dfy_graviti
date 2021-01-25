import math
import random

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
    ddxddt, ddyddt  = [0,0]
    planets = [planet1,planet2,planet3]
    for body in planets:
        r = (body.location.x - xt) ** 2 + (body.location.y - yt) ** 2
        r = math.sqrt(r)
        tm = 1 / (r ** 3)
        ddxddt += tm * (body.location.x - xt)
        ddyddt += tm * (body.location.y - yt)
        
    return dxdt,dydt,ddxddt,ddyddt


def update_velocity(targetbody, time_step, acceleration):
    targetbody.velocity.x += acceleration.x * time_step
    targetbody.velocity.y += acceleration.y * time_step


def update_location(targetbody, time_step):
    targetbody.location.x += targetbody.velocity.x * time_step
    targetbody.location.y += targetbody.velocity.y * time_step


def run_simulation(planets, targetbody, time_step, no_of_steps, report_int):
    location_hist = []
    target_index = 0

    for index, current_body in enumerate(planets):
        location_hist.append({"x": [], "y": [], "name": current_body.name})
        target_index = index
        location_hist[target_index]["x"] = current_body.location.x
        location_hist[target_index]["y"] = current_body.location.y

    target_index += 1

    location_hist.append({"x": [], "y": [], "name": targetbody.name})


    init = (
        0.5,  # x[0]
        0,  # y[0]
        1.8 * math.cos(80 * math.pi / 180),  # x'[0]
        1.8 * math.sin(80 * math.pi / 180)  # y'[0]
    )

    t0 = 0
    times = np.linspace(0, 25, 900000)
    values = scipy.integrate.solve_ivp(calculate_acc, (init), times, method="LSODA", args=(planets), tfirst=False, rtol=1e-5)


    return values


def plot_output(bodies, motion, outfile=None):
    fig = plot.figure()
    colours = ['r', 'b', 'g', 'y', 'm', 'c']
    ax = fig.add_subplot(1, 1, 1)
    max_range = 0
    for index, current_body in enumerate(bodies):
        if index == 3:
            max_dim = max(max([item[0] for item in motions]), max([item[1] for item in motions]))
            if max_dim > max_range:
                max_range = max_dim
            ax.plot([item[0] for item in motions], [item[1] for item in motions], c=random.choice(colours),
                    label=current_body["name"])
        else:
            plotx = bodies[index].location.x
            ploty = bodies[index].location.y
            plot.scatter(plotx, ploty, c=random.choice(colours), label="planet"+str(index),
                         s=22)
    ax.plot([item[0] for item in motions], [item[1] for item in motions], c=random.choice(colours),
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
Planet2 = {"location": Point(1 * math.cos(30 * math.pi / 180), -1 * math.sin(30 * math.pi / 180)),
           "velocity": Point(0, 0)}
Planet3 = {"location": Point(-1 * math.cos(30 * math.pi / 180), -1 * math.sin(30 * math.pi / 180)),
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
    motions = run_simulation(planets, targetbody, time_step=1e3, no_of_steps=8000, report_int=1000)
    plot_output(planet1,motions)
