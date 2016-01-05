from PIL import Image
from methods import divide_to_particles, get_rgb_values, get_rgb_matrixes, get_zero_layer_weights_matrix, \
    get_alpha, get_green_output_values, get_blue_output_values


#print(float((4+16900)*1+2)/(4*16900))
#print(float((4+16900)*2+2)/(4*16900))
#print(float((4+16900)*3+2)/(4*16900))
#print(float((4+16900)*4+2)/(4*16900))
#print(float((4+16900)*5+2)/(4*16900))
#print(float((4+16900)*6+2)/(4*16900))
#print(float((4+16900)*7+2)/(4*16900))
#print(float((4+16900)*8+2)/(4*16900))
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
matrix_iteration = 0

zero_layer_neurons_number = rgb_matrixes[0]['red'].size
zero_layer_weights_matrix = get_zero_layer_weights_matrix(zero_layer_neurons_number, first_layer_neurons_number)
for rgb_matrix in rgb_matrixes:
    ALPHA = get_alpha(rgb_matrix['red'])
    while True:
        first_layer_output_values = rgb_matrix['red']*zero_layer_weights_matrix
        first_layer_weights_matrix = zero_layer_weights_matrix.H
        second_layer_output_values = first_layer_output_values*first_layer_weights_matrix
        ALPHA_QUOTE = get_alpha(first_layer_output_values)
        delta_values_matrix = second_layer_output_values-rgb_matrix['red']
        corrected_first_layer_weights_matrix = first_layer_weights_matrix - \
                                                   ALPHA_QUOTE*first_layer_output_values.H*delta_values_matrix
        corrected_zero_layer_weights_matrix = zero_layer_weights_matrix - \
                                                  ALPHA*rgb_matrix['red'].H * \
                                                  delta_values_matrix*first_layer_weights_matrix.H
        print('BUGSGS')
        mean_square_error = delta_values_matrix*delta_values_matrix.H
        #print('max error', mean_square_error, ' < ', MAX_ERROR)
        if mean_square_error < MAX_ERROR:
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
            break
        else:
            zero_layer_weights_matrix = corrected_zero_layer_weights_matrix
            first_layer_weights_matrix = corrected_first_layer_weights_matrix

image.putdata(newData)
image.save('out.jpg')
