import math
import random
import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D


class Point:
    def __init__(self, x, y):
        """

        :type x: object
        """
        self.x = x
        self.y = y


class body:
    def __init__(self, location, mass, velocity, name=""):
        self.location = location
        self.mass = mass
        self.velocity = velocity
        self.name = name


def single_body_calculation(bodies, targetbody_index):
    G_const = 6.67e-11
    acceleration = Point(0, 0)
    targetbody = bodies[targetbody_index]
    for index, external_body in enumerate(bodies):
        if index != targetbody_index:
            r = (targetbody.location.x - external_body.location.x) ** 2 + (
                    targetbody.location.y - external_body.location.y) ** 2
            r = math.sqrt(r)
            tmp = 1 / r ** 3
            acceleration.x += -tmp * (external_body.location.x - targetbody.location.x)
            acceleration.y += -tmp * (external_body.location.y - targetbody.location.y)

    return acceleration


def compute_velocity(bodies, targetbody_index, time_step=1):
    acceleration = single_body_calculation(bodies, targetbody_index)
    targetbody = bodies[targetbody_index]
    targetbody.velocity.x += acceleration.x * time_step
    targetbody.velocity.y += acceleration.y * time_step


def update_location(bodies, targetbody_index, time_step=1):
    targetbody = bodies[targetbody_index]
    targetbody.location.x += targetbody.velocity.x * time_step
    targetbody.location.y += targetbody.velocity.y * time_step


def compute_gravity_step(bodies, targetbody_index, time_step=1):
    compute_velocity(bodies, targetbody_index, time_step)
    update_location(bodies, targetbody_index, time_step)


def run_simulation(targetbody_index, bodies, no_of_steps=10000, time_step=1, report_freq=100):
    locations_hist = []
    targetbody = bodies[targetbody_index]
    for current_body in bodies:
        locations_hist.append({"x": [], "y": [], "name": current_body.name})

    for i in range(1, no_of_steps):
        compute_gravity_step(bodies, targetbody_index, time_step=1000)
        if i % report_freq == 0:
            for index, body_location in enumerate(locations_hist):
                body_location["x"].append(bodies[index].location.x)
                body_location["y"].append(bodies[index].location.y)

    return locations_hist


def plot_output(points, outfile=None):
    fig = plot.figure()
    colours = ['r', 'b', 'g', 'y', 'm', 'c']
    ax = fig.add_subplot(1, 1, 1)
    max_range = 0

    for current_pos in points:
        max_dim = max(max(current_pos["x"]), max(current_pos["y"]))
        if max_dim > max_range:
            max_range = max_dim
        ax.plot(current_pos["x"], current_pos["y"], c=random.choice(colours))

    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])

    if outfile:
        plot.savefig(outfile)
    else:
        plot.show()


# planet data (location (m), mass (kg), velocity (m/s)
unit_mass = {"location": Point(0.5, 0), "mass": 1,
             "velocity": Point(1.8 * math.cos(80 * math.pi / 180), 1.8 * math.cos(80 * math.pi / 180))}
planet1 = {"location": Point(0, 1), "mass": 3.285e23, "velocity": Point(0, 0)}
planet2 = {"location": Point(1 * math.cos(math.pi / 6), -1 * math.sin(math.pi / 6)), "mass": 3.285e23,
           "velocity": Point(0, 0)}
planet3 = {"location": Point(-1 * math.cos(math.pi / 6), -1 * math.sin(math.pi / 6)), "mass": 3.285e23,
           "velocity": Point(0, 0)}

if __name__ == "__main__":
    # build list of planets in the simulation, or create your own
    bodies = [
        body(location=planet1["location"], mass=planet1["mass"], velocity=planet1["velocity"], name="planet1"),
        body(location=planet2["location"], mass=planet2["mass"], velocity=planet2["velocity"], name="planet2"),
        body(location=planet3["location"], mass=planet3["mass"], velocity=planet3["velocity"], name="planet3"),
        body(location=unit_mass["location"], mass=unit_mass["mass"], velocity=unit_mass["velocity"], name="unit_mass"),
    ]

    motions = run_simulation(3, bodies, time_step=100, no_of_steps=80000, report_freq=1000)
    plot_output(motions)

#yaay! from the console :)
