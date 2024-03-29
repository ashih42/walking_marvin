from colorama import Fore, Back, Style
import gym
import envs
import pickle

from evolution import NeuralNetwork
from qwop_controller import Easy_QWOP_Controller, Extreme_QWOP_Controller

class MarvinManager:

	def __init__(self, env_name):
		self.__env = gym.make(env_name)
		self.__model = NeuralNetwork(self.__env)

	def set_seed(self, seed):
		self.__env.seed(seed)

	def train(self, n_episodes, t_max, also_walk):
		for episode in range(n_episodes):
			print(Style.BRIGHT, 'Episode: ', episode + 1, Style.RESET_ALL)
			self.__model.train(t_max)
			if also_walk:
				self.__run_simulation(t_max)
		self.__model.save_plots()

	def walk(self, n_episodes):
		for episode in range(n_episodes):
			print(Style.BRIGHT, 'Episode: ', episode + 1, Style.RESET_ALL)
			total_reward = self.__run_simulation(t_max=None)
			print('  Total reward = %.3f' % total_reward)

	def __run_simulation(self, t_max):
		total_reward = 0
		state = self.__env.reset()
		if t_max is None:
			while True:
				self.__env.render(mode='human')
				action = self.__model.get_action(state)
				state, reward, done, info = self.__env.step(action)
				total_reward += reward
				if done:
					break
		else:
			for t in range(t_max):
				self.__env.render(mode='human')
				action = self.__model.get_action(state)
				state, reward, done, info = self.__env.step(action)
				total_reward += reward
				if done:
					break
		self.__env.close()
		return total_reward

	def qwop(self, n_episodes, is_extreme):
		self.__controller = Extreme_QWOP_Controller() if is_extreme else Easy_QWOP_Controller()
		for episode in range(n_episodes):
			print(Style.BRIGHT, 'Episode: ', episode + 1, Style.RESET_ALL)
			total_reward = self.__qwop_simulation()
			print('  Total reward = %.3f' % total_reward)

	def __qwop_simulation(self):
		self.__controller.reset()
		total_reward = 0
		state = self.__env.reset()
		while True:
			self.__env.render(mode='human')
			action = self.__controller.get_action()
			state, reward, done, info = self.__env.step(action)
			total_reward += reward
			if done:
				break
		self.__env.close()
		return total_reward

	def load(self, filename):
		print('Loading model parameters in ' + Fore.BLUE + filename + Fore.RESET)
		with open(filename, 'rb') as file:
			self.__model = pickle.load(file)
		self.__model.env = self.__env

	def set_filename(self, filename):
		self.__model.filename = filename

	def save(self, filename):
		path = 'saves/' + filename + '.dat'
		print('Saving model parameters in ' + Fore.BLUE + path + Fore.RESET)
		self.__model.save(path)
