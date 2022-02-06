import numpy as np
import random
import math

def relu(data):
    return np.maximum(0, data)


def do_nothing(data):
    return data


class Network:
    def __init__(self, inputs, hidden_layers, outputs, activation=None):
        self.count_inputs = inputs
        self.count_outputs = outputs
        self.count_layers = len(hidden_layers) + 1

        self.weights = []
        self.biases = []
        self.n_biases = inputs + sum(hidden_layers) + outputs
        self.n_weights = 0
        last_layer_size = inputs
        for e in hidden_layers + [self.count_outputs]:
            self.weights.append(np.random.rand(e, last_layer_size))
            self.n_weights += last_layer_size * e
            self.biases.append(np.random.rand(e))
            last_layer_size = e
        if activation is None:
            self.activation = [relu] * (self.count_layers - 1) + [do_nothing]
        else:
            self.activation = activation

    def run(self, inputs):
       # return[100*math.pi*4/3,400]
        values = inputs
        for i in range(self.count_layers):
            values = np.dot(values, self.weights[i].T) + self.biases[i]
            values = self.activation[i](values)
        return values

    def clone(self):
        new = Network(0, [], 0)
        new.count_inputs = self.count_inputs
        new.count_outputs = self.count_outputs
        new.count_layers = self.count_layers
        new.weights = [e.copy() for e in self.weights]
        new.biases = [e.copy() for e in self.biases]
        new.activation = [e for e in self.activation]
        new.n_weights=self.n_weights
        new.n_biases=self.n_biases
        return new

    def mutate(self, amount):
        for i in range(amount):
           # print(0, self.n_weights + self.n_biases - 1)
            target = random.randint(0, self.n_weights + self.n_biases - 1)
            for biases in self.biases:
                if biases.shape[0] > target:
                    biases[target] *= 4 * random.random() - 2
                    continue
                target -= biases.shape[0]
            for weights in self.weights:
                if weights.shape[0] * weights.shape[1] > target:
                    weights[int(target / weights.shape[1])][target % weights.shape[1]] *= 4 * random.random() - 2
                    continue
                else:
                    target -= weights.shape[0] * weights.shape[1] > target
