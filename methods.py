from numpy import matrix
import random


def divide_to_particles(image_size, pixels):
    particles = []
    particle = []

    #k, v = image_size
    """
    for i in range(0, k):
        particle.append(pixels[i])
        if (i+1) % 2 == 0:
            particle.append(pixels[k+i])
            particle.append(pixels[k+i+1])
            particles.append(particle)
            particle = []
        print i
    """

    for i in range(0, len(pixels)):
        particle.append(pixels[i])
        if (i+1) % 2 == 0: #Five
            particles.append(particle)
            particle = []
    return particles


def get_rgb_values(particles):
    rgbs = []
    for particle in particles:
        rgb = {'red': [], 'green': [], 'blue': []}
        for pixel in particle:
            r, g, b = pixel
            rgb['red'].append(round((2 * float(r) / 255) - 1, 4))
            rgb['green'].append(round((2 * float(g) / 255) - 1, 4))
            rgb['blue'].append(round((2 * float(b) / 255) - 1, 4))
        rgbs.append(rgb)
    return rgbs


def get_rgb_matrixes(rgbs):
    matrixes = []
    for i in rgbs:
        rgb_matrix = {'red': matrix(i['red']),
                      'green': matrix(i['green']),
                      'blue': matrix(i['blue'])}
        matrixes.append(rgb_matrix)
    return matrixes


def get_zero_layer_weights_matrix(zero_layer_neurons_number, first_layer_neurons_number):
    zero_layer_weights = []
    for i in range(zero_layer_neurons_number):
        neuron_weights = []
        for j in range(first_layer_neurons_number):
            neuron_weights.append(round(random.uniform(0, 1), 4))
        zero_layer_weights.append(neuron_weights)
    return matrix(zero_layer_weights)
