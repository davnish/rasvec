import geopandas as gpd
import matplotlib.pyplot as plt

def view(plot_list : list) -> None:
    """Plots the given list of plots."""
    
    fig, ax = plt.subplots(1, len(plot_list), figsize=(10,10))
    for idx, plot in enumerate(plot_list):
        plot.plot(ax=ax[idx])
        ax[idx].axis('off')
    plt.tight_layout()
    plt.show()
    return