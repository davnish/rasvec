import geopandas as gpd
import matplotlib.pyplot as plt

def view(plot_list : list) -> None:
    """Plots the given list of plots."""
    
    fig, ax = plt.subplots(figsize=(10,10))
    for plot in plot_list:
        plot.plot(ax=ax)
    plt.show()
    return