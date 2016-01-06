from PIL import Image
from methods import divide_to_particles, get_rgb_values, get_rgb_matrixes, get_zero_layer_weights_matrix, \
    get_alpha, get_green_output_values, get_blue_output_values

image = Image.open("Test_Image.png").convert("RGB")
image_size = image.size
pixels = image.getdata()
newData = []
for x in pixels:
    newData.append((0, 0, 0))

image_particles = divide_to_particles(image_size, pixels)

rgb_values = get_rgb_values(image_particles)

rgb_matrixes = get_rgb_matrixes(rgb_values)

#first_layer_neurons_number = input('Enter the number of neurons in the first layer: ')
first_layer_neurons_number = 2
MAX_ERROR = 10

zero_layer_neurons_number = rgb_matrixes[0]['red'].size

list_of_mean_squared_errors = []
list_of_corrected_weights = []

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
            zero_layer_weights_matrix = list_of_corrected_weights[matrix_iteration]['zero_layer']
            first_layer_weights_matrix = list_of_corrected_weights[matrix_iteration]['first_layer']
        ALPHA = get_alpha(rgb_matrix['red'])
        first_layer_output_values = rgb_matrix['red']*zero_layer_weights_matrix
        second_layer_output_values = first_layer_output_values*first_layer_weights_matrix
        ALPHA_QUOTE = get_alpha(first_layer_output_values)
        delta_values_matrix = second_layer_output_values-rgb_matrix['red']
        corrected_first_layer_weights_matrix = first_layer_weights_matrix - \
                                                   ALPHA_QUOTE*first_layer_output_values.H*delta_values_matrix
        corrected_zero_layer_weights_matrix = zero_layer_weights_matrix - \
                                                  ALPHA*rgb_matrix['red'].H * \
                                                  delta_values_matrix*first_layer_weights_matrix.H
        list_of_mean_squared_errors.append(delta_values_matrix*delta_values_matrix.H)

        if error_iteration == 0:
            list_of_corrected_weights.append({'zero_layer': corrected_zero_layer_weights_matrix,
                                                'first_layer': corrected_first_layer_weights_matrix})
        else:
            list_of_corrected_weights.pop(matrix_iteration)
            list_of_corrected_weights.insert(matrix_iteration, {'zero_layer': corrected_zero_layer_weights_matrix,
                                                                'first_layer': corrected_first_layer_weights_matrix})
        #print(matrix_iteration)
        #print(matrix_iteration, corrected_zero_layer_weights_matrix, corrected_first_layer_weights_matrix)
        matrix_iteration += 1
        #print(zero_layer_weights_matrix, first_layer_weights_matrix)
        #print(rgb_matrix['red'], second_layer_output_values)
        #print(delta_values_matrix*delta_values_matrix.H)

    mean_square_error = sum(list_of_mean_squared_errors)
    list_of_mean_squared_errors = []
    print('MSE ', mean_square_error)
    #input()
    print(error_iteration)
    error_iteration += 1

print('JESUS CHRIST')
if mean_square_error < MAX_ERROR:
    print('Holly Molly')
    print('MAX ERROR', mean_square_error, ' < ', MAX_ERROR)
    print(matrix_iteration, "====================================")

    RED_second_layer_output_values = second_layer_output_values
    GREEN_second_layer_output_values = get_green_output_values(rgb_matrix['green'], zero_layer_weights_matrix)
    BLUE_second_layer_output_values = get_blue_output_values(rgb_matrix['blue'], zero_layer_weights_matrix)
    #print('boobs ', newData)
    new_data_iteration = 0
    for r, g, b in newData[matrix_iteration*2:(matrix_iteration+1)*2]: #FIVE
        RED_changed_color_value = RED_second_layer_output_values.flat[new_data_iteration]
        RED_changed_color_value = int((RED_changed_color_value + 1) * 255 / 2)
        GREEN_changed_color_value = GREEN_second_layer_output_values.flat[new_data_iteration]
        GREEN_changed_color_value = int((GREEN_changed_color_value + 1) * 255 / 2)
        BLUE_changed_color_value = BLUE_second_layer_output_values.flat[new_data_iteration]
        BLUE_changed_color_value = int((BLUE_changed_color_value + 1) * 255 / 2)
        newData[matrix_iteration * 2 + new_data_iteration] = RED_changed_color_value, GREEN_changed_color_value, BLUE_changed_color_value #FIVE
        new_data_iteration += 1
    matrix_iteration += 1
    #break
else:
    zero_layer_weights_matrix = corrected_zero_layer_weights_matrix
    first_layer_weights_matrix = corrected_first_layer_weights_matrix

image.putdata(newData)
image.save('out.jpg')
