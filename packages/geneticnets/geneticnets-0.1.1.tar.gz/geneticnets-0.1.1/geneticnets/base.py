# Author: 
# GitHub -> @javi22020
# Creation Date: 2024-02-21
import numpy as np
from typing import Literal, Generator, Iterator, Callable
import random as rn
import asyncio
class GeneticAlgorithm:
    class GeneticNet:
        def __init__(self, ID: int, layers: list[int], activation: Literal["sigmoid", "relu"]) -> None:
            self.ID = ID
            self.layers = layers
            self.activation = activation
            self.weights = [np.random.randn(layers[i], layers[i+1]) for i in range(len(layers)-1)]
        def __str__(self) -> str:
            return f"GeneticNet with ID {self.ID} with layers: {self.layers} and {self.activation} activation function."
        def copy(self):
            """Returns a copy of the network."""
            new_net = GeneticAlgorithm.GeneticNet(self.ID, self.layers, self.activation)
            new_net.weights = [w.copy() for w in self.weights]
            return new_net
        def save_weights(self, path: str) -> None:
            """Saves the weights of the network to a file."""
            np.save(path, self.weights)
        def load_weights(self, path: str) -> None:
            """Loads the weights of the network from a file."""
            self.weights = np.load(path, allow_pickle=True)
        def forward(self, input: np.ndarray) -> np.ndarray:
            """
            Forward pass of the network. Returns the output of the network given an input.
            """
            for w in self.weights:
                input = input @ w
                match self.activation:
                    case "sigmoid":
                        input = 1 / (1 + np.exp(-input))
                    case "relu":
                        input = np.maximum(0, input)
            return input
        def mutate(self, mutation_rate: float) -> None:
            """Mutates the weights of the network by adding random noise to them."""
            for w in self.weights:
                w += np.random.randn(*w.shape) * mutation_rate
            return self
        async def train_net_step_async(self, input_data: np.ndarray, mutation_rate: float):
            self.mutate(mutation_rate)
            result = self.forward(input_data)
            return result
    def __init__(self, popul_size: int, layers: list[int], activation: Literal["sigmoid", "relu"]) -> None:
        """Initializes the genetic algorithm with a population size, the layers of the networks, and an activation function."""
        self.popul_size = popul_size
        self.gen = [GeneticAlgorithm.GeneticNet(net_id, layers, activation) for net_id in range(popul_size)]
    def crossover(self, net1: GeneticNet, net2: GeneticNet, net_id: int) -> GeneticNet:
        new_net = GeneticAlgorithm.GeneticNet(net1.ID, net1.layers, net1.activation)
        new_net.weights = [net1.weights[i] if np.random.randn() > 0 else net2.weights[i] for i in range(len(net1.weights))]
        new_net.ID = net_id
        return new_net
    async def train_all_nets_step_async(self, input_data: np.ndarray, fitness: Callable, mutation_rate: float, top_n: int, verbose: bool) -> GeneticNet:
        """Performs a single step of training for all networks asynchronously."""
        results = await asyncio.gather(*[net.train_net_step_async(input_data, mutation_rate) for net in self.gen])
        fitnesses = [fitness(result) for result in results]
        if verbose:
            print(f"Average fitness: {np.mean(fitnesses)}")
        top_n_nets = [self.gen[n] for n in np.argsort(fitnesses)[-top_n:]]
        new_gen = [self.crossover(*rn.sample(top_n_nets, 2), net_id).mutate(mutation_rate) for net_id in range(self.popul_size)]
        self.gen = new_gen
        return top_n_nets[-1]
    def train(self, generations: int, data: Iterator, fitness: Callable, mutation_rate: float, top_n: int, verbose: bool = False):
        """
        Trains the genetic algoritm for a number of generations and returns the best network.\n
        The fitness function should take the output of the network and return a scalar value that represents the fitness of the network.\n
        Inputs:\n
        - generations: the number of generations to train the network for.\n
        - data: the data to train the network on. Should be a list of numpy arrays or generator.\n
        - fitness: the fitness function to evaluate the networks.\n
        - mutation_rate: the mutation rate of the networks.\n
        - top_n: the number of top networks to crossover from for the next generation.
        """
        for num in range(generations):
            print(f"Training generation {num+1}/{generations}...")
            for input_data in data:
                net = asyncio.run(self.train_all_nets_step_async(input_data=input_data, fitness=fitness, mutation_rate=mutation_rate, top_n=top_n, verbose=verbose))
        return net
    def live_train(self, generator: Generator, fitness: Callable, mutation_rate: float, top_n: int, verbose: bool = False):
        """
        Trains the genetic algorithm with a generator that yields data.\n
        The fitness function should take the output of the network and return a scalar value that represents the fitness of the network.\n
        Inputs:\n
        - generator: the generator that yields data to train the network on.\n
        - fitness: the fitness function to evaluate the networks.\n
        - mutation_rate: the mutation rate of the networks.\n
        - top_n: the number of top networks to crossover from for the next generation.
        """
        for data in generator:
            net = asyncio.run(self.train_all_nets_step_async(input_data=data, fitness=fitness, mutation_rate=mutation_rate, top_n=top_n, verbose=verbose))
            yield net