import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np

df = pd.read_csv('/Users/daniillickovaha/Documents/learning/SQL/projects/SEA/bd/dataset.csv')

events = {}
disp_c = disp_o = disp_s = 0

for i in range(len(df)):
    participants = df['participants'][i]
    type = df['type'][i]

    if type not in events:
        events[type] = [participants]
    else:
        events[type].append(participants)

    
mid_c = sum(events['Conference'])/len(events['Conference'])
mid_o = sum(events['Olympiad'])/len(events['Olympiad'])
mid_s = sum(events['Seminar'])/len(events['Seminar'])

for value in events['Conference']:
    disp_c += (mid_c - value) ** 2

disp_c /= len(events['Conference'])

for value in events['Olympiad']:
    disp_o += (mid_o - value) ** 2

disp_o /= len(events['Olympiad'])

for value in events['Seminar']:
    disp_s += (mid_s - value) ** 2

disp_s /= len(events['Seminar'])

def normal_distr(mid, disp, name, color):
    plt.figure(figsize = (14, 8)) # creating figure
    sigm = np.sqrt(disp)
    # creating 100 points in range mid - 3*sigm, mid + 3*sigm
    # in this range lies 99.7% of data
    x = np.linspace(mid - 4 * sigm, mid + 4 * sigm, 100) # more points - smoother the line
    plt.plot(x, norm.pdf(x, mid, sigm), color = color, label = name) # x=[1, 2, 3], y=[0.1, 0.4, 0.5], color='red', name='a'
    mx_y = norm.pdf(mid, mid, sigm)
    # norm.pdf() 1st arg - point, array of points for calculating
    # 2nd - math expect, 3d - standart deviation
    # scatter - for draw point
    plt.fill_between(x, norm.pdf(x, mid, sigm), color = color, alpha = 0.2)
    plt.scatter(mid, mx_y, color = 'black', marker = 'o', label = f'mean for {name} = {round(mid)}', zorder = 10) 
    # zorder - position on the z-axis
    plt.plot([mid, mid], [0, mx_y], '--', color = color, alpha = 0.8) # vertical dotted line 
    # ([start_x, end_x], [start_y, end_y])

    # for interval (mean - sigm, mean + sigm)
    plt.plot([mid - sigm, mid - sigm], [0, norm.pdf(mid - sigm, mid, sigm)], '--', color = color, alpha = 0.6)
    plt.plot([mid + sigm, mid + sigm], [0, norm.pdf(mid + sigm, mid, sigm)], '--', color = color, alpha = 0.6)
    # for interval (mean - 2sigm, mean + 2sigm)
    plt.plot([mid - 2*sigm, mid - 2*sigm], [0, norm.pdf(mid - 2*sigm, mid, sigm)], '--', color = color, alpha = 0.45)
    plt.plot([mid + 2*sigm, mid + 2*sigm], [0, norm.pdf(mid + 2*sigm, mid, sigm)], '--', color = color, alpha = 0.45)
    # for interval (mean - 3sigm, mean + 3sigm)
    plt.plot([mid - 3*sigm, mid - 3*sigm], [0, norm.pdf(mid - 3*sigm, mid, sigm)], '--', color = color, alpha = 0.3)
    plt.plot([mid + 3*sigm, mid + 3*sigm], [0, norm.pdf(mid + 3*sigm, mid, sigm)], '--', color = color, alpha = 0.3)


def call_figure(mid, disp, name, color):
    # creating the new graphic window
    normal_distr(mid, disp, name, color)
    plt.xlim(0) # less connot be

    plt.title('distribution of the number of participants by event type')
    plt.xlabel('number of participants')
    plt.ylabel('probability density')
    plt.legend() # post all of the labels in the right places
    plt.grid(True) # turn on grid
    plt.show()

call_figure(mid_c, disp_c, 'Conference', 'red')
call_figure(mid_o, disp_o, 'Olympiad', 'blue')
call_figure(mid_s, disp_s, 'Seminar', 'green')

