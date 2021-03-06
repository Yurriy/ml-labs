import numpy as np
from scipy.misc import toimage, imresize

(im_h, im_w) = (40, 40)

indexes = dict()

def change_labels(data):
    labels_uniques = np.unique(data[:, 1])
    labels_uniques.sort()
    for i in range(labels_uniques.size):
        indexes[labels_uniques[i]] = i
    return np.array([indexes[data[i][1]] for i in range(len(data))])

def invert_colors(im):
    return np.abs(im - 255)

data = np.load('train.npy')
np.random.shuffle(data)
cnt = len(data)
y_full = change_labels(data)

prev_len = 0
x_full = np.zeros((cnt, im_h, im_w))
for i in range(cnt):
    x_full[i] = imresize(data[i][0], size=(im_h, im_w))
    x_full[i] = np.abs(x_full[i] - 255)
    progress = str(i / len(data) * 100)[:4] + '%'
    print('\r' * prev_len, progress, end="")
    prev_len = len(progress)

print("\nFormatting has finished")

x_full = x_full.reshape((cnt, im_h, im_w, 1))
sep = int(cnt * 0.85)
x_train, y_train = x_full[:sep], y_full[:sep]
x_test, y_test = x_full[sep:], y_full[sep:]

np.save('data/x_train', x_train)
np.save('data/y_train', y_train)

np.save('data/x_test', x_test)
np.save('data/y_test', y_test)
