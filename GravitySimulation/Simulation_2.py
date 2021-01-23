import math
import random

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


def calculate_acc(planets, targetbody):
    acceleration = Point(0, 0)
    for body in planets:
        r = (body.location.x - targetbody.location.x) ** 2 + (body.location.y - targetbody.location.y) ** 2
        r = math.sqrt(r)
        tm = 1 / (r ** 3)
        acceleration.x += tm * (body.location.x - targetbody.location.x)
        acceleration.y += tm * (body.location.y - targetbody.location.y)

    return acceleration


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

    for i in range(no_of_steps):
        acceleration = calculate_acc(planets, targetbody)
        update_velocity(targetbody, time_step, acceleration)
        update_location(targetbody, time_step)
        if i % report_int == 0:
            location_hist[target_index]["x"].append(targetbody.location.x)
            location_hist[target_index]["y"].append(targetbody.location.y)

    return location_hist


def plot_output(bodies, outfile=None):
    fig = plot.figure()
    colours = ['r', 'b', 'g', 'y', 'm', 'c']
    ax = fig.add_subplot(1, 1, 1)
    max_range = 0
    for index, current_body in enumerate(bodies):
        print(current_body)
        max_dim = max(max(current_body[index]["x"]), max(current_body[index]["y"]))
        if max_dim > max_range:
            max_range = max_dim
        ax.plot(current_body["x"], current_body["y"], c=random.choice(colours),
                label=current_body["name"])

    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
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
    planets = [
        Planets(location=Planet1["location"], velocity=Planet1["velocity"], name="Planet1"),
        Planets(location=Planet2["location"], velocity=Planet2["velocity"], name="Planet2"),
        Planets(location=Planet3["location"], velocity=Planet3["velocity"], name="Planet3"),
    ]

    targetbody = Planets(location=unit_mass["location"], velocity=unit_mass["velocity"], name="unit_mass")

    motions = run_simulation(planets, targetbody, time_step=1e-2, no_of_steps=80000, report_int=1000)
    plot_output(motions)
