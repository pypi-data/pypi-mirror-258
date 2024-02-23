from matplotlib import pyplot as plt
def fgmk(n,x,y,xlabel,ylabel, titlestr, figtext = None, glabel = None, grid = None):
    plt.figure(n)
    plt.plot(x,y, label = glabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if(grid == True):
        plt.grid(which='both')
    plt.title(titlestr)
    plt.text(0.5, -0.18, r'$\bf{Figure\ }$' + str(n) + r': '+ str(figtext), transform=plt.gca().transAxes,
            horizontalalignment='center', verticalalignment='center', fontsize=10)
    plt.legend()