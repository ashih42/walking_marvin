from colorama import Fore, Back, Style
import matplotlib.pyplot as plt
import numpy as np
import os
import gym
import envs

'''

Layer 1		24 + 1 -> 24
Layer 2		24 + 1 -> 24
Layer 3		24 + 1 -> 4
Layer 4		4

Theta_1		25 x 24
Theta_2		25 x 24
Theta_3		25 x 4

'''

class NeuralNetwork:
	np.random.seed(42)

	__LEARNING_RATE = 0.1
	__SIGMA = 0.1
	__N_MUTANTS = 10
	__SCORE_CACHE_SIZE = 100
	__PLOTS_DIRECTORY = 'Evolution_Plots/'

	def __init__(self, env):
		self.env = env
		self.filename = 'Default'
		
		self.__generation = 0
		self.__average_mutant_scores = []
		self.__generation_list = []
		self.__current_fitness_list = []
		self.__average_fitness_per_generation_list = []
		self.__average_fitness_over_generations_list = []

		self.Theta_1 = np.zeros((25, 24))
		self.Theta_2 = np.zeros((25, 24))
		self.Theta_3 = np.zeros((25, 4))

	# input X is np.array of shape (24,)
	# output is np.array of shape (4, )
	def get_action(self, X):
		X = X[np.newaxis, :]

		A_1 = np.tanh(X)
		A_1 = np.c_[1, A_1]

		A_2 = A_1 @ self.Theta_1
		A_2 = np.maximum(A_2, 0, A_2)
		A_2 = np.c_[1, A_2]

		A_3 = A_2 @ self.Theta_2
		A_3 = np.maximum(A_3, 0, A_3)
		A_3 = np.c_[1, A_3]

		A_4 = A_3 @ self.Theta_3
		A_4 = np.tanh(A_4)
		return A_4.flatten()

	def train(self, t_max):
		self.__generation += 1
		mutants = [ None ] * self.__N_MUTANTS
		mutant_scores = np.empty(self.__N_MUTANTS)
		for i in range(self.__N_MUTANTS):
			mutants[i] = self.__mutate()
			mutant_scores[i] = mutants[i].__get_fitness(t_max)
		self.__measure_mutants_performance(t_max, mutant_scores)
		self.__update_parent_from_mutants(mutants, mutant_scores)

	def __mutate(self):
		mutant = NeuralNetwork(self.env)
		mutant.Theta_1 = self.Theta_1 + np.random.randn(*self.Theta_1.shape) * self.__SIGMA
		mutant.Theta_2 = self.Theta_2 + np.random.randn(*self.Theta_2.shape) * self.__SIGMA
		mutant.Theta_3 = self.Theta_3 + np.random.randn(*self.Theta_3.shape) * self.__SIGMA
		return mutant

	def __get_fitness(self, t_max, n_episodes=1):
		total_reward = 0
		for episode in range(n_episodes):
			state = self.env.reset()
			for t in range(t_max):
				action = self.get_action(state)
				state, reward, done, info = self.env.step(action)
				total_reward += reward
				if done:
					break
		return total_reward

	def __measure_mutants_performance(self, t_max, mutant_scores):
		current_fitness = self.__get_fitness(t_max)
		best_fitness = np.max(mutant_scores)
		worst_fitness = np.min(mutant_scores)
		average_fitness = np.mean(mutant_scores)

		self.__average_mutant_scores.append(average_fitness)
		if len(self.__average_mutant_scores) > self.__SCORE_CACHE_SIZE:
			del self.__average_mutant_scores[0]
		average_over_generations = np.mean(self.__average_mutant_scores)

		print(Fore.GREEN, 'Generation', self.__generation, Fore.RESET)
		print(Fore.BLUE, 'Current: ', Fore.RESET, '%.3f' % current_fitness)
		print(Fore.BLUE, 'Mutants Average: ', Fore.RESET, '%.3f' % average_fitness,
			Fore.BLUE, ' Best: ', Fore.RESET, '%.3f' % best_fitness,
			Fore.BLUE, ' Worst: ', Fore.RESET, '%.3f' % worst_fitness,
			Fore.BLUE, ' Average (Last 100 Gen): ', Fore.RESET, '%.3f' % average_over_generations)
		self.__generation_list.append(self.__generation)
		self.__current_fitness_list.append(current_fitness)
		self.__average_fitness_per_generation_list.append(average_fitness)
		self.__average_fitness_over_generations_list.append(average_over_generations)

	def __update_parent_from_mutants(self, mutants, mutant_scores):
		std = (mutant_scores - np.mean(mutant_scores)) / np.std(mutant_scores)
		Grad_1 = np.zeros(self.Theta_1.shape)
		Grad_2 = np.zeros(self.Theta_2.shape)
		Grad_3 = np.zeros(self.Theta_3.shape)
		for i in range(self.__N_MUTANTS):
			Grad_1 += mutants[i].Theta_1 * std[i]
			Grad_2 += mutants[i].Theta_2 * std[i]
			Grad_3 += mutants[i].Theta_3 * std[i]
		self.Theta_1 += self.__LEARNING_RATE / (self.__N_MUTANTS * self.__SIGMA) * Grad_1
		self.Theta_2 += self.__LEARNING_RATE / (self.__N_MUTANTS * self.__SIGMA) * Grad_2
		self.Theta_3 += self.__LEARNING_RATE / (self.__N_MUTANTS * self.__SIGMA) * Grad_3

	def save_plots(self):
		self.__init_plots()
		self.__update_plots()
		self.__save_plots()
		
	def __init_plots(self):
		try:
			os.stat(self.__PLOTS_DIRECTORY)
		except:
			os.mkdir(self.__PLOTS_DIRECTORY)
		self.__fig = plt.figure(figsize=(18, 6))
		self.__fig.tight_layout()
		self.__ax_1 = self.__fig.add_subplot(1, 3, 1)
		self.__ax_2 = self.__fig.add_subplot(1, 3, 2)
		self.__ax_3 = self.__fig.add_subplot(1, 3, 3)

	def __update_plots(self):
		# Current Fitness
		self.__ax_1.clear()
		self.__ax_1.plot(self.__generation_list, self.__current_fitness_list)
		self.__ax_1.set_xlabel('Generation')
		self.__ax_1.set_ylabel('Fitness')
		self.__ax_1.set_title('Current Fitness')
		# Mutants Average Fitness
		self.__ax_2.clear()
		self.__ax_2.plot(self.__generation_list, self.__average_fitness_per_generation_list)
		self.__ax_2.set_xlabel('Generation')
		self.__ax_2.set_ylabel('Fitness')
		self.__ax_2.set_title('Mutants Average Fitness')
		# Average Fitness over Generations
		self.__ax_3.clear()
		self.__ax_3.plot(self.__generation_list, self.__average_fitness_over_generations_list)
		self.__ax_3.set_xlabel('Generation')
		self.__ax_3.set_ylabel('Fitness')
		self.__ax_3.set_title('Average of Mutants Average Fitness\n(Last 100 Generations)')

	def __save_plots(self):
		filename = self.__PLOTS_DIRECTORY + self.filename + '.png'
		plt.savefig(filename)
		print('Saved plots in ' + Fore.BLUE + filename + Fore.RESET)
		
