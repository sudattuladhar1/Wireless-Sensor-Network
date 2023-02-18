import numpy as np
from q_learning import QLearning
from sensors import Sensors
import seaborn as sns
import matplotlib.pyplot as plt

print 'Random Dense Program Started'

sensors = Sensors(scenario = 'RANDOM_DENSE')

channel_quality_matrix = sensors.get_channel_quality()

q = QLearning(channel_quality_matrix = channel_quality_matrix)
q.run()

#print 'Final Q value'
#print q.get_Q()

print 'Path: ',  q.get_path(10)
print 'Path: ',  q.get_path(25)
print 'Path: ',  q.get_path(50)
print 'Path: ',  q.get_path(75)
print 'Path: ',  q.get_path(99)
print 'Path: ',  q.get_path(41)
print 'Path: ',  q.get_path(67)

sensors.visualize(showRange = False)

# Specific path plot
sensors.show_path(q.get_path(10), color = 'b')
sensors.show_path(q.get_path(25), color = 'g')
sensors.show_path(q.get_path(50), color = 'r')
sensors.show_path(q.get_path(75), color = 'c')
sensors.show_path(q.get_path(99), color = 'm')
sensors.show_path(q.get_path(41), color = 'y')
sensors.show_path(q.get_path(67), color = 'k')



sensors.savefig('./Results/Layout_Random_Dense_Route')
sensors.end()


print 'Random Dense Program Ended'