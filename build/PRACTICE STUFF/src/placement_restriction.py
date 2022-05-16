import random
import numpy as np

# while True:
#     # choose points
#     x, x1 = random.randint(0, 100), random.randint(0, 100)
#     y, y1 = random.randint(0, 100), random.randint(0, 100)
#     z, z1 = random.randint(0, 100), random.randint(0, 100)
#     # specify min distance
#     v = 100
#     # check suitability
#     if np.linalg.norm(np.array([x,x1]) - np.array([y,y1])) > v and np.linalg.norm(np.array([x,x1]) - np.array([z,z1])) > v and np.linalg.norm(np.array([y,y1]) - np.array([z,z1])) > v:
#         break

import matplotlib.pyplot as plt
# plt.scatter([x,y,z, 100], [x1,y1,z1, 100])
# plt.show()



l1 = [0, 100,   0, 50]
l2 = [0,   0, 100, 50]

# l1 = [0, 100]
# l2 = [0,   0]

min = 10
max = 200
times = 0
for i in range(len(l1)-1):

    for j in range(i+1, len(l1)):

        if np.linalg.norm(np.array([l1[i], l2[i]]) - np.array([l1[j], l2[j]])) > min and np.linalg.norm(np.array([l1[i], l2[i]]) - np.array([l1[j], l2[j]])) < max:
            times+=1
            print(times)
            print("safe")
            print(f"{(l1[i], l2[i])}, {(l1[j], l2[j])}")
            print(np.linalg.norm(np.array([l1[i], l2[i]]) - np.array([l1[j], l2[j]])))
            print("="*30)

        else:
            times += 1
            print(times)
            print("unsafe")
            print(f"{(l1[i], l2[i])}, {(l1[j], l2[j])}")
            print(np.linalg.norm(np.array([l1[i], l2[i]]) - np.array([l1[j], l2[j]])))
            print("="*30)

