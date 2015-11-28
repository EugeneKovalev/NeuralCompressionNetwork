from PIL import Image
from methods import divide_to_particles, get_rgb_values, get_rgb_matrixes, get_zero_layer_weights_matrix


ALPHA = 0.001
image = Image.open("Kwame_Raoul_Expr.png").convert("RGB")
image_size = image.size
pixels = image.getdata()
newData = []
for x in pixels:
    newData.append((0, 0, 0))


image_particles = divide_to_particles(pixels)

rgb_values = get_rgb_values(image_particles)

rgb_matrixes = get_rgb_matrixes(rgb_values)

for color in ['red', 'green', 'blue']:
    matrix_iteration = 0
    for rgb_matrix in rgb_matrixes:
        zero_layer_neurons_number = rgb_matrix[color].size
        first_layer_neurons_number = 10
        zero_layer_weights_matrix = get_zero_layer_weights_matrix(zero_layer_neurons_number, first_layer_neurons_number)
        first_layer_weights_matrix = zero_layer_weights_matrix.H

        # START CYCLE
        while True:
            first_layer_output_values = rgb_matrix[color]*zero_layer_weights_matrix
            second_layer_output_values = first_layer_output_values*first_layer_weights_matrix

            delta_values_matrix = second_layer_output_values-rgb_matrix[color]

            corrected_first_layer_weights_matrix = first_layer_weights_matrix - \
                                                   ALPHA*first_layer_output_values.H*delta_values_matrix
            corrected_zero_layer_weights_matrix = zero_layer_weights_matrix - \
                                                  ALPHA*rgb_matrix[color].H * \
                                                  delta_values_matrix*corrected_first_layer_weights_matrix.H

            MAX_ERROR = 0.1*first_layer_neurons_number
            mean_square_error = delta_values_matrix*delta_values_matrix.H

            if mean_square_error < MAX_ERROR:
                print(matrix_iteration)
                new_data_iteration = 0
                for r, g, b in newData[matrix_iteration*5:(matrix_iteration+1)*5]:
                    changed_color_value = second_layer_output_values.flat[new_data_iteration]
                    changed_color_value = int((changed_color_value + 1) * 255 / 2)
                    if color is 'red':
                        newData[matrix_iteration * 5 + new_data_iteration] = changed_color_value, g, b
                    elif color is 'green':
                        newData[matrix_iteration * 5 + new_data_iteration] = r, changed_color_value, b
                    elif color is 'blue':
                        newData[matrix_iteration * 5 + new_data_iteration] = r, g, changed_color_value

                    new_data_iteration += 1

                matrix_iteration += 1
                break
            else:
                zero_layer_weights_matrix = corrected_zero_layer_weights_matrix
                first_layer_weights_matrix = corrected_first_layer_weights_matrix

image.putdata(newData)
image.save('out.jpg')
