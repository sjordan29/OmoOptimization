import pyswat as ps 
import pandas as pd
import os
import geopandas as gpd
import matplotlib.pyplot as plt 
import contextily as ctx
import numpy as np 
from matplotlib import cm
from matplotlib.colors import ListedColormap,LinearSegmentedColormap

hsv_modified = cm.get_cmap('Blues', 256)# create new hsv colormaps in range of 0.3 (green) to 0.7 (blue)
newcmp = ListedColormap(hsv_modified(np.linspace(0.5, 1.0, 256)))



fpath = "/scratch/smj5vup/omoScenarios/BestPolicyEachObj/DPS/"
Objectives = ['Hydropower', 'Environment', 'Recession', 'Sugar', 'Cotton'] 
folders = ['TxtInOut_0', 'TxtInOut_1', 'TxtInOut_2','TxtInOut_3','TxtInOut_4']

omo = gpd.read_file('shapefile/subs1.shp')
omo.to_crs(epsg=3857, inplace=True)

riv = gpd.read_file('shapefile/riv1.shp')
riv.to_crs(epsg=3857, inplace=True)

puc = '/scratch/smj5vup/omoScenarios/Historical/Uncontrolled/TxtInOut_00/SWATfiles/'

model_puc = ps.connect(puc)

puc_df = model_puc.expressResults(startDate="1989-01-01", 
                              endDate="2018-12-31", 
                              id_no=[f for f in range(1,28)], 
                              variable='SWmm', 
                              julian=True, 
                              fetch_tables='sub', 
                              freq='d')



# for j in range(1, 28):
#     v = puc_df[0][j]
#     v = v[(v.index.month == 11) | (v.index.month == 12) | (v.index.month == 1) | (v.index.month == 2)]
#     v_avg = v['SWmm'].mean()
#     ls.append(v_avg)


# omo['puc'] = ls 


for i in range(len(Objectives)):
    print(Objectives[i])
    if Objectives[i] in ['Sugar', 'Cotton']:

        # connect to SWAT model 
        model = ps.connect(r"%s%s/SWATfiles" % (fpath, folders[i]))

        sub_df = model.expressResults(startDate="1989-01-01", 
                                      endDate="2018-12-31", 
                                      id_no=[f for f in range(1,28)], 
                                      variable='SWmm', 
                                      julian=True, 
                                      fetch_tables='sub', 
                                      freq='d')
        rch_df = model.expressResults(startDate="1989-01-01", 
                                      endDate="2018-12-31", 
                                      id_no=[f for f in range(1,28)], 
                                      variable='FLOW_OUTcms', 
                                      julian=True, 
                                      fetch_tables='rch', 
                                      freq='d')


        # ls = []

        # for j in range(1, 28):
        #     v = sub_df[0][j]
        #     v = v[(v.index.month == 11) | (v.index.month == 12) | (v.index.month == 1) | (v.index.month == 2)]
        #     v_avg = v['SWmm'].mean()
        #     ls.append(v_avg)

        
        # omo[Objectives[i]] = ls
        # omo[Objectives[i] + '_diff'] = omo[Objectives[i]] - omo['puc']
        # print(omo[Objectives[i] + '_diff'].min(), omo[Objectives[i] + '_diff'].max())

        # fig, ax = plt.subplots(1,1)

        # o = omo.plot(column=Objectives[i] + "_diff",
        #     ax=ax,
        #     cmap = "RdBu",
        #     vmin = -13,
        #     vmax = 13, 
        #     legend=True,
        #     edgecolor="k")
        
        # ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=7)


        # fig.set_size_inches(12, 6)
        # ax.set_title(Objectives[i])

        # plt.savefig('/scratch/smj5vup/omoScenarios/BestPolicyEachObjCC/MakeFigures/Figures/Spatial/%s.png' % Objectives[i])

        for mo in range(1,13):
            print("Month: %s" % str(mo))
            ls = []
            flw = []
            huc = []

            for j in range(1, 28):
                v = sub_df[0][j]
                v = v[v.index.month == mo]
                v_avg = v['SWmm'].mean()
                ls.append(v_avg)

                f = rch_df[0][j]
                f = f[f.index.month == mo]
                f_avg = f['FLOW_OUTcms'].mean()
                flw.append(f_avg)

                u = puc_df[0][j]
                u = u[u.index.month == mo]
                u_avg = u['SWmm'].mean()
                huc.append(u_avg)
            
            omo[Objectives[i] + "_%s" % str(mo)] = ls
            riv[Objectives[i] + "_%s" % str(mo)] = flw
            omo['puc_%s' % str(mo)] = huc

            omo[Objectives[i] + '_diff_%s' % str(mo) ] = omo[Objectives[i] + "_%s" % str(mo)] - omo['puc_%s' % str(mo)]
            # print(omo[Objectives[i] + '_diff_%s' % str(mo)].min(), omo[Objectives[i] + '_diff_%s' % str(mo)].max())

            fig, ax = plt.subplots(1,1)

            print(omo.head())
            print(riv.head())

            o = omo.plot(column=Objectives[i] + "_diff_%s" % str(mo),
                ax=ax,
                cmap = "RdBu",
                vmin = -20,
                vmax = 20, 
                legend=True,
                edgecolor="k")

            # r = riv.plot(column = Objectives[i] + "_%s" % str(mo), 
            #     ax = ax,
            #     cmap = newcmp, 
            #     vmin = 0,
            #     vmax = 3000)
            
            ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, zoom=7)


            fig.set_size_inches(12, 6)
            ax.set_title("month = %s" % mo)

            if len(str(mo)) < 2:
                str_mo = "0" + str(mo)
            else:
                str_mo = str(mo)

            plt.savefig('/scratch/smj5vup/omoScenarios/BestPolicyEachObjCC/MakeFigures/Figures/Spatial/%s/%s_month.png' % (Objectives[i], str_mo))
            plt.clf()





