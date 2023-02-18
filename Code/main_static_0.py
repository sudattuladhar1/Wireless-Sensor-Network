# Link is Probabilistic depending on the connection

import numpy as np
from q_learning import QLearning
from sensors import Sensors
import seaborn as sns
import matplotlib.pyplot as plt

print 'Static_0: Probabilistic Link Program Started'

sensors = Sensors(scenario = 'STATIC_0')

channel_quality_matrix = sensors.get_channel_quality()
print 'Channel Quality Matrix: '
print channel_quality_matrix

q = QLearning(channel_quality_matrix = channel_quality_matrix)
q.run()

print 'Final Q value'
print q.get_Q()

for i in range(10):
	print 'Path: ',  q.get_path(5)

sensors.visualize(showRange = True)

# Specific path plot
sensors.show_path(q.get_path(5), color = 'r')

sensors.savefig('./Results/Layout_Static_0_Route')
sensors.end()


print 'Static_0: Probabilistic Link Program Ended'