import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc

ncin = nc.Dataset("cloud_top_heights/2007_over-water_water_cloud_anomalies_with_sea_ice_and_heights_and_illuminated.nc", "r")

illuminated_indices = np.where(ncin["illuminated"][:] == 1)
shadowed_indices = np.where(ncin["illuminated"][:] == 0)

#illuminated_ice_conc = []
#shadowed_ice_conc = []

illuminated_ice_conc = ncin["sea_ice_concentration"][illuminated_indices]
shadowed_ice_conc = ncin["sea_ice_concentration"][shadowed_indices]

nan_conc_illum = np.where(np.isnan(illuminated_ice_conc))
illuminated_ice_conc[nan_conc_illum] = -20

nan_conc_shad = np.where(np.isnan(shadowed_ice_conc))
shadowed_ice_conc[nan_conc_shad] = -20

bin_edges = np.arange(-20, 105, 5)

ice = [illuminated_ice_conc, shadowed_ice_conc]
numAnomalies = ncin["sea_ice_concentration"][:].size

labels = ["Illuminated", "Not illuminated"]

# This is achieved by dividing the count by the number of
# observations times the bin width and not dividing by the total number of observations.
plt.figure()
plt.title("Anomalies Over Sea Ice")
p = plt.hist(ice, bins = bin_edges, histtype='bar', stacked=True, label=labels, edgecolor = 'black', weights=[np.ones(len(illuminated_ice_conc)) / numAnomalies * 100, np.ones(len(shadowed_ice_conc)) / numAnomalies * 100])

xlocs, xlabels = plt.xticks()
plt.xticks(xlocs, [xlocs[0], "No Data", *xlocs[2:]])
plt.xlim(-20, 100)
plt.xlabel("Sea Ice Concentration (%)")
plt.ylabel("Anomaly Frequency (%)")
plt.legend(loc="upper left")

plt.savefig("illumination_at_diff_sea_ice_conc.png")
