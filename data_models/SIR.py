from scipy.integrate import odeint
import numpy as np
import os
import sys
import json
from json import JSONEncoder


class NumpyArrayEncoder(JSONEncoder):
    """
    Numpy array to Json converter
    json.dumps requires class instance for cls param
    """

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def deriv(y, time, N, beta, gamma, delta):
    """

    differntial equations that define the SEIR model
    reference: https://web.stanford.edu/~jhj1/teachingdocs/Jones-Epidemics050308.pdf slide 50

    :param y: tuple of susceptible, exposed, infected, resistant values
    :param time: time
    :param N: total population
    :param beta: rate of spread
    :param gamma: rate of recovery
    :param delta: rate of progression from exposure to infection
    :return: returns tuple of derivatives for susceptible, exposed, infected, resistant

    """
    susceptible, exposed, infected, resistant = y
    dSusceptible = -beta * susceptible * infected / N
    dExposed = beta * susceptible * infected / N - delta * exposed
    dInfected = delta * exposed - gamma * infected
    dResistant = gamma * infected
    return dSusceptible, dExposed, dInfected, dResistant


def integ(y_initial, time, N, beta, gamma, delta):
    """

    solves the system of SEIR differntial equations using scipy.integrate
    :param y_initial: tuple of seed values for SEIR values
    :param time: time
    :param N: total population
    :param beta: rate of spread
    :param gamma: rate of recovery
    :param delta: rate of progression from exposure to infectione
    :return: returns tuple of time-series arrays for susceptible, exposed, infected, resistant 

    """
    ret = odeint(deriv, y_initial, time, args=(N, beta, gamma, delta))
    susceptible, exposed, infected, resistant = ret.T
    return susceptible, exposed, infected, resistant


def read_in():
    value = input()
    return json.loads(value)


def main():
    variables = read_in()
    susceptible = variables['susceptible']
    exposed = variables['exposed']
    infected = variables['infected']
    resistant = variables['resistant']
    return susceptible, exposed, infected, resistant


# Start process
if __name__ == '__main__':
    susceptible, exposed, infected, resistant = main()

    N = susceptible
    E = exposed
    D = 4.0  # infections lasts four days
    gamma = 1.0 / D
    delta = 1.0 / 5.0  # incubation period of five days
    R_0 = 5.0
    beta = R_0 * gamma  # R_0 = beta / gamma, so beta = R_0 * gamma
    S0, E0, I0, R0 = N-E, E, 0, 0  # initial conditions: one exposed

    time = np.linspace(0, 99, 100)  # Grid of time points (in days)
    y_iniital = S0, E0, I0, R0  # Initial conditions vector

    S, E, I, R = integ(y_iniital, time, N, beta, gamma, delta)
    S.tolist()
    E.tolist()
    I.tolist()
    R.tolist()

    results = {
        'susceptible': S,
        'exposed': E,
        'infected': I,
        'resistant': R
    }

    results_json = json.dumps(results, cls=NumpyArrayEncoder)
    print(results_json)
    sys.stdout.flush()
