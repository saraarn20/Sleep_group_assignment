import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

x = [
95.1923076923077, 
94.08602150537635, 
94.24083769633508, 
95.23809523809523, 
94.24083769633508, 
90.98360655737704, 
89.16083916083916, 
94.6236559139785, 
97.45762711864407, 
89.36170212765957, 
91.796875, 
91.85606060606061, 
89.04109589041096, 
95.57344064386318, 
78.46153846153847, 
81.35593220338984, 
89.10891089108911, 
85.07462686567165, 
89.7196261682243, 
95.14563106796116, 
87.5, 
80.95238095238095, 
87.93103448275862, 
82.35294117647058, 
96.0, 
80.0, 
76.8, 
81.25, 
53.84615384615385, 
78.94736842105263, 
85.71428571428571, 
71.1864406779661, 
84.95575221238938, 
89.36170212765957, 
96.5909090909091, 
96.7741935483871, 
95.1923076923077, 
92.3076923076923, 
81.25, 
93.33333333333333, 
94.3820224719101, 
93.75, 
92.62435677530017, 
94.86166007905138, 
95.57522123893806, 
92.5, 
78.94736842105263, 
73.68421052631578, 
94.18604651162791, 
96.84210526315789, 
96.84210526315789, 
95.83333333333334, 
97.19222462203024, 
96.96969696969697, 
96.7032967032967, 
87.74509803921569, 
79.61538461538461, 
77.96257796257797, 
90.9090909090909, 
95.28907922912205, 
88.50325379609545, 
92.3076923076923]

y = [0, 
0, 
0, 
0, 
0, 
0, 
0, 
0, 
0, 
0, 
0, 
0, 
0, 
0, 
0, 
2, 
1, 
1, 
2, 
1, 
1, 
2, 
2, 
3, 
4, 
3, 
2, 
2, 
2, 
2, 
2, 
2, 
2, 
5, 
5, 
5, 
3, 
3, 
1, 
2, 
1, 
2, 
2, 
3, 
2, 
0, 
0, 
0, 
4, 
3, 
4, 
4, 
3, 
4, 
4, 
1, 
1, 
1, 
1, 
0, 
0, 
0]


print(np.corrcoef(x, y))

plt.scatter(x, y) 
plt.title('A plot to show the correlation between coffene and sleep efficiency (SE) \n')
plt.xlabel('Sleep Efficiency')
plt.ylabel('Number of caffeine drinks')
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)), color='yellow')
plt.savefig("correlation.png")