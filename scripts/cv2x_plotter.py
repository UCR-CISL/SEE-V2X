import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
rc('font',family='Times New Roman')

# For Interactive Plotting
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import Range1d

matlab_blue = "#0072BD"
matlab_red = "#D95319"
matlab_yellow="#EDB120"
matlab_purple="#7E2F8E"
matlab_green="#77AC30"
color_map={0:matlab_blue,1:matlab_red,
           5:matlab_yellow,
           6:matlab_blue,7:matlab_red,
           11:matlab_green}

THROUGHPUT_COLOR_MAP={
    't1':'b',
    't2':'g',
    't3':'b',
    'rsu':'darkorange'
}

LOSS_COLOR_MAP={
    't1':'r--',
    't2':'m--',
    't3':'r--',
    'rsu':'c--'
}



def drawLineChart4ThroughputNLoss(throughput:dict,
                                  loss:dict,
                                  showPeak=False,
                                  title='Throughput and Loss Rate'):
    fig, ax = plt.subplots()
    ## line throughput
    font = {'family': 'Times New Roman',
        'color':  'black',
        'weight': 'bold',
        'size': 25,
        }
    
    lns_throughput =[]
    lns_loss =[]
    for whichTx, dictY in throughput.items():
        x = list(dictY.keys())
        y_throughput = list(dictY.values())
        if showPeak:
            peak_throughput = max(y_throughput)
            peak_idx = y_throughput.index(peak_throughput)
            sct1 = ax.scatter(x[peak_idx],
                      peak_throughput,
                      color='k',s=100,zorder=9999)
            ax.annotate('%.3f Mbps'%peak_throughput,
                        (x[peak_idx],peak_throughput),
                        (x[peak_idx]+200,peak_throughput-0.05),
                        fontsize=25,zorder=9999,weight='bold')
        lns1=ax.plot(x,y_throughput,
                    THROUGHPUT_COLOR_MAP[whichTx],
                    marker='o',
                    label='Throughput '+whichTx)
        lns_throughput+=lns1
        ax.set_xlabel('Packet Size (bytes)',fontdict=font)
        ax.set_ylabel('Throughput (Mbps)',fontdict=font)
        ax.tick_params(axis = 'both', labelsize = 20)
        
        ## line loss
        axX=ax.twinx()
        y_loss = list(loss[whichTx].values())
        lns2=axX.plot(x,y_loss,
                    LOSS_COLOR_MAP[whichTx],
                    marker='s',
                    label='Packet Loss Rate '+whichTx)
        axX.set_ylabel('Packet Loss Rate (%) ',fontdict=font)
        axX.set_ylim(0,100)
        axX.tick_params(axis = 'both', labelsize = 20)
        
        lns_loss+=lns2
    ax.set_title(title, fontdict=font)
    labs = [l.get_label() for l in lns_throughput+lns_loss]
    ax.legend(lns_throughput+lns_loss, labs, loc='upper left',fontsize=12)
        
def drawThroughputNLossByTimer(throughput:dict,
                               loss:dict,
                               title='Throughput and Loss Rate'):
    fig, ax = plt.subplots(figsize=(12, 3))
    ## line throughput
    font = {'family': 'Times New Roman',
        'color':  'black',
        'weight': 'bold',
        'size': 25,
        }
    
    lns_throughput =[]
    lns_loss =[]
    for whichTx, dictY in throughput.items():
        x = list(dictY.keys())
        y_throughput = list(dictY.values())
        lns1=ax.plot(x,y_throughput,
                    THROUGHPUT_COLOR_MAP[whichTx],
                    label='Throughput '+whichTx)
        lns_throughput+=lns1
        ax.set_xlabel('Time (ms)',fontdict=font)
        ax.set_ylabel('Throughput (Mbps)',fontdict=font)
        ax.tick_params(axis = 'both', labelsize = 20)
        
        ## line loss
        axX=ax.twinx()
        y_loss = list(loss[whichTx].values())
        lns2=axX.plot(x,y_loss,
                    LOSS_COLOR_MAP[whichTx],

                    label='Packet Loss Rate '+whichTx)
        axX.set_ylabel('Packet Loss Rate (%) ',fontdict=font)
        axX.tick_params(axis = 'both', labelsize = 20)
        print("throughput max",max(y_throughput))
        print("throughput mean",sum(y_throughput)/len(y_throughput))
        print("loss max",max(y_loss))
        print("loss mean",sum(y_loss)/len(y_loss))
        lns_loss+=lns2
    ax.set_title(title, fontdict=font)
    labs = [l.get_label() for l in lns_throughput+lns_loss]
    ax.legend(lns_throughput+lns_loss, labs, loc='upper left',fontsize=12)
    
def drawLineChart4Latency(latency:dict,
                          title='Latency'):
    fig, ax = plt.subplots()
    ## line latency
    font = {'family': 'Times New Roman',
        'color':  'black',
        'weight': 'bold',
        'size': 25,
        }
    
    lns_latency =[]
    for prio, dictY in latency.items():
        color = (np.random.random(),np.random.random(),np.random.random())
        for whichTx, dictY in dictY.items():
            x = list(dictY.keys())
            y_latency = list(dictY.values())
            lns1=ax.plot(x,y_latency,
                        color=color,
                        marker='o',
                        label='Latency '+whichTx+' '+str(prio))
            lns_latency+=lns1
            ax.set_xlabel('Packet Size (bytes)',fontdict=font)
            ax.set_ylabel('Latency (ms)',fontdict=font)
            ax.tick_params(axis = 'both', labelsize = 20)
    ax.set_title(title, fontdict=font)
    labs = [l.get_label() for l in lns_latency]
    ax.legend(lns_latency, labs, loc='upper left',fontsize=12)
        
def drawLatencyByTime(latency:dict,
                      title='Latency'):
    fig, ax = plt.subplots()
    ## line latency
    font = {'family': 'Times New Roman',
        'color':  'black',
        'weight': 'bold',
        'size': 25,
        }
    
    lns_latency =[]
    for whichTx, dictY in latency.items():
        color = (np.random.random(),np.random.random(),np.random.random())
        x = list(dictY.keys())
        y_latency = list(dictY.values())
        lns1=ax.plot(x,y_latency,
                    color=color,
                    label='Latency '+whichTx)
        lns_latency+=lns1
        ax.set_xlabel('Time (ms)',fontdict=font)
        ax.set_ylabel('Latency (ms)',fontdict=font)
        ax.tick_params(axis = 'both', labelsize = 20)
    ax.set_title(title, fontdict=font)
    labs = [l.get_label() for l in lns_latency]
    ax.legend(lns_latency, labs, loc='upper left',fontsize=12)
    
def drawChannelOccupy(rb_dict:dict,
                      x_range=1000):
        output_notebook()
        p = figure(width=1000, height=300)
        p.x_range = Range1d(0, x_range)
        p.y_range=Range1d(0,100)
        for mcs,rb in rb_dict.items():
            sf_list,sf_right_list,rb_start_list,rb_end_list= rb[0],rb[1],rb[2],rb[3]
            p.quad(top=rb_end_list, bottom=rb_start_list, left=sf_list,
                right=sf_right_list, color=color_map[mcs])
        
        p.xaxis.axis_label = "Time (ms)"
        p.xaxis.axis_label_text_font = 'Times New Roman'
        p.xaxis.major_label_text_font = "Times New Roman"
        p.xaxis.major_label_text_font_size = "20pt"
        p.xaxis.axis_label_text_font_size='25pt'
        p.xaxis.axis_label_text_font_style = 'bold'

        
        p.yaxis.axis_label = "Sub-channels"
        p.yaxis.axis_label_text_font = 'Times New Roman'
        p.yaxis.major_label_text_font = "Times New Roman"
        p.yaxis.major_label_text_font_size = "20pt"
        p.yaxis.axis_label_text_font_size='25pt'
        p.yaxis.axis_label_text_font_style = 'bold'
        show(p)   