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
    
    def get_genome(self):
        
        genome = np.concatenate([
            self.weights_input_hidden.flatten(),
            self.weights_hidden_output.flatten(),
            self.biases_hidden,
            self.biases_output
        ])
        return genome
    
    def set_genome(self, genome):
        idx = 0
        
        size = self.input_nodes * self.hidden_nodes
        self.weights_input_hidden = genome[idx:idx + size].reshape(self.hidden_nodes, self.input_nodes)
        idx += size

        size = self.hidden_nodes * self.output_nodes
        self.weights_hidden_output = genome[idx:idx + size].reshape(self.output_nodes, self.hidden_nodes)
        idx += size

        self.biases_hidden = genome[idx:idx + self.hidden_nodes]
        idx += self.hidden_nodes

        self.biases_output = genome[idx:idx + self.output_nodes]

    def sigmoid(self, x):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))  # Clip to prevent overflow
    
    def tanh(self, x):
        """Tanh activation function - ideal for neuroevolution"""
        return np.tanh(np.clip(x, -500, 500))  # Clip to prevent overflow
    
    def predict(self, inputs):
        hidden_output = np.dot(self.weights_input_hidden, inputs) + self.biases_hidden
        hidden_output = self.tanh(hidden_output)
        raw_output = np.dot(self.weights_hidden_output, hidden_output) + self.biases_output
        predictions = softmax(raw_output)
        action = np.argmax(predictions)
        return action