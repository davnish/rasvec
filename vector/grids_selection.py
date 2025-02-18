import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import shapely
import os

class grid_selection:
    def __init__(self):
        """
        This class is to get grids over state or district
        This class will simultaneously plot and save the grids.
        """
        self.grids = gpd.read_file("grid_india\\grid_7km_wcrs.shp")
    
    def plot_save_grid_over_state(self, state_name):
        """
        Input:
            The input of the function is the state name you want to plot and save grids over.
        
        output:
            The ouput of this function is the saved grids as a geopandas file as "ESRI Shapefile" in "grid_india" dir
            Total
        """
        self.states = gpd.read_file(os.path.join("Administrative Boundary Database", "STATE_BOUNDARY.shp")).to_crs(epsg = 4326)
        _, ax = plt.subplots(figsize=(10,10))
        state = self.states[self.states['STATE'] == state_name]
        self.states.plot(ax = ax)
        state.plot(ax = ax, color = 'red')
        self.grids.plot(ax = ax, edgecolor='black', facecolor = 'none')
        state_grids = self.grids[self.grids.intersects(state['geometry'].all())]
        state_grids.plot(ax = ax, edgecolor='yellow', facecolor = 'none')
        saving_path = os.path.join(f"grid_india\\state\\{state_name}")
        if os.path.exists(os.path.join("grid_india", "state", state_name)) == False:
            os.mkdir(saving_path)
        state_grids.to_file(os.path.join(saving_path, f'{state_name}_grids.shp'), driver='ESRI Shapefile')
        print(f'Total grids in {state_name}: {len(state_grids)}')
        plt.show()
    
    def plot_save_grid_over_district(self, district_name):
        self.states = gpd.read_file(os.path.join("Administrative Boundary Database", "DISTRICT_BOUNDARY.shp")).to_crs(epsg = 4326)
        _,  ax = plt.subplots(figsize=(10,10))
        state = self.states[self.states['District'] == district_name]
        self.states.plot(ax = ax)
        state.plot(ax = ax, color = 'red')
        self.grids.plot(ax = ax, edgecolor='black', facecolor = 'none')
        state_grids = self.grids[self.grids.intersects(state['geometry'].all())]
        state_grids.plot(ax = ax, edgecolor='yellow', facecolor = 'none')
        saving_path = os.path.join(f"grid_india\\district\\{district_name}")
        if os.path.exists(os.path.join("grid_india", "district", district_name)) == False:
            os.mkdir(saving_path)
        state_grids.to_file(os.path.join(saving_path, f'{district_name.replace('>', 'A')}_grids.shp'), driver='ESRI Shapefile')
        print(f'Total grids in {district_name}: {len(state_grids)}')
        plt.show()





if __name__ == '__main__':
    
    vis = grid_selection()
    vis.plot_save_grid_over_district('BULANDSHAHR')