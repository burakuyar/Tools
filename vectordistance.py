import numpy as np

x = np.array([0.01160998, 0.66176873, 1.33514738, 1.6602267, 2.33360553, 2.9953742])
y = np.array([0.01160997711122036, 0.65015858970582485, 1.3119275029748678, 1.6370067056268454, 2.240725701674819, 2.8676645215600729])

#x = np.array([1, 4, 8, 16])
#y = np.array([1, 4, 8, 16])


def adaptive_scaler(x, y):

    distances = list()
    distancesums = list()
    mindistance = 100
    ratio = 0.5
    rate = 0.01

    for i in range(0, 301):

        scaled_y = ratio * (y - y[0]) + y[0]
        print("Scaler:", i, "Scaled Y:", scaled_y)
        distances.append(x - scaled_y)
        distancesums.append(sum(abs(distances[-1])))
        ratio += rate

    mindistance = min(distancesums)
    index_of_mindistance = distancesums.index(mindistance)
    closest_scaled_y = distances[index_of_mindistance]
    ratio = 0.5 + (index_of_mindistance * rate)
    print(mindistance, index_of_mindistance, ratio)
    print("Min difference:", closest_scaled_y)

    y = ratio * (y - y[0]) + y[0]
    print("Final Y:", y)

adaptive_scaler(x, y)

