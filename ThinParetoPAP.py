# -*- coding: utf-8 -*-
"""
Created 6/21/2021

@author: Sarah Jordan

Make parallel axis plots comparing SWAT and DPS reservoir operating policies for thesis.

Updated 9/18/2021 
- rename policies 
- transparency 
"""

# packages
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string


ref = pd.read_csv('ThinRef/thin_reference.ref', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
ref = ref.iloc[::-1]

# read in SWAT and DPS
swat = pd.read_csv('ThinRef/SWAT_step94_thinned.reference', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
dps = pd.read_csv('ThinRef/DPS_step94_thinned.reference', sep=' ', names =  ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'])
swat['source'] = 'SWAT'
dps['source'] = 'DPS'

swat_dps_all = pd.concat([swat, dps])

def PAP(ax, df,ex_df,title, lgd):


    table = df[['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton']]


    # Scale the data to minimum and maximum values 
    scaled = table.copy()
    for column in table.columns:
        if column != 'Source':
            mm = ex_df[column].min()
            mx = ex_df[column].max()
            scaled[column] = (table[column] - mm) / (mx - mm)
    
    # label is the soruce
    labs = df['source']

    # Plot all of the policies 
    d = 0
    s = 0
    for solution,l in zip(scaled.iterrows(),labs):
        if l == 'DPS':
            col = '#ff7f00'
            ls = "solid"
            d += 1 
            lbl = "Release Policy"
        elif l == 'SWAT':
            col = '#377eb8'
            ls = "solid"
            s +=1
            lbl = "Target Storage"
        else:
            col = 'lightgrey'
            ls = "solid"
            s +=1

        ys = solution[1]
        xs = range(len(ys - 1))

        ax.plot(xs, ys, c=col, linewidth = 2, label=lbl if (d == 1) or (s==1) else "", linestyle=ls, zorder =2.5 if (l=='DPS') else 0, alpha=0.3 if (l=='DPS') else 0.5)

    # Format the figure

    ax.annotate('', xy=(-0.14, 0.15), xycoords='axes fraction', xytext=(-0.14, 0.85),
        arrowprops=dict(arrowstyle="->", color='black'))

    ax.set_xticks(np.arange(0,np.shape(table)[1],1))
    ax.set_xlim([0,np.shape(table)[1]-1])
    ax.set_ylim([0,1])

    ax.set_ylabel("Scaled Objective Values")
    # ax.set_xticks([0,1,2,3,4])
    ax.set_xticklabels(["Hydropower", "Environment", "Recession", "Sugar", "Cotton"])

    ax.tick_params(axis='y',which='both',labelleft='off',left='off',right='off')
    ax.tick_params(axis='x',which='both',top='off',bottom='off')

    
    # cbar.ax.set_xticklabels(['10','15','20','25','30'])
    # fig.axes[-1].set_xlabel('Scaled Environmental Flows Objective',fontsize=14)
    
    # make subplot frames invisible
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    # draw in axes
    for i in np.arange(0,np.shape(table)[1],1):
        ax.plot([i,i],[0,1],c='k')

    # ax.set_title("Policy Source", size=18)
    ax.set_title(title)
    if lgd == True:
        ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)

# find sources of combined Pareto Set 
source = []
for index, row in ref.iterrows():
    check_swat = swat.loc[(round(swat['Hydropower'],5) == round(row['Hydropower'],5)) & (round(swat['Environment'],5) == round(row['Environment'],5)) & (round(swat['Recession'],5) == round(row['Recession'], 5)) & (round(swat['Sugar'],5) == round(row['Sugar'],5)) & (round(swat['Cotton'],5) == round(row['Cotton'],5))]
    check_dps = dps.loc[(round(dps['Hydropower'],5) == round(row['Hydropower'],5)) & (round(dps['Environment'],5) == round(row['Environment'],5)) & 
                             (round(dps['Recession'],5) == round(row['Recession'], 5)) &
                             (round(dps['Sugar'],5) == round(row['Sugar'],5)) & (round(dps['Cotton'],5) == round(row['Cotton'],5))]
    if len(check_swat['Hydropower']) > 0:
        val = 'SWAT'
    elif len(check_dps['Hydropower']) > 0:
        val = 'DPS'
    else:
        val = 'Error'
    source.append(val)

ref['source'] = source

# print("SWAT:", len(ref[ref['source'] == 'SWAT']))
# print("DPS:", len(ref[ref['source'] == 'DPS']))

sns.set(style="white")
fig, (ax1, ax2) = plt.subplots(2, 1)
fig.set_size_inches([6.3625, 6.3625])

PAP(ax1, swat_dps_all, swat_dps_all, "", False)
PAP(ax2, ref, swat_dps_all, "", True)

ax_ls = [ax1, ax2]
for n in range(len(ax_ls)):
    ax_ls[n].text(0.01, 0.9, "("+ string.ascii_lowercase[n] + ")", transform=ax_ls[n].transAxes, 
            size=13, weight='bold')


fig.tight_layout()
fig.savefig(os.path.join('./Figures/', "02_HistoricalParallelAxisPlot.svg"))
plt.clf()



# Another Figure:
# pull out best policy from each
Objectives = ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'] 
colors = ['#999999', "forestgreen", "cornflowerblue", "mediumpurple", "orange"]
dps_idx = dps[Objectives].idxmin()
swat_idx = swat[Objectives].idxmin()

# get best rows 
d_best = dps.iloc[dps_idx].reset_index()
s_best = swat.iloc[swat_idx].reset_index()

print(d_best)

d_best['colors'] = colors
s_best['colors'] = colors

d_best['best_obj'] = ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'] 
s_best['best_obj'] = ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'] 


# concatenate
all_best = pd.concat([s_best, d_best])

# set up figure
fig, ax = plt.subplots(1, 1)
fig.set_size_inches([6.3625, 3.3625])

# plot
df = all_best
ex_df = swat_dps_all
title = ""
lgd = False

table = df[['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton']]


# Scale the data to minimum and maximum values 
scaled = table.copy()
for column in table.columns:
    if column != 'Source':
        mm = ex_df[column].min()
        mx = ex_df[column].max()
        scaled[column] = (table[column] - mm) / (mx - mm)

# label is the soruce
labs = df['source']
# pull out colors
cols = df['colors']
# pull ot objs
objs = df['best_obj']

# Plot all of the policies 
d = 0
s = 0
for solution,l,col, o in zip(scaled.iterrows(),labs, cols, objs):
    if l == 'DPS':
        # col = '#ff7f00'
        ls = "solid"
        d += 1 
        lbl = "Release Policy"
    elif l == 'SWAT':
        # col = '#377eb8'
        ls = "dashed"
        s +=1
        lbl = "Target Storage"
    else:
        # col = 'lightgrey'
        ls = "solid"
        s +=1

    ys = solution[1]
    xs = range(len(ys - 1))

    ax.plot(xs, ys, c=col, linewidth = 2, label=o if (d <= 5) or (s==2000) else "", linestyle=ls, zorder =2.5 if (l=='DPS') else 0, alpha=0.8)

# Format the figure

ax.annotate('', xy=(-0.14, 0.15), xycoords='axes fraction', xytext=(-0.14, 0.85),
    arrowprops=dict(arrowstyle="->", color='black'))

ax.set_xticks(np.arange(0,np.shape(table)[1],1))
ax.set_xlim([0,np.shape(table)[1]-1])
ax.set_ylim([0,1])

ax.set_ylabel("Scaled Objective Values")
# ax.set_xticks([0,1,2,3,4])
ax.set_xticklabels(["Hydropower", "Environment", "Recession", "Sugar", "Cotton"])

ax.tick_params(axis='y',which='both',labelleft='off',left='off',right='off')
ax.tick_params(axis='x',which='both',top='off',bottom='off')


# cbar.ax.set_xticklabels(['10','15','20','25','30'])
# fig.axes[-1].set_xlabel('Scaled Environmental Flows Objective',fontsize=14)

# make subplot frames invisible
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)

# draw in axes
for i in np.arange(0,np.shape(table)[1],1):
    ax.plot([i,i],[0,1],c='k')

# ax.set_title("Policy Source", size=18)
ax.set_title(title)
if lgd == True:
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.3), ncol=2)

fig.tight_layout()
fig.savefig(os.path.join('./Figures/', "03_PAP_BestObjs.svg"))





