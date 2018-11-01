'''
Created on Oct 18, 2018

@author: EYA
'''
# ---------- LOAD LIBRARIES ------------  
import os,sys
import netCDF4
from netCDF4 import Dataset
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
from matplotlib.pyplot import axes, axis
try:
    import Tkinter as tk
    from tkFileDialog import askopenfilename # python 2  
except ModuleNotFoundError :
    import tkinter as tk # python3 
    from tkinter.filedialog import askopenfilename # for python 3
#from Tkinter import * # python 2
#  
root = tk.Tk()
root.withdraw()
import time
    
 # ---------- DEFINE PLOT STYLE ------------  

plt.style.use('bmh') # define plot style from the list of available: 
# available (checked):'bmh','fivethirtyeight','ggplot'
# not-available:'default', 'grayscale','seaborn-ticks','classic'
# not-available:'seaborn-bright','default','dark_background','seaborn'
# fte_graph(plt.backgroundcolor = 'red')
SMALL_SIZE  = 8 #define font
MEDIUM_SIZE = 9
BIGGER_SIZE = 9
plt.rc('font',    size= MEDIUM_SIZE)   # controls default text sizes
plt.rc('axes', labelsize=BIGGER_SIZE)   # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)   # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)   # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)   # legend fontsize

# ---------- READ FILEs WITH OBSERVARION DATA ------------  
ask_filename = askopenfilename(
    initialdir= os.getcwd(),
    filetypes =(("xlsx file", "*.xls"),("All Files","*.*")),
                title = "Choose a needed  file.")  
fname = ask_filename # input filename
data_water = pd.read_excel(fname)        
# ---------- END OF READ 

class Param():
    def __init__(self, name = 'navn', p_list = [1,2], p_min = 0, 
                 p_max = 100, p_gs = 1,p_xaxis_up = 0, p_label_up =0, 
                 p_label ='Navn', p_color ='#ffff90',  p_linestyle='-'):
        self.name = name    
        self.p_list = p_list
        self.p_min = p_min
        self.p_max = p_max
        self.p_gs = p_gs
        self.p_xaxis_up = p_xaxis_up
        self.p_label_up = p_label_up
        self.p_label = p_label
        self.p_color = p_color
        self.p_linestyle = p_linestyle
#==========================================================================
#read array of stations numbers
nst = data_water['Nst'].values
# arrays of pressure and variables from the data file
depth = data_water['Depth'].values
# minima and maxima of depth for axes
depth_min = 0.
depth_max = 90. #75.
depth_max = 60 #140
print(nst)
#           NAME       ARRAY            MIN   MAX  GS X-SHIFT LABEL 
o2   = Param('o2',  data_water['O2'],    200,  450,  1,  0,  1.10,
            '$ O_2, \mu  M $','#00aa00','o-')
ph   = Param('ph',  data_water['pH'],    6.8, 8.05,  2,  0,  1.10,
            '$ pH,NBS $','#ff00ff','o-')
alk  = Param('alk',  data_water['Alk'], 2000, 2500,  2, 35,  1.25,
            '$ Alk,\mu  M $','#909090','o-')
po4  = Param('po4',  data_water['PO4'],    0,  2.5,  3,  0,  1.10,
            '$ PO_4,\mu  M $','#0000f0','o-')
si   = Param('si',  data_water['Si'],      0,  30,   3, 35,  1.25,
            '$ Si,\mu  M $','#558855','o-')
no3  = Param('no3',  data_water['NO3'],    0, 12.5,  4,  0,  1.10,
            '$ NO_3,\mu  M $','#f00000','o-')
no2  = Param('no2',  data_water['NO2'],    0, 0.5,   4, 35,  1.25,
            '$ NO_2,\mu  M $','#606000','o-')
nh4  = Param('nh4',  data_water['NH4'],    0, 1.5,   4, 70,  1.40,
            '$ NH_4,\mu  M $','#008080','o-')
pH_spec=Param('pH_spec',data_water['pH_spec'], 6.8, 8.05, 2, 70,  1.40,
            '$ pH,Total $','#0f0f0f','o-')
ch4  = Param('ch4',  data_water['CH4'],    0, 750,   3, 70,  1.40,
            '$ CH_4,\mu  M $','#00f0f0','o-')
#print(temp.name,  temp.p_min, temp.p_max, 
#      temp.p_gs, temp.p_xaxis_up, temp.p_label_up, 
#      temp.p_label, temp.p_color, temp.p_linestyle)
#print(pp.name, pp.val_list)
o2   = Param('o2',  data_water['O2'],    300,  330,  1,  0,  1.10,
            '$ O_2, \mu  M $','#00aa00','o-')
ph   = Param('ph',  data_water['pH'],    7.8, 7.85,  2,  0,  1.10,
            '$ pH,NBS $','#ff00ff','o-')
alk  = Param('alk',  data_water['Alk'], 2000, 2500,  2, 35,  1.25,
            '$ Alk,\mu  M $','#909090','o-')
po4  = Param('po4',  data_water['PO4'],    0.5,  0.8,  3,  0,  1.10,
            '$ PO_4,\mu  M $','#0000f0','o-')
si   = Param('si',  data_water['Si'],     6.2, 6.6,   3, 35,  1.25,
            '$ Si,\mu  M $','#558855','o-')
no3  = Param('no3',  data_water['NO3'],    9, 13,  4,  0,  1.10,
            '$ NO_3,\mu  M $','#f00000','o-')
no2  = Param('no2',  data_water['NO2'],    0, 0.2,   1, 35,  1.25,
            '$ NO_2,\mu  M $','#606000','o-')
nh4  = Param('nh4',  data_water['NH4'],    0, 0.15,   2, 70,  1.40,
            '$ NH_4,\mu  M $','#008080','o-')
ch4  = Param('ch4',  data_water['CH4'],    0, 3050,   0, 70,  1.40,
            '$ CH_4,\mu  M $','#00f0f0','o-')


def gen_lists(nst):
    start_list=[]
    end_list = []
    for i in range(len(nst)): # iterate through the nst array
        if nst[i]!=nst[i-1]:
            start_list.append(i) # appending index of row, where station number changes
            end_list.append(i)
    end_list = end_list[1:]
    end_list.append(len(nst))
    return start_list, end_list

start_list, end_list = gen_lists(nst)
max_st=len(end_list)

# ---------- SUBROUTINES TO PLOT -----------
# ----------  PLOT CURVES -----------
#def plot_par(i_st,ip,var,dep,k_min,k_max,axa,linestyle): #plot  parameter ip vert. distribution

def plot_par(fig,gs,i_st,var,dep,k_min,k_max, #plot  parameter ip vert. distribution
             pamin,pamax,ags,xaxis_up,label_shift,label,pcolor,linestyle):
    axa = fig.add_subplot(gs[ags]) 
    ax =axa.twiny()
    ax.set_ylim(depth_max,depth_min)   #   set axis range    
    depth_ticks = np.arange(depth_min, depth_max, 10) #define ticks min, max and step  
    ax.set_yticks(depth_ticks)           # set y-axis ticks 

    ax.set_xlim(pamin,pamax) # set x-axis ticks   
    par_ticks = np.arange(pamin, pamax,(pamax-pamin)/5.) 
    ax.set_xticks(par_ticks)           # set x-axis ticks 
            
    plt.setp(ax.get_yticklabels(), visible=False)
    plt.setp(ax.get_xticklabels(), visible=False)
    ax.xaxis.set_ticks_position('top')
    ax.spines['top'].set_position(('outward',xaxis_up))   
#            ax.axhline(-label_shift[ip] +0.01,  color='black',linestyle = '-', linewidth = 2)
#            ax.axhline(-x_ax_shift[ip]+0.01,color='black',linestyle='-',linewidth=2)
   #         plot_par(i_st,ip,var,pressure,start_list[i_st],end_list[i_st],ax,'o-')
    ax.plot(var[k_min:k_max], 
        dep[k_min:k_max], linestyle,
        color = pcolor) 
    ax.annotate(label, xy=(0.5,label_shift), ha='center', va='top',
            xycoords='axes fraction', fontsize = 12, color = pcolor)
# ----------  PLOT PARAMETERS-----------

def plot_all_var(title,i_st):    #plot all parameters at station i_st 
    gs = gridspec.GridSpec(1,5)   # define  subplots, (i.e. y=vertical,x=horizontal)
    gs.update(left=0.06, right=0.93,top = 0.7,bottom = 0.01) # in ratios of the screen with (0,0) in the left bottom corner
    fig = plt.figure(figsize=(12,5), dpi=300)
    fig.set_facecolor('white') # specify background color
# read CTD data from file if present
    ctd_data = []
    a_st = nst[start_list[i_st]]
#    plt.savefig(results_dir+title+str(a_st)+'.png', facecolor=fig.get_facecolor(), edgecolor='none')
    
    ctd_file=str(a_st)+'.xlsx'
    print(ctd_file)
    try:
        fin=open(ctd_file,'r') 
        print('OK! I am satisfied. ')
        data_ctd = pd.read_excel(ctd_file)
        
        ctd_d = data_ctd['prDM'].values
        t_ctd  = Param('t_ctd',  data_ctd['t090C'],  -2,    8,  0,  0,  1.10,
                      '$ T,^0C $','#ff0000','-')
        s_ctd  = Param('s_ctd',  data_ctd['sal00'],  10,   35,  0, 35,  1.25,
                      '$ Salt,PSU $','#008000','-')
        cdom  = Param('cdom',  data_ctd['wetCDOM'],   0, 30,   1, 35,  1.25,
                      '$ CDOM,mg/m^3 $','#00c0c0','-')
        turb  = Param('turb',  data_ctd['seaTurbMtr'], 0, 2500,   1, 70,  1.40,
                      '$ Turbidity,FTU $','#9f9f9f','-')
        flu  = Param('flu',  data_ctd['flSP'],    0, 2.5,   0, 70,  1.40,
                    '$ Fluorescence,Seapoint $','#00000f','-')
        
 #       ctd_CDOM = data_ctd['wetCDOM'].values
        plot_par(fig,gs,i_st,t_ctd.p_list,ctd_d,1,len(ctd_d),
                 t_ctd.p_min, t_ctd.p_max, t_ctd.p_gs, t_ctd.p_xaxis_up, 
                 t_ctd.p_label_up,t_ctd.p_label, t_ctd.p_color, t_ctd.p_linestyle)
        plot_par(fig,gs,i_st,s_ctd.p_list,ctd_d,1,len(ctd_d),
                 s_ctd.p_min, s_ctd.p_max, s_ctd.p_gs, s_ctd.p_xaxis_up, 
                 s_ctd.p_label_up,s_ctd.p_label, s_ctd.p_color, s_ctd.p_linestyle)    
        plot_par(fig,gs,i_st,cdom.p_list,ctd_d,1,len(ctd_d),
                 cdom.p_min, cdom.p_max, cdom.p_gs, cdom.p_xaxis_up, 
                 cdom.p_label_up,cdom.p_label, cdom.p_color, cdom.p_linestyle)
        plot_par(fig,gs,i_st,turb.p_list,ctd_d,1,len(ctd_d),
                 turb.p_min, turb.p_max, turb.p_gs, turb.p_xaxis_up, 
                 turb.p_label_up,turb.p_label, turb.p_color, turb.p_linestyle)
        plot_par(fig,gs,i_st,flu.p_list,ctd_d,1,len(ctd_d),
                 flu.p_min, flu.p_max, flu.p_gs, flu.p_xaxis_up, 
                 flu.p_label_up,flu.p_label, flu.p_color, flu.p_linestyle)
            
    except EnvironmentError as err:
        print("ERROR, I am so sorry..", err)      
        temp  = Param('temp', data_water['Temp'],   -2,    8,  0,  0,  1.10,
                      '$ T,^0C $','#ff0000','o-')
        salt = Param('salt',data_water['Salt'],   10,   35,  0, 35,  1.25,
                     '$ Salt,PSU $','#008000','o-')
        plot_par(fig,gs,i_st,temp.p_list,depth,start_list[i_st],end_list[i_st],
                     temp.p_min, temp.p_max, temp.p_gs, temp.p_xaxis_up, 
                     temp.p_label_up,temp.p_label, temp.p_color, temp.p_linestyle) 
        plot_par(fig,gs,i_st,salt.p_list,depth,start_list[i_st],end_list[i_st],
                     salt.p_min, salt.p_max, salt.p_gs, salt.p_xaxis_up, 
                     salt.p_label_up,salt.p_label, salt.p_color, salt.p_linestyle)
#------------------------------------------
    plot_par(fig,gs,i_st,o2.p_list,depth,start_list[i_st],end_list[i_st],
            o2.p_min, o2.p_max, o2.p_gs, o2.p_xaxis_up, 
            o2.p_label_up,o2.p_label, o2.p_color, o2.p_linestyle)
    plot_par(fig,gs,i_st,ph.p_list,depth,start_list[i_st],end_list[i_st],
            ph.p_min, ph.p_max, ph.p_gs, ph.p_xaxis_up, 
            ph.p_label_up,ph.p_label, ph.p_color, ph.p_linestyle)
#    plot_par(fig,gs,i_st,alk.p_list,depth,start_list[i_st],end_list[i_st],
#            alk.p_min, alk.p_max, alk.p_gs, alk.p_xaxis_up, 
#            alk.p_label_up,alk.p_label, alk.p_color, alk.p_linestyle)
    plot_par(fig,gs,i_st,po4.p_list,depth,start_list[i_st],end_list[i_st],
            po4.p_min, po4.p_max, po4.p_gs, po4.p_xaxis_up, 
            po4.p_label_up,po4.p_label, po4.p_color, po4.p_linestyle)
    plot_par(fig,gs,i_st,si.p_list,depth,start_list[i_st],end_list[i_st],
            si.p_min, si.p_max, si.p_gs, si.p_xaxis_up, 
            si.p_label_up,si.p_label, si.p_color, si.p_linestyle)
    plot_par(fig,gs,i_st,no3.p_list,depth,start_list[i_st],end_list[i_st],
            no3.p_min, no3.p_max, no3.p_gs, no3.p_xaxis_up, 
            no3.p_label_up,no3.p_label, no3.p_color, no3.p_linestyle)
    plot_par(fig,gs,i_st,no2.p_list,depth,start_list[i_st],end_list[i_st],
            no2.p_min, no2.p_max, no2.p_gs, no2.p_xaxis_up, 
            no2.p_label_up,no2.p_label, no2.p_color, no2.p_linestyle)
    plot_par(fig,gs,i_st,nh4.p_list,depth,start_list[i_st],end_list[i_st],
            nh4.p_min, nh4.p_max, nh4.p_gs, nh4.p_xaxis_up, 
            nh4.p_label_up,nh4.p_label, nh4.p_color, nh4.p_linestyle)#
#    plot_par(fig,gs,i_st,pH_spec.p_list,depth,start_list[i_st],end_list[i_st],
#            pH_spec.p_min, pH_spec.p_max, pH_spec.p_gs, pH_spec.p_xaxis_up, 
#            pH_spec.p_label_up,pH_spec.p_label, pH_spec.p_color, pH_spec.p_linestyle)
    plot_par(fig,gs,i_st,ch4.p_list,depth,start_list[i_st],end_list[i_st],
            ch4.p_min, ch4.p_max, ch4.p_gs, ch4.p_xaxis_up, 
            ch4.p_label_up,ch4.p_label, ch4.p_color, ch4.p_linestyle)
            
# save file with figure
    script_dir = os.path.dirname(__file__)    #retrieve current directory
    results_dir = os.path.join(script_dir, 'Verta/') #make subfolder for figure(s)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)    
    a_st = nst[start_list[i_st]]
    plt.savefig(results_dir+title+str(a_st)+'.png', facecolor=fig.get_facecolor(), edgecolor='none')
#    plt.show()   # print to screen   

    print('Station ',a_st,' plotted.' )
    plt.clf()
    
    
# -------------  PLOT STATIONS ------------
for i_st in range(0,max_st):   # plot stations one by one
    plot_all_var('St_',i_st)          
