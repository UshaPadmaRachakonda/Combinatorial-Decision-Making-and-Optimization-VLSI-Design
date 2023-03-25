import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from pathlib import Path




def read_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        assert len(lines) > 2 
        lines = [line.strip() for line in lines]
        line = lines[0].split()
        n = int(lines[1])
        bbox = []
        for i in range(n):
            bbox.append([int(x) for x in lines[i+2].split()])
        return (line, bbox)


def get_color(n):
    return plt.cm.get_cmap('hsv', n)
def plot(data, save = None):
    line, bboxs = data
    w, l = int(line[0]), int(line[1])
    # rainbow colors
    colors = get_color(len(bboxs))

    fig, ax = plt.subplots(facecolor='w', edgecolor='k')
    # bounding boxes
    for i, bbox in enumerate(bboxs):
        if len(bbox) == 4:
            x, y, x1, y1 = bbox
        else:
            x, y, x1, y1, r = bbox
            if int(r) == 1:
                x, y, x1, y1 = y, x, x1, y1
        rectangle = Rectangle((x1, y1), x, y, fill=True, color=colors(i), alpha=0.4)
        ax.add_patch(rectangle)
    plt.xlim(0, w)
    plt.ylim(0, l)
    plt.xticks(np.arange(w+1))
    plt.yticks(np.arange(l+1))
    # plt.grid(color='black', linestyle='--')
    if save:
        plt.savefig(save, dpi=300, bbox_inches='tight')

    plt.show()
    

