import pandas as pd
import matplotlib.pyplot as plt # creating graphs
from scipy.stats import norm # normal distribution
from scipy.integrate import simpson # for square
import statsmodels.api as sm # for qq plot
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

def NormalDistr(mid, disp, name, color):
    plt.figure(figsize = (14, 8)) # creating figure
    sigm = np.sqrt(disp)
    # creating 100 points in range mid - 3*sigm, mid + 3*sigm
    # in this range lies 99.7% of data
    x = np.linspace(mid - 4 * sigm, mid + 4 * sigm, 100) # more points give precision
    plt.plot(x, norm.pdf(x, mid, sigm), color = color, label = name) # x=[1, 2, 3], y=[0.1, 0.4, 0.5], color='red', name='a'
    mx_y = norm.pdf(mid, mid, sigm) # probability density function
    # norm.pdf() 1st arg - point, array of points for calculating
    # 2nd - math expect, 3d - standart deviation

    # scatter - for draw point
    plt.scatter(mid, mx_y, color = 'black', marker = 'o', label = f'mean for {name} = {round(mid)}, \n(sigma = {round(sigm)})', zorder = 10) 
    # zorder - position on the z-axis
    # plt.plot([mid, mid], [0, mx_y], '--', color = color, alpha = 0.6) # vertical dotted line 
    # ([start_x, end_x], [start_y, end_y])

    # for interval (mean - sigm, mean + sigm)
    plt.plot([mid - sigm, mid - sigm], [0, norm.pdf(mid - sigm, mid, sigm)], '--', color = 'black', alpha = 0.4)
    plt.plot([mid + sigm, mid + sigm], [0, norm.pdf(mid + sigm, mid, sigm)], '--', color = 'black', alpha = 0.4)
    # for interval (mean - 2sigm, mean + 2sigm)
    plt.plot([mid - 2*sigm, mid - 2*sigm], [0, norm.pdf(mid - 2*sigm, mid, sigm)], '--', color = 'black', alpha = 0.35)
    plt.plot([mid + 2*sigm, mid + 2*sigm], [0, norm.pdf(mid + 2*sigm, mid, sigm)], '--', color = 'black', alpha = 0.35)
    # for interval (mean - 3sigm, mean + 3sigm)
    plt.plot([mid - 3*sigm, mid - 3*sigm], [0, norm.pdf(mid - 3*sigm, mid, sigm)], '--', color = 'black', alpha = 0.3)
    plt.plot([mid + 3*sigm, mid + 3*sigm], [0, norm.pdf(mid + 3*sigm, mid, sigm)], '--', color = 'black', alpha = 0.3)

    # the area under the prob density graph = 1
    # simpson able to calculate the square under the graph
    x1 = np.linspace(mid - sigm, mid + sigm, 100)
    y1 = norm.pdf(x1, mid, sigm)
    area1 = round(simpson(y=y1, x=x1), 2)
    plt.fill_between(x1, y1, color = color, alpha = 0.2, label = f'square = {area1}')

    x2 = np.linspace(mid - 2*sigm, mid + 2*sigm, 100)
    y2 = norm.pdf(x2, mid, sigm)
    area2 = round(round(simpson(y=y2, x=x2) - area1, 2), 2)
    plt.fill_between(x2, y2, color = color, alpha = 0.15, label = f'square = {area2}')

    x3 = np.linspace(mid - 3*sigm, mid + 3*sigm, 100)
    y3 = norm.pdf(x3, mid, sigm)
    area3 = round(round(simpson(y=y3, x=x3)) - area2 - area1, 2)
    plt.fill_between(x3, y3, color = color, alpha = 0.1, label = f'square = {area3}')
    
def CallFigure(mid, disp, name, color):
    # creating the new graphic window
    NormalDistr(mid, disp, name, color)
    plt.xlim(0) # less connot be

    plt.title('distribution of the number of participants by event type')
    plt.xlabel('number of participants')
    plt.ylabel('probability density')

    plt.legend() # post all of the labels in the right places

    plt.grid(True) # turn on grid
    # set text on graph, bbox - white window for text
    # plt.show()
    plt.savefig(f'outputs/{name}_normal.png', dpi = 324)
    # close for auto-creating new figure and avoid memory leakss
    plt.close()

def QQPlot(name, lst, dist, mean, sigma):
    # numpy array is +- c-array with static_type data
    # need for sm.qqplot
    data = np.array(lst)
    sm.qqplot(data, dist = dist, loc = mean, scale = sigma, line = '45') # 45 is normal line
    # the x-axis is theoretical quantiles
    # the y-axis is real quantiles
    # quantile is number, which show, 
    # that p-part of data in the left side of this number
    # qq plot comparing the quantiles from 2 set, perfect is equal
    plt.title(f'Q-Q plot for {name}')
    plt.savefig(f'outputs/{name}_qqplot.png', dpi = 324)
    plt.close()

# calling normal distribution (theoretical) figure
CallFigure(mid_c, disp_c, 'Conference', 'red')
CallFigure(mid_o, disp_o, 'Olympiad', 'blue')
CallFigure(mid_s, disp_s, 'Seminar', 'green')

# calling Q-Q plots for each events (comparing theoretical with real data)
QQPlot('Conference', events['Conference'], norm, mid_c, round(np.sqrt(disp_c)))
QQPlot('Olympiad', events['Olympiad'], norm, mid_o, round(np.sqrt(disp_o)))
QQPlot('Seminar', events['Seminar'], norm, mid_s, round(np.sqrt(disp_s)))