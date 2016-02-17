from PIL import Image
from methods import divide_to_particles, get_rgb_values, get_rgb_matrixes, get_color_output_values, \
    process_teaching_for_color, get_new_rgb_values

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

new_rgb_values = get_new_rgb_values(rgb_matrixes, RED_zero_layer_weights, RED_first_layer_weights,
                                                  GREEN_zero_layer_weights, GREEN_first_layer_weights,
                                                  BLUE_zero_layer_weights, BLUE_first_layer_weights)

buf = 0
c_j = 0
width, height = image_size
print('sdg', height)

for i in range(0, len(newData), 2):
    try:
        newData[i + buf] = new_rgb_values['red'][c_j][0], new_rgb_values['green'][c_j][0], new_rgb_values['blue'][c_j][0]
        newData[i + buf + 1] = new_rgb_values['red'][c_j][1], new_rgb_values['green'][c_j][1], new_rgb_values['blue'][c_j][1]
        newData[i + buf + width] = new_rgb_values['red'][c_j][2], new_rgb_values['green'][c_j][2], new_rgb_values['blue'][c_j][2]
        newData[i + buf + width + 1] = new_rgb_values['red'][c_j][3], new_rgb_values['green'][c_j][3], new_rgb_values['blue'][c_j][3]
        if (i+2)%width == 0:
            buf += width
        c_j += 1
        print(c_j)
    except IndexError:
        break

"""
rm_rf = 0
for i in range(0, len(newData), 4):
    newData[i] = new_rgb_values['red'][rm_rf][0], new_rgb_values['green'][rm_rf][0], new_rgb_values['blue'][rm_rf][0]
    newData[i + 1] = new_rgb_values['red'][rm_rf][1], new_rgb_values['green'][rm_rf][1], new_rgb_values['blue'][rm_rf][1]
    newData[i + 2] = new_rgb_values['red'][rm_rf][2], new_rgb_values['green'][rm_rf][2], new_rgb_values['blue'][rm_rf][2]
    newData[i + 3] = new_rgb_values['red'][rm_rf][3], new_rgb_values['green'][rm_rf][3], new_rgb_values['blue'][rm_rf][3]
    rm_rf += 1
    print(rm_rf)
"""

image.putdata(newData)
image.save('out.jpg')
