'''
Consolidate Code from:
/scratch/omoScenarios/BestPolicyEachObjCC/PythonScripts/05_CombineObjs_PAP.ipynb
'''

# packages
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from utils import * 
import string

# filepaths
fpath_dps = '../Objectives/DPS'
fpath_swat = '../Objectives/SWAT'
fpath_uc = '../Objectives/Uncontrolled'

# get mid/late-century objective values
df = pd.read_csv(os.path.join(fpath_dps,os.listdir(fpath_dps)[0]), names = ['Mid', 'Late'])

# define objectives 
Objectives = ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'] 

# filepaths
fpath_mc = '../PythonScripts/Data/Objectives/MidCentury'
fpath_lc = '../PythonScripts/Data/Objectives/LateCentury'


# initialize and populate dictionaries 
DPS_MC = dict.fromkeys(Objectives)
DPS_LC = dict.fromkeys(Objectives)
SWAT_MC = dict.fromkeys(Objectives)
SWAT_LC = dict.fromkeys(Objectives)
UC_MC = dict.fromkeys(Objectives)
UC_LC = dict.fromkeys(Objectives)

for obj in Objectives:
    DPS_MC[obj] = pd.read_csv(os.path.join(fpath_mc, '%s_DPS.csv' % obj), index_col = 'Unnamed: 0')
    DPS_LC[obj] = pd.read_csv(os.path.join(fpath_lc, '%s_DPS.csv' % obj), index_col = 'Unnamed: 0')
    
    SWAT_MC[obj] = pd.read_csv(os.path.join(fpath_mc, '%s_SWAT.csv' % obj), index_col = 'Unnamed: 0')
    SWAT_LC[obj] = pd.read_csv(os.path.join(fpath_lc, '%s_SWAT.csv' % obj), index_col = 'Unnamed: 0')
            
    UC_MC[obj] = pd.read_csv(os.path.join(fpath_mc, '%s_UC.csv' % obj),index_col = 'Unnamed: 0')
    UC_LC[obj] = pd.read_csv(os.path.join(fpath_lc, '%s_UC.csv' % obj),index_col = 'Unnamed: 0')

### SORT PROJECTIONS - DRY-->WET and LO-->HI TEMP
# determine uncontrolled flows for each objective and sort 
projections = UC_MC['Hydropower'].index 
fpath_ts = '../Timeseries/Uncontrolled'

UC_ts = dict.fromkeys(projections)
for proj in projections:
    UC_ts[proj] = pd.read_csv(os.path.join(fpath_ts, '%s_UC_Flow.csv' % proj), index_col = 'Unnamed: 0')

# mean flow of uncontrolled 
UC_mean = dict.fromkeys(projections)
for proj in projections:
    UC_mean[proj] = UC_ts[proj]['flow'].mean()

# sort projections 
sorted_projs = printDict(UC_mean)

# sort by temp 
temp = pd.read_csv('../PythonScripts/Data/ClimateDeltas.csv')
temp = temp.sort_values(by=['tasmax_2040_2069_ann'])

sorted_temp_projs = temp['model'].tolist()
sorted_temp_projs = [f[:-7].replace("_", ".") for f in  sorted_temp_projs]
sorted_temp_projs = [f for f in sorted_temp_projs if f in projections]


import itertools
O2 = list(itertools.chain.from_iterable(itertools.repeat(x, 2) for x in Objectives))

######## Read Data
# comined pareto set
DPS_MC_combined = dict.fromkeys(Objectives)
DPS_LC_combined = dict.fromkeys(Objectives)
SWAT_MC_combined = dict.fromkeys(Objectives)
SWAT_LC_combined = dict.fromkeys(Objectives)   

# indices of robust policices
dps_pols = [0, 1, 2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28,
            29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 43, 44, 48, 49, 50, 51, 54, 55, 56, 57, 59, 60, 62, 66, 67,
            69, 70, 71, 73, 74, 75,76, 77, 81, 82, 83, 84, 85, 86, 87, 89, 90, 94, 95, 97]

swat_pols = [0, 1,  2,  3,  4,  5,  7, 8,  9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 35, 40, 41, 44, 48]

dps_cols = []
swat_cols = []
for item in dps_pols:
    if len(str(item)) == 1:
        val = "P0" + str(item)
    else:
        val = "P" + str(item)
        
    dps_cols.append(val)
    
for item in swat_pols:
    if len(str(item)) == 1:
        val = "P0" + str(item)
    else:
        val = "P" + str(item)
        
    swat_cols.append(val)


# sorted 
UC_MC_sorted = dict.fromkeys(Objectives)
UC_LC_sorted = dict.fromkeys(Objectives)


for obj in Objectives:
    DPS_MC_combined[obj] = DPS_MC[obj][dps_cols]
    DPS_LC_combined[obj] = DPS_LC[obj][dps_cols]
    
    SWAT_MC_combined[obj] = SWAT_MC[obj][swat_cols]
    SWAT_LC_combined[obj] = SWAT_LC[obj][swat_cols]    


for obj in Objectives:
    if obj in ["Sugar", "Cotton"]:
        DPS_MC_combined[obj] = DPS_MC_combined[obj].reindex(sorted_temp_projs)
        DPS_LC_combined[obj] =  DPS_LC_combined[obj].reindex(sorted_temp_projs)
        SWAT_MC_combined[obj] = SWAT_MC_combined[obj].reindex(sorted_temp_projs)
        SWAT_LC_combined[obj] = SWAT_LC_combined[obj].reindex(sorted_temp_projs)
        UC_MC_sorted[obj] = UC_MC[obj].reindex(sorted_temp_projs)
        UC_LC_sorted[obj] = UC_LC[obj].reindex(sorted_temp_projs)        
    else:
        DPS_MC_combined[obj] = DPS_MC_combined[obj].reindex(sorted_projs)
        DPS_LC_combined[obj] =  DPS_LC_combined[obj].reindex(sorted_projs)
        SWAT_MC_combined[obj] = SWAT_MC_combined[obj].reindex(sorted_projs)
        SWAT_LC_combined[obj] = SWAT_LC_combined[obj].reindex(sorted_projs)
        UC_MC_sorted[obj] = UC_MC[obj].reindex(sorted_projs)
        UC_LC_sorted[obj] = UC_LC[obj].reindex(sorted_projs) 


# find policies that meet robustness metric
# outperform uncontrolled in all projections and all 
dps_mc_pols = FindCommonElements(DPS_MC_combined, UC_MC_sorted,Objectives)
dps_lc_pols = FindCommonElements(DPS_LC_combined, UC_LC_sorted,Objectives)
swat_mc_pols = FindCommonElements(SWAT_MC_combined, UC_MC_sorted,Objectives)
swat_lc_pols = FindCommonElements(SWAT_LC_combined, UC_LC_sorted,Objectives)



# plot 
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style("white")
fig, axes = plt.subplots(5,2)
for n, ax in zip(range(len(axes.flatten())), axes.flatten()):
    if n %2 == 0:
        PAP_ltd(ax, DPS_MC_combined, SWAT_MC_combined, UC_MC_sorted, O2[n], dps_lc_pols, swat_lc_pols, DPS_LC_combined, SWAT_LC_combined, UC_LC)
    else:
        PAP_ltd(ax, DPS_LC_combined, SWAT_LC_combined, UC_LC_sorted, O2[n], dps_lc_pols, swat_lc_pols, DPS_MC_combined, SWAT_MC_combined, UC_MC)
        ax.set_yticklabels("")
    ax.annotate('', xy=(0, -0.06), xycoords='axes fraction', xytext=(1, -0.06),
            arrowprops=dict(arrowstyle="<-", color='black'))
#     ax.annotate('', xy=(-0.06, 0), xycoords='axes fraction', xytext=(-0.06, 1),
#             arrowprops=dict(arrowstyle="<-", color='black'))
    
for ax,i in zip(axes.flatten(), range(10)):
    ax.set_ylim(0,1.05)
    ax.set_xticklabels("")
    if i > 5:
        ax.set_xlabel("Increasing Temperature")
    else:
        ax.set_xlabel("Increasing Flows")
    if i % 2 == 0:
        ax.annotate('', xy=(-0.14, -0.1), xycoords='axes fraction', xytext=(-0.14, 1),
        arrowprops=dict(arrowstyle="->", color='black'))
    
    ax.text(0.008, 1.02, "("+ string.ascii_lowercase[i] + ")", transform=ax.transAxes, 
size=13, weight='bold')       
    
    
    # make subplot frames invisible
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
        # draw in axes
    for i in np.arange(0,48,1):
        if i in [0, 47]:
            ax.plot([i,i], [0,1], color='black')

# plt.savefig('../Figures/ClimateChangePAP_DPSfront_LateCentury_CombinedSet.png')
# for ax in axes.flatten()[3:6]:
#     ax.set_xlabel("Climate Projection", fontsize=16)
axes.flatten()[4].set_ylabel("Scaled Objective Value", fontsize=18,labelpad=10)
# fig.text(0.55, -0.02, 'Climate Projection', ha='center', fontsize=18)
fig.text(0.33, 1.0, 'Mid-Century', ha='center', fontsize=18)
fig.text(0.77, 1.0, 'Late Century', ha='center', fontsize=18)


fig.set_size_inches([8.3625, 11.3625])
fig.tight_layout()
ax.legend(loc="lower center", bbox_to_anchor=(0, -0.55), ncol=3, fontsize=12)
fig.savefig('Figures/06_PAP_ClimateChange.svg', bbox_inches='tight')
plt.clf()