import numpy as np
from q_learning import QLearning
from sensors import Sensors
import seaborn as sns
import matplotlib.pyplot as plt

print 'Random Sparse Program Started'

sensors = Sensors(scenario = 'RANDOM_SPARSE')

channel_quality_matrix = sensors.get_channel_quality()

q = QLearning(channel_quality_matrix = channel_quality_matrix)
q.run()

print 'Final Q value'
print q.get_Q()

for i in range(11):
	print 'Path: ',  q.get_path(i)

sensors.visualize(showRange = True)

# Specific path plot
sensors.show_path(q.get_path(1), color = 'b')
sensors.show_path(q.get_path(2), color = 'g')
sensors.show_path(q.get_path(3), color = 'r')
# sensors.show_path(q.get_path(4), color = 'c')
# sensors.show_path(q.get_path(5), color = 'm')
# sensors.show_path(q.get_path(6), color = 'y')
# sensors.show_path(q.get_path(7), color = 'k')


sensors.savefig('./Results/Layout_Random_Sparse_Route_Run3')
#sensors.savefig('./Results/Layout_Random_Sparse_Route_11')
sensors.end()


print 'Random Sparse Program Ended'