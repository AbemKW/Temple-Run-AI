import environment
import numpy as np
# full connected multi-layer neural network model
# inference only
# no external dependencies
def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

class NeuralNetwork:
    def __init__(self, input_size, hidden_layers, output_size):
        self.input_nodes = input_size
        self.hidden_nodes = hidden_layers
        self.output_nodes = output_size

        self.weights_input_hidden = np.random.uniform(-1, 1, (self.hidden_nodes, self.input_nodes))
        self.weights_hidden_output = np.random.uniform(-1, 1, (self.output_nodes, self.hidden_nodes))

        self.biases_hidden = np.random.uniform(-1, 1, (self.hidden_nodes))
        self.biases_output = np.random.uniform(-1, 1, (self.output_nodes))
    def forward(self, inputs):
        hidden_output = np.dot(self.weights_input_hidden, inputs) + self.biases_hidden
        hidden_output = self.sigmoid(hidden_output)
        final_output = np.dot(self.weights_hidden_output, hidden_output) + self.biases_output
        final_output = softmax(final_output)
        return final_output