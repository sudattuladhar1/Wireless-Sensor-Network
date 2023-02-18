# Sensor Distribution

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import spatial
import sys


class Sensors:

	def __init__(self, scenario):
		# Initialize Sensor Positions
		if scenario == 'STATIC_0':
			self.__initialize_position_static_0()
		elif scenario == 'STATIC_1':
			self.__initialize_position_static_1()
		elif scenario == 'STATIC_2':
			self.__initialize_position_static_2()
		elif scenario == 'RANDOM_SPARSE':
			self.__initialize_position_random(numNode = 20, radius = 0.3)
		elif scenario == 'RANDOM_DENSE':
			self.__initialize_position_random(numNode = 100, radius = 0.2)
		else:
			print 'Initialization Error: Scenario = ', scenario
			sys.exit()


	def __initialize_position_static(self):
		self.__df = pd.DataFrame(columns = ['X', 'Y'])
		# Add Add destination
		self.__df = self.__df.append({'X' : 0, 'Y' : 0.5}, ignore_index = True)
		# Add Nodes
		self.__df = self.__df.append({'X' : 0.35, 'Y' : 0.4}, ignore_index = True)
		self.__df = self.__df.append({'X' : 0.35, 'Y' : 0.6}, ignore_index = True)
		self.__df = self.__df.append({'X' : 0.65, 'Y' : 0.4}, ignore_index = True)
		self.__df = self.__df.append({'X' : 0.65, 'Y' : 0.6}, ignore_index = True)
		self.__df = self.__df.append({'X' : 1.0, 'Y' : 0.5}, ignore_index = True)
		# Define Visibility Radius
		self.__visibility_radius = 0.4
		self.__N = self.__df.shape[0]

	def __initialize_position_static_0(self):
		print 'Scenario Static 0'
		self.__initialize_position_static()
		self.__calc_channel_quality()

	def __initialize_position_static_1(self):
		print 'Scenario Static 1'
		self.__initialize_position_static()
		#							Action	0	   1      2      3     4     5			State
		self.__channel_quality = np.array([[100.0, 100.0, 100.0, 0.00, 0.00, 0.00], 	# 0
										   [100.0, 0.00,  0.50,  0.70, 0.50, 0.00],		# 1
										   [100.0, 0.50,  0.00,  0.50, 0.80, 0.00],		# 2
										   [0.00,  0.70,  0.50,  0.00, 0.50, 0.90],		# 3
										   [0.00,  0.50,  0.80,  0.50, 0.00, 0.85],		# 4
										   [0.00,  0.00,  0.00,  0.90, 0.85, 0.00]])	# 5
	def __initialize_position_static_2(self):
		print 'Scenario Static 2'
		self.__initialize_position_static()
		#							Action	0	   1      2      3     4     5			State
		self.__channel_quality = np.array([[100.0, 100.0, 100.0, 0.00, 0.00, 0.00], 	# 0
										   [100.0, 0.00,  0.50,  0.50, 0.80, 0.00],		# 1
										   [100.0, 0.50,  0.00,  0.80, 0.50, 0.00],		# 2
										   [0.00,  0.50,  0.80,  0.00, 0.50, 0.95],		# 3
										   [0.00,  0.80,  0.50,  0.50, 0.00, 0.90],		# 4
										   [0.00,  0.00,  0.00,  0.95, 0.90, 0.00]])	# 5

			
	def __initialize_position_random(self, numNode, radius):
		#np.random.seed(442)
		self.__df = pd.DataFrame(columns = ['X', 'Y'])
		# Add Add destination
		self.__df = self.__df.append({'X' : 0.5, 'Y' : 0.5}, ignore_index = True)
		# Add Nodes
		for i in range(numNode):
			self.__df = self.__df.append({'X' : np.random.uniform(), 'Y' : np.random.uniform()}, ignore_index = True)
		
		# Define Visibility Radius
		self.__visibility_radius = radius
		self.__N = self.__df.shape[0]
		# Define Channel Quality
		# Calculate channel quality matrix
		#self.__channel_quality = np.ones((numNode + 1, numNode + 1))
		self.__calc_channel_quality()

	def get_channel_quality(self):
		return self.__channel_quality
		#return 1

	def __calc_channel_quality(self):
		#print 'Visibility radius: ', self.__visibility_radius
		dist = spatial.distance.cdist(self.__df, self.__df, 'euclidean')
		#print(np.round(dist, 2))

		self.__channel_quality = np.zeros(shape = (self.__N, self.__N))

		for i in range(self.__N):
			for j in range(self.__N):
				#print dist[0][j],
				#self.__channel_quality[0][j] = 111
				if (dist[i][j] <= self.__visibility_radius) & (i != j):
					self.__channel_quality[i][j] = np.round(np.random.uniform(), 2)
				 	self.__channel_quality[j][i] = np.round(np.random.uniform(), 2)

				if dist[0][j] <= self.__visibility_radius:
				 	self.__channel_quality[0][j] = 100.0
				 	self.__channel_quality[j][0] = 100.0

	def show_path(self, path, color = 'k'):
		for i in range(len(path) - 1):
			x = self.__df.iloc[path[i]]['X']
			y = self.__df.iloc[path[i]]['Y']
			dx = self.__df.iloc[path[i + 1]]['X'] - x
			dy = self.__df.iloc[path[i + 1]]['Y'] - y
			self.__ax.add_artist(plt.Arrow(x, y, dx, dy, width = 0.03, color = color))
		#plt.draw()

	def visualize(self, showRange = True, showLabel = True):
		self.__fig, self.__ax = plt.subplots(1, 1)
		self.__df.plot.scatter(x = 'X', y = 'Y', c = 'DarkBlue', s = 120, linewidth = 0, ax = self.__ax)
		for k, v in self.__df.iterrows():
			if k == 0: # Indicating the sink node
				plt.scatter(v['X'], v['Y'], color = 'r')
			if showLabel == True:
				self.__ax.annotate(k, v, xytext=(5,-5), textcoords='offset points', 
					family='sans-serif', fontsize=10, color='darkslategrey')
			if showRange == True:
				self.__ax.add_artist(plt.Circle((v['X'], v['Y']), radius = self.__visibility_radius, 
					color = 'r', linestyle = '--', fill = False))

		plt.xlim([-0.1, 1.1])
		plt.ylim([0, 1])
		#plt.show(block = False)

	def savefig(self, filename):
		self.__fig.savefig(filename, dpi = 200)

	def end(self):
		plt.show()


if __name__ == '__main__':
	print 'Static Position Sensor Program Started'
	sensors = Sensors(scenario = 'STATIC')
	#sensors = Sensors(scenario = 'RANDOM_SPARSE')
	#sensors = Sensors(scenario = 'RANDOM_DENSE')

	# Get Channel Quality
	print 'Channel Quality'
	print '  0\t   1\t2\t 3\t  4\t   5\t6\t 7\t  8\t   9\t10'
	print '-----------------------------------------------------'
	print sensors.get_channel_quality()

	sensors.visualize(showRange = True)
	# Specific path plot
	#sensors.show_path([4, 3, 9, 0], color = 'm')
	#sensors.show_path([5, 4, 1, 0], color = 'm')
	#sensors.show_path([5, 3, 2, 0], color = 'r')

	#sensors.savefig('./Results/Layout2.png')
	sensors.end()

	print 'Static Position Sensor Program Ended'
