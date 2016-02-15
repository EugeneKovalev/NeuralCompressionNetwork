from PIL import Image
from methods import divide_to_particles, get_rgb_values, get_rgb_matrixes, get_color_output_values, \
    process_teaching_for_color

image = Image.open("Test_Image.png").convert("RGB")
image_size = image.size
pixels = image.getdata()
newData = []
for x in pixels:
    newData.append((0, 0, 0))

image_particles = divide_to_particles(image_size, pixels)

rgb_values = get_rgb_values(image_particles)

rgb_matrixes = get_rgb_matrixes(rgb_values)

first_layer_neurons_number = input('Enter the number of neurons in the first layer: ')
MAX_ERROR = input('Enter the MAX ERROR value: ')

RED_zero_layer_weights, RED_first_layer_weights = process_teaching_for_color(MAX_ERROR, first_layer_neurons_number, rgb_matrixes, 'red')

GREEN_zero_layer_weights, GREEN_first_layer_weights = process_teaching_for_color(MAX_ERROR, first_layer_neurons_number, rgb_matrixes, 'green')

BLUE_zero_layer_weights, BLUE_first_layer_weights = process_teaching_for_color(MAX_ERROR, first_layer_neurons_number, rgb_matrixes, 'blue')

print('JESUS CHRIST')

new_rgb_values = {'red': None, 'green': None, 'blue': None}

for rgb_matrix in rgb_matrixes:
    RED_latent_layer = rgb_matrix['red'] * RED_zero_layer_weights
    RED_output_layer = RED_latent_layer * RED_first_layer_weights
    GREEN_latent_layer = rgb_matrix['green'] * GREEN_zero_layer_weights
    GREEN_output_layer = GREEN_latent_layer * GREEN_first_layer_weights
    BLUE_latent_layer = rgb_matrix['blue'] * BLUE_zero_layer_weights
    BLUE_output_layer = BLUE_latent_layer * BLUE_first_layer_weights
    for r in list(RED_output_layer.flat):
        print(int((r + 1) * 255 / 2))
    for g in list(GREEN_output_layer.flat):
        print(int((g + 1) * 255 / 2))
    for b in list(BLUE_output_layer.flat):
        print(int((b + 1) * 255 / 2))


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

#RSLA = get_color_output_values(rgb_matrix['red'], zero_layer_weights_matrix)
#print(RSLA)
#GREEN_second_layer_output_values = get_color_output_values(rgb_matrix['green'], zero_layer_weights_matrix)
#BLUE_second_layer_output_values = get_blue_output_values(rgb_matrix['blue'], zero_layer_weights_matrix)
#new_data_iteration = 0
#for r, g, b in newData:  # FIVE
    #RED_changed_color_value = RED_second_layer_output_values.flat[new_data_iteration]
    #RED_changed_color_value = int((RED_changed_color_value + 1) * 255 / 2)
    #GREEN_changed_color_value = GREEN_second_layer_output_values.flat[new_data_iteration]
    #GREEN_changed_color_value = int((GREEN_changed_color_value + 1) * 255 / 2)
    #BLUE_changed_color_value = BLUE_second_layer_output_values.flat[new_data_iteration]
    #BLUE_changed_color_value = int((BLUE_changed_color_value + 1) * 255 / 2)
    #r,g,b = RED_changed_color_value, 0, 0
    #new_data_iteration += 1

image.putdata(newData)
image.save('out.jpg')
