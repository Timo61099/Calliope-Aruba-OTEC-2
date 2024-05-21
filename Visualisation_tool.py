#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:35:36 2024

@author: timoscheepmaker
"""

import calliope
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
 
results = calliope.read_netcdf("Aruba_test.nc")
all_capacity = results.get_formatted_array("energy_cap").to_pandas().T  # get_formatted_array().to_pandas() is your bread and butter when analysing the .nc files
 
# --- Generation Capacity --- #
# here, you basically filter out all non-generation technologies
generation_capacity = all_capacity[(all_capacity.index.str.contains('demand_power')==False) &
                                   (all_capacity.index.str.contains("pumped_hydro")==False)]

 
# --- Generation --- #
 # here we get the generation
generation = results.get_formatted_array('carrier_prod').loc[{'carriers':'power'}].sum('locs').to_pandas()
generation_total_per_tech = results.get_formatted_array('carrier_prod').loc[{'carriers':'power'}].sum('locs').sum("timesteps").to_pandas()
generation_total = results.get_formatted_array('carrier_prod').loc[{'carriers':'power'}].sum('locs').sum("timesteps").sum("techs").to_pandas()

energy_generation = results.get_formatted_array('carrier_prod')
total_energy_supplied = energy_generation.sum().to_pandas()
total_energy_generation_per_tech = energy_generation.loc[{'carriers':'power'}].sum('timesteps').to_pandas().T

 # again, filter out all non-generation technologies
generation = generation [(generation.index.str.contains('demand_power')==False) &
                           (generation.index.str.contains('transmission')==False)].T
 # Define generation sources
generation_sources = ['battery', 'offshore_wind', 'onshore_wind', 'otec', 'solar', 'solar_floating']

#--- Consumption /Demand ---#
consumption = results.get_formatted_array('carrier_con').loc[{'carriers':'power'}].sum('locs').to_pandas()
demand = consumption[(consumption.index.str.contains('battery')==False)].T

#--- Battery Size (MWh)---#
battery_size_MWh = generation_capacity.loc['battery']/0.25

# --- Costs --- #
# here we get the costs of each tech
costs = results.get_formatted_array('cost').loc[{'costs': 'monetary'}].to_pandas().T
total_costs = results.get_formatted_array('cost').sum().to_pandas()
total_costs2 = results.get_formatted_array('cost').loc[{'costs': 'monetary'}].sum().to_pandas().T
total_costs3 = results.get_formatted_array('cost')

# --- LCOE ---#
# here we get the lcoe of each tech
lcoe = results.results.systemwide_levelised_cost.loc[{'carriers': 'power', 'costs':'monetary'}].to_pandas().T
lcos = total_costs/total_energy_supplied

#again, filter out all technologies that aren't used
lcoe = lcoe [(lcoe.index.str.contains('ac_transmission')==False) &
             (lcoe.index.str.contains('biomass')==False) &
             (lcoe.index.str.contains('cc_gas')==False) &
             (lcoe.index.str.contains('coal')==False) &
             (lcoe.index.str.contains('demand_power')==False) &
             (lcoe.index.str.contains('filler_gen')==False) &
             (lcoe.index.str.contains('geothermal')==False) &
             (lcoe.index.str.contains('hvdc_transmission')==False) &
             (lcoe.index.str.contains('large_hydro')==False) &
             (lcoe.index.str.contains('nuclear')==False) &
             (lcoe.index.str.contains('oc_gas')==False) &
             (lcoe.index.str.contains('pumped_hydro')==False) &
             (lcoe.index.str.contains('small_hydro')==False) &
             (lcoe.index.str.contains('diesel')==False)].T

#%%----------------------------------------------------------
# ------ # Plotting # ------- #

#%% --- Generation Capacities ---#

generation_capacity.plot(kind='bar', figsize=(10, 6), legend=False)
plt.bar_label(plt.gca().containers[0])
plt.title('Generation Capacities by Technology')
plt.xlabel('Technology')
plt.ylabel('Capacity (MW)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#%% --- Generated Electricity per Technology (Annual) --- #

# total_energy_generation_per_tech.plot(kind='bar', figsize=(10,6), legend=False)
# plt.bar_label(plt.gca().containers[0])
# plt.title('Total Electricity Generated per Technology (Annual)')
# plt.xlabel('Technology')
# plt.ylabel('Electricity (MWh)')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

#%% --- Generation --- #

# plt.figure(figsize=(10, 7))
# lines = []
# for source in generation_sources:
#     line, = plt.plot(generation.index, generation[source], linestyle='-', markersize=2, label=source)
#     lines.append(line)

# plt.title('Generation Data by Source')
# plt.xlabel('Time')
# plt.ylabel('Generation (units)')
# plt.xticks(rotation=45)
# plt.legend()
# plt.grid(True)
# plt.tight_layout()

# plt.show()

# # Stacked plot generation
# plt.figure(figsize=(10, 7))

#    # Convert the generation DataFrame to a NumPy array
# generation_values = generation[generation_sources].values.T

#    # Plot the stacked area plot
# plt.stackplot(generation.index, generation_values, labels=generation_sources, baseline='zero', alpha=0.7)
# plt.title('Generation Data by Source (Stacked)')
# plt.xlabel('Time')
# plt.ylabel('Generation (units)')
# plt.xticks(rotation=45)
# plt.legend(loc='upper left')
# plt.grid(True)
# plt.tight_layout()

# plt.show()

#%% --- Demand --- #

# plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
# demand.plot(linewidth=0.05)
# plt.title('Demand Profile')
# plt.xlabel('Time')
# plt.ylabel('Demand (MW)')  # Replace 'units' with the appropriate unit for your demand data
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# plt.show()

#%% --- Costs ---#

# costs.plot(kind='bar', figsize=(10, 6), legend=False)
# plt.bar_label(plt.gca().containers[0])
# plt.title('Costs by Technology')
# plt.xlabel('Technology')
# plt.ylabel('Costs (USD)')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

#%% --- LCOE ---#

# lcoe.plot(kind='bar', figsize=(10, 6))
# plt.bar_label(plt.gca().containers[0])
# plt.title('LCOE per technology')
# plt.xlabel('Technology')
# plt.ylabel('Costs (USD/MWh)')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

#%% --- Battery and Demand --- #


# Plotting the consumption data


# Plot the generation data
# plt.figure(figsize=(10, 6))
# plt.plot(generation.index, generation.values, linestyle='-', label='Generation')
# plt.title('Generation Data')
# plt.xlabel('Time')
# plt.ylabel('Generation (units)')
# plt.xticks(rotation=45)
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # Create checkboxes for each technology
# rax = plt.axes([0.85, 0.4, 0.1, 0.3])
# labels = [source.capitalize() for source in generation_sources]
# visibility = [line.get_visible() for line in lines]
# check = CheckButtons(rax, labels, visibility)


# def toggle_visibility(label):
#     index = labels.index(label)
#     lines[index].set_visible(not lines[index].get_visible())
#     plt.draw()


# check.on_clicked(toggle_visibility)
