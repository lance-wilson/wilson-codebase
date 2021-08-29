#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   Homework_2_10a.py
#
# Purpose:
#   Plot zonal wind U as a function of time.
#
# Syntax:
#   python3 Homework_2_10a.py
#
# Modification History:
#   2020/01/30 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

i = np.arange(0,21)
time = np.arange(0,61,3)
u = np.array([3, 4, 3, 6, 6, 2, 5, 3, 7, 8, 5, 4, 3, 5, 2, 2, 4, 5, 3, 6, 5])

# The following three lines are so that the grid can be behind the dots.
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_axisbelow(True)
#plt.plot(time, u, marker='o')
plt.scatter(time, u)
plt.grid()
plt.title('Problem 10a')
plt.xlabel('Time (min)')
plt.ylabel('U (m/s)')
plt.xlim(-0.5, 60.5)
plt.ylim(0,9)
plt.xticks(time)

#plt.show()
plt.savefig('problem_10a.png', dpi=400)


