# encoding: utf-8
from numpy import *
from matplotlib.pyplot import *
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import integrate

def mquiver(xs,ys,v,**kw):
    """wrapper function for quiver
    xs and ys are arrays of x's and y's
    v is a function R^2 -> R^2, representing vector field
    kw are passed to quiver verbatim"""
    X,Y=meshgrid(xs,ys)
    V=[[v(x,y) for x in xs] for y in ys]
    VX=[[w[0] for w in q] for q in V]
    VY=[[w[1] for w in q] for q in V]
    quiver(X,Y,VX,VY,**kw)

def dirfield(xs,ys,f,**kw):
    """
    wrapper function of mquiver that plots the direction field
    xs and ys are arrays of x's and y's
    f is a function R^2->R
    kw are passed to quiver verbatim
    """
    xs, ys = list(xs), list(ys) #in case something wrong was given
    mquiver(xs,ys,lambda x,y: (1,f(x,y)),scale=90,headwidth=0.0, 
                   headlength=0.0, 
                   headaxislength=0.0,pivot='middle',angles='xy',**kw)
def mplot(xs,f,**kw):
    """wrapper function for plot,
    xs is an array of x's
    f is a function R^1 -> R^1
    the rest of arguments are passed to plot"""
    plot(xs,map(f,xs),**kw)

def axes4x4(labels=("t","x")):
    """Функция устанавливает размер картинки в [-4,4]×[-4,4] и подписывает оси
    
    args
    ====
    - labels — метки осей (абсцисса, ордината)
    """
    axis([-4,4,-4,4])
    center_spines()
    text(3.8,0.2,"$%s$" % labels[0],fontsize=20)
    text(0.1,3.7,"$%s$"% labels[1],fontsize=20)

def normdirfield(xs,ys,f,**kw):
    """
    plot normalized direction field
    
    kwargs
    ======
    
    - length is a desired length of the lines (default: 1)
    - the rest of kwards are passed to plot
    
    uses a trick with None delimeters in plot from 
    http://exnumerus.blogspot.ru/2011/02/how-to-quickly-plot-multiple-line.html
    """
    length= kw.pop('length') if 'length' in kw else 1
    xlist=[]
    ylist=[]
    for x in xs:
        for y in ys:
            vy=f(x,y)
            prelen=sqrt(1+vy**2)
            deltax=1/prelen*length
            deltay=vy/prelen*length
            xlist.extend([x-deltax/2,x+deltax/2,None])
            ylist.extend([(-deltax/2)*vy+y,(deltax/2)*vy+y,None])
    plot(xlist,ylist,**kw)

#center_spines and CenteredFormatter are adapted from
#http://stackoverflow.com/questions/4694478/center-origin-in-matplotlib/4718438#4718438
#by Joe Kington
#licensed under CC BY-SA

def center_spines(ax=None, centerx=0, centery=0):
    """Centers the axis spines at <centerx, centery> on the axis "ax", and
    places arrows at the end of the axis spines."""
    if ax is None:
        ax = gca()

    # Set the axis's spines to be centered at the given point
    # (Setting all 4 spines so that the tick marks go in both directions)
    ax.spines['left'].set_position(('data', centerx))
    ax.spines['bottom'].set_position(('data', centery))
    ax.spines['right'].set_position(('data', centerx))
    ax.spines['top'].set_position(('data', centery))

    # Hide the line (but not ticks) for "extra" spines
    for side in ['right', 'top']:
        ax.spines[side].set_color('none')

    # On both the x and y axes...
    for axis, center in zip([ax.xaxis, ax.yaxis], [centerx, centery]):
        # Turn on minor and major gridlines and ticks
        axis.set_ticks_position('both')
        axis.grid(True, 'major', ls='solid', lw=0.5, color='gray')
        axis.grid(True, 'minor', ls='solid', lw=0.1, color='gray')
        axis.set_minor_locator(mpl.ticker.AutoMinorLocator())

        # Hide the ticklabels at <centerx, centery>
        formatter = CenteredFormatter()
        formatter.center = center
        axis.set_major_formatter(formatter)

    # Add offset ticklabels at <centerx, centery> using annotation
    # (Should probably make these update when the plot is redrawn...)
    xlabel, ylabel = map(formatter.format_data, [centerx, centery])
    ax.annotate('(%s, %s)' % (xlabel, ylabel), (centerx, centery),
            xytext=(-4, -4), textcoords='offset points',
            ha='right', va='top')
 
class CenteredFormatter(mpl.ticker.ScalarFormatter):
    """Acts exactly like the default Scalar Formatter, but yields an empty
    label for ticks at "center"."""
    center = 0
    def __call__(self, value, pos=None):
        if value == self.center:
            return ''
        else:
            return mpl.ticker.ScalarFormatter.__call__(self, value, pos)
def axes4x4(labels=("t","x")):
    """Функция устанавливает размер картинки в [-4,4]×[-4,4] и подписывает оси

    args
    ====

    labels: обозначения осей.
    """
    axis([-4,4,-4,4])
    center_spines()
    text(3.8,0.2,"$%s$" % labels[0],fontsize=20)
    text(0.1,3.7,"$%s$" % labels[1],fontsize=20)

def eulersplot(f, xa, xb, ya, n = 500, **kw):
    """plots numerical solution y'=f

    args
    ====

    - xa: initial value of independent variable
    - xb: final value of independent variable
    - ya: initial value of dependent variable
    - n : number of steps (higher the better)
    """
    h = (xb - xa) / float(n)
    x = [xa] 
    y = [ya]
    for i in range(1,n+1):
        y.append(y[-1] + h * f(x[-1], y[-1]))
        x.append(x[-1] + h)
    plot(x,y, **kw)

def normvectorfield(xs,ys,fs,**kw):
    """
    plot normalized vector field
    
    kwargs
    ======
    
    - length is a desired length of the lines (default: 1)
    - the rest of kwards are passed to plot
    """
    length= kw.pop('length') if 'length' in kw else 1
    x, y=meshgrid(xs, ys)
    # calculate vector field
    vx,vy=fs(x,y)
    # plot vecor field
    norm = length /sqrt(vx**2+vy**2)
    quiver(x, y, vx * norm, vy * norm, angles='xy',**kw)

def vectorfield(xs,ys,fs,**kw):
    """
    plot vector field (no normalization!)

    args
    ====
    fs is a function that returns tuple (vx,vy)
    
    kwargs
    ======
    
    - length is a desired length of the lines (default: 1)
    - the rest of kwards are passed to plot
    """
    length= kw.pop('length') if 'length' in kw else 1
    x, y=meshgrid(xs, ys)
    # calculate vector field
    vx,vy=fs(x,y)
    # plot vecor field
    norm = length 
    quiver(x, y, vx * norm, vy * norm, angles='xy',**kw)

def plottrajectories(fs,x0,t=linspace(1,400,10000),**kw):
    """
    plots trajectory of the solution
    
    f  -- must accept an array of X and t=0, and return a 2D array of \dot y and \dot x
    x0 -- vector
    
    Example
    =======

    plottrajectories(lambda X,t=0:array([ X[0] -   X[0]*X[1] ,
                   -X[1] + X[0]*X[1] ]), [ 5,5], color='red')
    """
    x0 = array(x0)
    #f = lambda X,t=0: array(fs(X[0],X[1]))
    #fa = lambda X,t=0:array(fs(X[0],X[1]))
    X = integrate.odeint( fs, x0, t)
    plot( X[:,0], X[:,1], **kw )

def phaseportrait(fs,inits,t=[-5,5],n=100,**kw):
    """
    plots phase portrait of the differential equation (\dot x,\dot y)=fs(x,y)

    f  -- must accept an array of X and t=0, and return a 2D array of \dot y and \dot x
    inits -- list of vectors representing inital conditions
    t -- time interval
    n -- number of points

    Example
    =======
    
    from itertools import product
    phaseportrait(lambda X, t=0: array([X[0],2*X[1]]), product(linspace(-4,4,15),linspace(-4,4,15)), [-2,0.3], n=20)
    """
    assert(t[0]<t[1] and t[1]>0)
    X=[]
    Y=[]
    for x0 in inits:
        x0=array(x0)
        if t[0]<0:
            segments=[linspace(0,t[0],n),linspace(0,t[1],n)]
        else:
            segments=[linspace(t[0],t[1],2*n)]
        for s in segments:
            points=integrate.odeint(fs,x0,s)
            for i,Z in enumerate([X,Y]):
                Z.extend(points[:,i])
                Z.append(None)
        diriv = fs(x0)
        arrow(x0[0]-diriv[0],x0[1]-diriv[1],diriv[0],diriv[1], 
              head_width=0.2, lw=0.0)
    plot(X,Y,**kw)

def mcontour(xs,ys, fs, levels=None,**kw):
    """
    wrapper function for contour

    example
    ======
    mcontour(linspace(-4,4),linspace(-4,4),lambda x,y: x*y)
    """
    x,y=meshgrid(xs,ys)
    z=fs(x,y)
    if levels!=None:
        contour(x,y,z,levels,**kw)
    else:
        contour(x,y,z,**kw)
