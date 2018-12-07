from pynput.keyboard import Key, Listener
import numpy as np

class QWOP_Controller:

	def __init__(self):
		self.reset()
		listener = Listener(on_press=self.on_press, on_release=self.on_release)
		listener.start()

	def reset(self):
		self.q_value = 0.0
		self.w_value = 0.0
		self.o_value = 0.0
		self.p_value = 0.0

	def predict(self, state):
		return np.array([self.q_value, self.w_value, self.o_value, self.p_value])
		
	def on_press(self, key):
		if key == Key.alt:
			self.q_value = 1.0
		elif key == Key.cmd:
			self.w_value = 1.0
		elif key == Key.ctrl_r:
			self.o_value = 1.0
		elif key == Key.shift_r:
			self.p_value = 1.0

	def on_release(self, key):
		if key == Key.alt:
			self.q_value = -1.0
		elif key == Key.cmd:
			self.w_value = -1.0
		elif key == Key.ctrl_r:
			self.o_value = -1.0
		elif key == Key.shift_r:
			self.p_value = -1.0


class QWOP_Controller2:

	def __init__(self):
		self.reset()
		listener = Listener(on_press=self.on_press, on_release=self.on_release)
		listener.start()

	def reset(self):
		self.action = np.zeros(4)
		self.joint_state = np.zeros(4).astype(bool)

	def predict(self, state):
		self.action[0] += -0.2 + self.joint_state[0] * 0.4
		self.action[1] += -0.2 + self.joint_state[1] * 0.4
		self.action[2] += 0.2 + self.joint_state[2] * -0.4
		self.action[3] += 0.2 + self.joint_state[3] * -0.4
		self.action = np.clip(self.action, -1.0, 1.0)
		return self.action

	def on_press(self, key):
		if key == Key.alt:
			self.joint_state[0] = True
		elif key == Key.cmd:
			self.joint_state[1] = True
		elif key == Key.ctrl_r:
			self.joint_state[2] = True
		elif key == Key.shift_r:
			self.joint_state[3] = True

	def on_release(self, key):
		if key == Key.alt:
			self.joint_state[0] = False
		elif key == Key.cmd:
			self.joint_state[1] = False
		elif key == Key.ctrl_r:
			self.joint_state[2] = False
		elif key == Key.shift_r:
			self.joint_state[3] = False










