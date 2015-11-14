from PIL import Image
from numpy import matrix
import random

ALPHA = 0.00001
MAX_ERROR = 0.0001

image = Image.open("1.png").convert("RGB")
image_size = image.size
pixels = image.getdata()

newData = []
red = []
green = []
blue = []
for pixel in pixels:
    r, g, b = pixel
    red.append(r)
    green.append(g)
    blue.append(b)

red_input_matrix = matrix(red)
green_input_matrix = matrix(green)
blue_input_matrix = matrix(blue)

zero_layer_neurons_number = len(red or green or blue)
first_layer_neurons_number = len(red or green or blue)/2

zero_layer_weights = []
for i in range(zero_layer_neurons_number):
    neuron_weights = []
    for j in range(first_layer_neurons_number):
        neuron_weights.append(random.uniform(-1, 1))
    zero_layer_weights.append(neuron_weights)

zero_layer_weights_matrix = matrix(zero_layer_weights)
first_layer_weights_matrix = zero_layer_weights_matrix.H

first_layer_output_values = red_input_matrix*zero_layer_weights_matrix
#print(first_layer_output_values)
#print(first_layer_weights_matrix)
output_values = first_layer_output_values*first_layer_weights_matrix
#print(output_values)
delta_values_matrix = output_values-red_input_matrix
#print(delta_values_matrix)

corrected_first_layer_weights_matrix = first_layer_weights_matrix - ALPHA*first_layer_output_values.H*delta_values_matrix
print(first_layer_weights_matrix)
print(corrected_first_layer_weights_matrix)

corrected_zero_layer_weights_matrix = zero_layer_weights_matrix - ALPHA*red_input_matrix.H*delta_values_matrix*corrected_first_layer_weights_matrix.H

print(corrected_zero_layer_weights_matrix)

MAX_ERROR = 0.0001*first_layer_neurons_number

#mean_square_error = delta_values_matrix*delta_values_matrix
#print(mean_square_error)

image.putdata(newData)
image.save('out.jpg')
