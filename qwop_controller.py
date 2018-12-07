from pynput.keyboard import Key, Listener
import numpy as np

class Extreme_QWOP_Controller:

	def __init__(self):
		self.reset()
		listener = Listener(on_press=self.on_press, on_release=self.on_release)
		listener.start()

	def reset(self):
		self.__action = np.zeros(4)

	def get_action(self):
		return self.__action
		
	def on_press(self, key):
		if key == Key.alt:
			self.__action[0] = 1.0
		elif key == Key.cmd:
			self.__action[1] = 1.0
		elif key == Key.ctrl_r:
			self.__action[2] = 1.0
		elif key == Key.shift_r:
			self.__action[3] = 1.0

	def on_release(self, key):
		if key == Key.alt:
			self.__action[0] = -1.0
		elif key == Key.cmd:
			self.__action[1] = -1.0
		elif key == Key.ctrl_r:
			self.__action[2] = -1.0
		elif key == Key.shift_r:
			self.__action[3] = -1.0

class Easy_QWOP_Controller:

	def __init__(self):
		self.reset()
		listener = Listener(on_press=self.on_press, on_release=self.on_release)
		listener.start()

	def reset(self):
		self.__action = np.zeros(4)
		self.__turn_direction = np.zeros(4).astype(bool)

	def get_action(self):
		self.__update_action()
		return self.__action

	def __update_action(self):
		self.__action[0] += -0.2 + self.__turn_direction[0] * 0.4
		self.__action[1] += -0.2 + self.__turn_direction[1] * 0.4
		self.__action[2] += 0.2 + self.__turn_direction[2] * -0.4
		self.__action[3] += 0.2 + self.__turn_direction[3] * -0.4
		self.__action = np.clip(self.__action, -1.0, 1.0)

	def on_press(self, key):
		if key == Key.alt:
			self.__turn_direction[0] = True
		elif key == Key.cmd:
			self.__turn_direction[1] = True
		elif key == Key.ctrl_r:
			self.__turn_direction[2] = True
		elif key == Key.shift_r:
			self.__turn_direction[3] = True

	def on_release(self, key):
		if key == Key.alt:
			self.__turn_direction[0] = False
		elif key == Key.cmd:
			self.__turn_direction[1] = False
		elif key == Key.ctrl_r:
			self.__turn_direction[2] = False
		elif key == Key.shift_r:
			self.__turn_direction[3] = False
