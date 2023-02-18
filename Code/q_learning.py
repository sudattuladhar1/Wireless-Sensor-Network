# https://www.youtube.com/watch?v=LzaWrmKL1Z4
# example: reinforcement learning

import numpy as np
import sys

class QLearning:

	def __init__(self, channel_quality_matrix):
		#np.random.seed(0)
		self.__N = channel_quality_matrix.shape[0]
		self.__gamma = 0.8
		self.__alpha = 0.2

		self.__R = np.multiply(np.matrix(channel_quality_matrix),1.0)
		self.__Q = np.matrix(np.zeros([self.__N, self.__N]))

	# This function returns all available actions in the state given as an argument
	def __available_actions(self, state):
		current_state_row = self.__R[state,]
		av_act = np.where(current_state_row > 0)[1]
		return av_act

	# This function chooses at random which action to be performed within the range of all the available actions
	def __sample_next_action(self, available_act):
		next_action = int(np.random.choice(available_act, 1))
		return next_action

	# This function updates the Q-matrix according to the path selected and the Q learning algorithm
	def __update(self, current_state, action):
		# Find arg Max[Q(next_state, all actions)]
		next_state = action # For Find Find Problem
		max_index = np.where(self.__Q[next_state, ] == np.max(self.__Q[next_state, ]))[1]

		# If multiple indices with max value, randomly choose one
		if max_index.shape[0] > 1:
			max_index = int(np.random.choice(max_index, size = 1))
		else:
			max_index = int(max_index)
		max_value = self.__Q[next_state, max_index]

		# Q learning formula
		# if np.random.uniform() < self.__channel_quality_matrix[current_state, action]:
		# 	reward = self.__R[current_state, action]
		# else:
		# 	reward = -1.0
		
		#reward = self.__R[current_state, action]
		reward = self.__R[current_state, action]
		self.__Q[current_state, action] = (1 - self.__alpha) * self.__Q[current_state, action] + self.__alpha * (reward + self.__gamma * max_value)	

	# Train over 10,000 iterations, (Re-iterate the process above)
	def __training(self):
		for i in range(10000):
		#for i in range(5):
			# Start with random State
			current_state = np.random.randint(0, self.__N)#int(self.__Q.shape[0]))
			# Determine all available actions from the current_state
			available_act = self.__available_actions(current_state)
			# Check for empty available action
			if len(available_act) == 0:
				continue

			# Take sample action from available action pool
			action = self.__sample_next_action(available_act)

			# Update the Q matrix based on channel probability
			#if np.random.uniform() < self.__channel_quality_matrix[current_state][action]:
			self.__update(current_state, action)

		# Normalizing Q values
		self.__Q = self.__Q / np.max(self.__Q) * 100

	def get_path(self, current_state):
		steps = [current_state]
		count = 0
		while current_state != 0:
			count = count + 1
			if(np.max(self.__Q[current_state,]) < 10**-6) | (count > self.__N):
				steps = [current_state]
				#print 'No Path lead to destination starting at : ', current_state
				break
			next_step_index = np.where(self.__Q[current_state, ] == np.max(self.__Q[current_state,]))[1]

			if next_step_index.shape[0] > 1:
				next_step_index = int(np.random.choice(next_step_index, size = 1))
			else:
				next_step_index = int(next_step_index)

			steps.append(next_step_index)
			current_state = next_step_index

		return steps

	def get_Q(self):
		return self.__Q

	def run(self):
		self.__training()


###############################################################################
if __name__ == '__main__':

	print 'Static Position Q-Learning Program Started'

	print 'Static Position Q-Learning Program Ended'











