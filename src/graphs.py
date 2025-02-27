"""
Labour mismatch data visualisation functions.

Functions:
----------

format_float(fmt, val)
    Convert a float to a string with a specified format.
    last updated: 03/02/2025

shares_heatmap(piaac_df, measures_list, measures_labels, group_var, sort_by, title, y_labels, x_labels, colorbar, numbers, nan_present, size, vertical, filename, display, save)
    Plot a heatmap of the mismatch shares.
    last updated: 03/02/2025

corr_heat_map(piaac_df, corr_type, measures_list, measures_labels, country, title, x_labels, y_labels, size, filename, display, save)
    Plot a heatmap of the correlation matrix.
    last updated: 03/02/2025
"""

import numpy as np
import matplotlib.pyplot as plt

from mismatch_toolbox.src import utilities
from mpl_toolkits.axes_grid1 import make_axes_locatable

def format_float(fmt, val):
  
  """
  Convert a float to a string with a specified format.

  Parameters:
  ----------
    fmt : str
        A format string.
    val : float
        A float to be formatted.

    Returns:
    -------
    str
        A formatted string.

    Example:
    --------
    >>> format_float("%.2f", 3.14159)
    "3.14"
    >>> format_float("%.2f", -3.14159)
    "-3.14"
  """

  ret = fmt % val
  if ret.startswith("0."):
    return ret[1:]
  if ret.startswith("-0."):
    return "-" + ret[2:]
  return ret

def shares_heatmap(piaac_df, 
                   measures_list, 
                   measures_labels, 
                   group_var, 
                   sort_by, 
                   title, 
                   y_labels, 
                   x_labels, 
                   colorbar = True, 
                   numbers = True, 
                   nan_present = True, 
                   size = (5, 15), 
                   vertical = True, 
                   filename = 'shares_heatmap', 
                   display = True, 
                   save = True):

    """
    Plot a heatmap of the mismatch shares.

    Parameters:
    ----------
    piaac_df : DataFrame
        A DataFrame containing the PIAAC data.
    measures_list : list
        A list of the mismatch measures variable names.
    measures_labels : list
        A list of the labels for the mismatch measures.
    group_var : str
        A variable name identifying the group level.
    sort_by : str
        A variable name used to sort the mismatch shares
    title : str
        A title of the heatmap.
    y_labels : bool
        A boolean indicating whether to display y-axis labels.
    x_labels : bool
        A boolean indicating whether to display x-axis labels.
    colorbar : bool
        A boolean indicating whether to display a colorbar. Default is True.
    numbers : bool
        A boolean indicating whether to display numbers in the heatmap. Default is True.
    nan_present : bool
        A boolean indicating whether NaN values are present in the data. Default is True.
    size : tuple
        A size of the heatmap. Default is (5, 15).
    vertical : bool
        A boolean indicating whether to plot the heatmap vertically. Default is True.
    filename : str
        A filename to save the heatmap. Default is 'shares_heatmap'.
    display : bool
        A boolean indicating whether to display the plot. Default is True.
    save : bool
        A boolean indicating whether to save the plot. Default is True.

    Returns:
    -------
    plt
        A plot of the heatmap.
    """

    # close all open graphs
    plt.close('all')

    # define the x-axis by the labels of specified measures
    x = measures_labels

    # define the y-axis by the median of specified sort_by for specified group_var level
    y = piaac_df[[group_var, sort_by]].groupby(by=[group_var]).median().round(decimals=2).sort_values(sort_by, ascending=False).reset_index(level=0).to_numpy().tolist()
    y_new = []
    for i in y:
        y_new += [i[0]]
    y = y_new

    heatmap_data = np.empty((len(piaac_df[group_var].value_counts()), 1))
    for measure in measures_list:
        heatmap_data = np.append(heatmap_data, np.delete(np.array(
            piaac_df[[group_var, sort_by, measure]].groupby(by=[group_var]).median().sort_values(sort_by, ascending=False)),
                                                         0, 1), axis=1)
    heatmap_data = np.delete(heatmap_data, 0, 1)
    heatmap_data = np.around(heatmap_data, decimals=2)
    
    if vertical == False:
        heatmap_data = heatmap_data.T
        x_old = x
        y_old = y
        x = y_old
        y = x_old
    
    fig = plt.figure(figsize=size)
    ax = fig.subplots()
    
    if nan_present == True:
        unique_values = np.unique(heatmap_data).tolist()
        unique_values.sort()
        min_value = unique_values[1]
        im = ax.imshow(heatmap_data, cmap='Greys', vmin=min_value)
    else:
        im = ax.imshow(heatmap_data, cmap='Greys')

    # colour schemes can be found at
    # https://matplotlib.org/stable/tutorials/colors/colormaps.html

    if colorbar == True:
        # Create colorbar
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("left", size="5%", pad=0.1)
        cbar = fig.colorbar(im, cax=cax)
        cbar.ax.yaxis.set_label_position('left')
        cbar.ax.yaxis.tick_left()
        cbar.ax.tick_params(axis='y', labelsize=14, labelrotation=0)
        cbar.ax.set_ylabel("Share", fontsize=18, rotation=90)
    else:
        pass

    # Show all ticks and label them with the respective list entries
    if x_labels == True:
        ax.set_xticks(np.arange(len(x)), labels=x)
    else:
        ax.set_xticks(np.arange(len(x)), labels=[])
    
    if y_labels == True:
        ax.set_ylabel('Countries by median earnings (descending)', fontsize=18, rotation=90)
        ax.yaxis.set_label_position("right")
        ax.yaxis.tick_right()
        ax.set_yticks(np.arange(len(y)), labels=y)
    else:
        ax.set_yticks(np.arange(len(y)), labels=[])

    ax.tick_params(axis='y', labelsize=14)
    ax.tick_params(axis='x', labelsize=18)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)
    ax.set_xticks(np.arange(heatmap_data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(heatmap_data.shape[0] + 1) - .5, minor=True)
    #ax.grid(which="minor", color="w", linestyle='-')
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.yaxis.tick_right()

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right", va="center", rotation_mode="anchor")
    #plt.setp(ax.get_yticklabels(), rotation=0, ha="left", va="center", rotation_mode="anchor")

    threshold = im.norm(heatmap_data.max()) / 2.
    textcolors = ("black", "white")

    # Loop over data dimensions and create text annotations.
    if numbers == True:
        for i in range(len(y)):
            for j in range(len(x)):
                text = ax.text(j, i, format_float("%.2f", heatmap_data[i, j]), ha="center", va="center",
                               color=textcolors[int(im.norm(heatmap_data[i, j]) > threshold)],
                               fontsize=14, rotation=0)

    ax.set_title(title, fontsize=22, rotation='horizontal', ha='center')
    fig.tight_layout()
    
    if save == True:
        plt.savefig(filename + '.pdf', bbox_inches="tight")
    
    if display == True:
        plt.show()

    return plt
    


def corr_heat_map(piaac_df, 
                  corr_type, 
                  measures_list, 
                  measures_labels, 
                  country, 
                  title, 
                  x_labels, 
                  y_labels, 
                  size = (5, 5), 
                  filename = 'corr_heatmap', 
                  display = True, 
                  save = True):

    """
    Plot a heatmap of the correlation matrix.

    Parameters:
    ----------
    piaac_df : DataFrame
        A DataFrame containing the PIAAC data.
    corr_type : str
        A type of correlation coefficient: 'matthews' or 'pearson'.
    measures_list : list
        A list of the mismatch measures variable names.
    measures_labels : list
        A list of the labels for the mismatch measures.
    country : str
        A country name or 'all'.
    title : str
        A title of the heatmap.
    x_labels : bool
        A boolean indicating whether to display x-axis labels.
    y_labels : bool
        A boolean indicating whether to display y-axis labels.
    size : tuple
        A size of the heatmap. Default is (5, 5).
    filename : str
        A filename to save the heatmap. Default is 'corr_heatmap'.
    display : bool
        A boolean indicating whether to display the plot. Default is True.
    save : bool
        A boolean indicating whether to save the plot. Default is True.

    Returns:
    -------
    plt
        A plot of the heatmap.
    """

    plt.close('all')

    fontsize = max(size) * 2

    x = measures_labels
    y = measures_labels
    
    if (country == 'all') & (corr_type == 'matthews'):
        heatmap_data = np.array(utilities.mcc_matrix(piaac_df, measures_list).round(2))
        bar_label = "Matthews correlation coefficient"
        
    elif (country != 'all') & (corr_type == 'matthews'):
        heatmap_data = np.array(utilities.mcc_matrix(piaac_df.loc[piaac_df['cntryname'] == country], measures_list).round(2))
        bar_label = "Matthews correlation coefficient"
        
    elif (country == 'all') & (corr_type == 'pearson'):
        heatmap_data = np.array(piaac_df[measures_list].corr().round(2))
        bar_label = "Pearson correlation coefficient"
        
    elif (country != 'all') & (corr_type == 'pearson'):
        heatmap_data = np.array(piaac_df.loc[piaac_df['cntryname'] == country, measures_list].corr().round(2))
        bar_label = "Pearson correlation coefficient"

    
    fig = plt.figure(figsize=size)
    ax = fig.subplots()
    im = ax.imshow(heatmap_data, cmap='Greys')
    
    # Create colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    cbar = fig.colorbar(im, cax=cax)
    cbar.ax.tick_params(axis='y', labelsize=fontsize, labelrotation = 0)
    cbar.ax.set_ylabel(bar_label, fontsize=fontsize, rotation=90)
    
    # Show all ticks and label them with the respective list entries
    if x_labels == True:
        ax.set_xticks(np.arange(len(x)), labels=x)
    else:
        ax.set_xticks(np.arange(len(x)), labels=[])
    if y_labels == True:
        ax.set_yticks(np.arange(len(y)), labels=y)
    else:
        ax.set_yticks(np.arange(len(y)), labels=[])
        
    ax.tick_params(axis='y', labelsize=fontsize)
    ax.tick_params(axis='x', labelsize=fontsize)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)
    ax.set_xticks(np.arange(heatmap_data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(heatmap_data.shape[0] + 1) - .5, minor=True)
    #ax.grid(which="minor", color="w", linestyle='-')
    ax.tick_params(which="minor", bottom=False, left=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right", va="center", rotation_mode="anchor")

    threshold = im.norm(heatmap_data.max()) / 2.
    textcolors = ("black", "white")

    # Loop over data dimensions and create text annotations.
    for i in range(len(y)):
        for j in range(len(x)):
            text = ax.text(j, i, format_float("%.2f", heatmap_data[i, j]), ha="center", va="center",
                           color=textcolors[int(im.norm(heatmap_data[i, j]) > threshold)],
                           fontsize=fontsize, rotation=0)

    ax.set_title(title, fontsize=fontsize*1.5, rotation='horizontal', ha='center')
    fig.tight_layout()
    
    if save == True:
        plt.savefig(filename + '.pdf')
    
    if display == True:
        plt.show()

    return plt