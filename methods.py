from numpy import matrix
import random


def divide_to_particles(image_size, pixels):
    particles = []
    particle = []
    k, v = image_size
    for j in range(0, v, 2):
        for i in range(k*j, k*(j+1)):
            particle.append(pixels[i])
            if (i+1) % 2 == 0:
                particle.append(pixels[k+i-1])
                particle.append(pixels[k+i])
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


def get_alpha(matrix):
    values_to_be_squared = 0
    for i in matrix.tolist()[0]:
        values_to_be_squared += i*i
    return 1/values_to_be_squared


def get_color_output_values(color_values, zero_layer_weights):
    first_layer_output_values = color_values*zero_layer_weights
    first_layer_weights_matrix = zero_layer_weights.H
    return first_layer_output_values*first_layer_weights_matrix


def process_teaching_for_color(MAX_ERROR, first_layer_neurons_number, rgb_matrixes, color):
    zero_layer_neurons_number = rgb_matrixes[0]['red'].size

    corrected_weights = []

    # the next string initializes a do-while-like loop
    mean_square_error = MAX_ERROR + 1
    error_iteration = 0
    while mean_square_error > MAX_ERROR:
        matrix_iteration = 0
        list_of_delta_matrixes = []
        for rgb_matrix in rgb_matrixes:

            if error_iteration == 0:
                zero_layer_weights_matrix = get_zero_layer_weights_matrix(zero_layer_neurons_number, first_layer_neurons_number)
                first_layer_weights_matrix = zero_layer_weights_matrix.H
            else:
                zero_layer_weights_matrix = corrected_weights['zero_layer']
                first_layer_weights_matrix = corrected_weights['first_layer']


            """
            if error_iteration == 0:
                zero_layer_weights_matrix = get_zero_layer_weights_matrix(zero_layer_neurons_number, first_layer_neurons_number)
                first_layer_weights_matrix = zero_layer_weights_matrix.H
            else:
                zero_layer_weights_matrix = corrected_weights[matrix_iteration]['zero_layer']
                first_layer_weights_matrix = corrected_weights[matrix_iteration]['first_layer']
            """

            ALPHA = get_alpha(rgb_matrix[color])
            first_layer_output_values = rgb_matrix[color] * zero_layer_weights_matrix
            second_layer_output_values = first_layer_output_values * first_layer_weights_matrix
            ALPHA_QUOTE = get_alpha(first_layer_output_values)
            delta_values_matrix = second_layer_output_values - rgb_matrix[color]
            corrected_first_layer_weights_matrix = first_layer_weights_matrix - \
                                                   ALPHA_QUOTE * first_layer_output_values.H * delta_values_matrix
            corrected_zero_layer_weights_matrix = zero_layer_weights_matrix - \
                                                  ALPHA * rgb_matrix[color].H * \
                                                  delta_values_matrix * first_layer_weights_matrix.H
            list_of_delta_matrixes.append(delta_values_matrix)

            corrected_weights = {'zero_layer': corrected_zero_layer_weights_matrix,
                                         'first_layer': corrected_first_layer_weights_matrix}


            """
            if error_iteration == 0:
                corrected_weights.append({'zero_layer': corrected_zero_layer_weights_matrix,
                                                    'first_layer': corrected_first_layer_weights_matrix})
            else:
                corrected_weights.pop(matrix_iteration)
                corrected_weights.insert(matrix_iteration, {'zero_layer': corrected_zero_layer_weights_matrix,
                                                                    'first_layer': corrected_first_layer_weights_matrix})
            """

            matrix_iteration += 1

        mean_square_error = 0
        for delta_matrix in list_of_delta_matrixes:
            mean_square_error += delta_matrix * delta_matrix.H

        print('MSE ', mean_square_error)
        print(error_iteration)
        error_iteration += 1
    print(matrix_iteration, "====================================")
    return corrected_zero_layer_weights_matrix, corrected_first_layer_weights_matrix