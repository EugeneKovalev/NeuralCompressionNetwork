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


def get_new_rgb_values(rgb_matrixes, RED_zero_layer_weights, RED_first_layer_weights,
                                     GREEN_zero_layer_weights, GREEN_first_layer_weights,
                                     BLUE_zero_layer_weights, BLUE_first_layer_weights):
    new_rgb_values = {'red': [], 'green': [], 'blue': []}
    for rgb_matrix in rgb_matrixes:
        RED_latent_layer = rgb_matrix['red'] * RED_zero_layer_weights
        RED_output_layer = RED_latent_layer * RED_first_layer_weights
        GREEN_latent_layer = rgb_matrix['green'] * GREEN_zero_layer_weights
        GREEN_output_layer = GREEN_latent_layer * GREEN_first_layer_weights
        BLUE_latent_layer = rgb_matrix['blue'] * BLUE_zero_layer_weights
        BLUE_output_layer = BLUE_latent_layer * BLUE_first_layer_weights
        red_list = []
        for r in list(RED_output_layer.flat):
            red_list.append(int((r + 1) * 255 / 2))
        green_list = []
        for g in list(GREEN_output_layer.flat):
            green_list.append(int((g + 1) * 255 / 2))
        blue_list = []
        for b in list(BLUE_output_layer.flat):
            blue_list.append(int((b + 1) * 255 / 2))
        new_rgb_values['red'].append(red_list)
        new_rgb_values['green'].append(green_list)
        new_rgb_values['blue'].append(blue_list)
    return new_rgb_values


def process_teaching_for_color(MAX_ERROR, first_layer_neurons_number, rgb_matrixes, color):
    zero_layer_neurons_number = rgb_matrixes[0]['red'].size

    corrected_weights = []

    # the next string initializes a do-while-like loop
    mean_square_error = MAX_ERROR + 1
    error_iteration = 0
    while mean_square_error > MAX_ERROR:
        matrix_iteration = 0
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

        for rgb_matrix in rgb_matrixes:
            first_layer_output_values = rgb_matrix[color] * corrected_zero_layer_weights_matrix
            second_layer_output_values = first_layer_output_values * corrected_first_layer_weights_matrix
            delta_values_matrix = second_layer_output_values - rgb_matrix[color]
            mean_square_error += delta_values_matrix * delta_values_matrix.H

        print('MSE ', mean_square_error)
        print(error_iteration)
        error_iteration += 1
    print(matrix_iteration, "====================================")
    return corrected_zero_layer_weights_matrix, corrected_first_layer_weights_matrix