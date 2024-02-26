import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pandas.plotting import parallel_coordinates
import numpy as np

class vissuAlize:
    @staticmethod
    def bar(x, y, title="Title", xlabel="X-axis", ylabel="Y-axis",
            figsize=(8, 6), color='maroon', orientation='vertical', **kwargs):
        """
        Draws a bar chart for the given data.

        Parameters:
        - x: The values for the x-axis (category names or numbers).
        - y: The values for the y-axis.
        - title: The title of the chart.
        - xlabel: The label for the x-axis.
        - ylabel: The label for the y-axis.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - color: The color of the bars.
        - orientation: The orientation of the bars, either 'vertical' or 'horizontal'.
        - **kwargs: Additional keyword arguments to be passed to the matplotlib bar function.
        """
        plt.figure(figsize=figsize)
        if orientation == 'vertical':
            plt.bar(x, y, color=color, **kwargs)
        else:
            plt.barh(x, y, color=color, **kwargs)

        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def plot(x, y, title="Title", xAxisLabel="X-axis", yAxisLabel="Y-axis",
             figsize=(8, 6), color='maroon', width=0.4, kind="line", **kwargs):
        """
        Draws a plot based on the specified kind. Supports 'line' and 'bar' plot types.

        Parameters:
        - x: The x values.
        - y: The y values.
        - title: The title of the plot.
        - xAxisLabel: Label for the X-axis.
        - yAxisLabel: Label for the Y-axis.
        - figsize: Tuple indicating figure size, (width, height) in inches.
        - color: Color of the plot elements.
        - width: The width of the bars (applicable only for bar plots).
        - kind: Type of plot to draw ('line' or 'bar').
        - **kwargs: Additional keyword arguments to pass to the underlying plot function.
        """
        if kind == "line":
            plt.figure(figsize=figsize)
            plt.plot(x, y, color=color, **kwargs)
            plt.title(title)
            plt.xlabel(xAxisLabel)
            plt.ylabel(yAxisLabel)
            plt.show()
        elif kind == "bar":
            plt.figure(figsize=figsize)
            plt.bar(x, y, color=color, width=width, **kwargs)
            plt.title(title)
            plt.xlabel(xAxisLabel)
            plt.ylabel(yAxisLabel)
            plt.show()

    @staticmethod
    def scatter(x, y, title="Title", xlabel="X-axis", ylabel="Y-axis",
                figsize=(8, 6), color='blue', marker='o', **kwargs):
        """
        Draws a scatter plot for the given x and y coordinates.

        Parameters:
        - x, y: The x and y coordinates of the data points.
        - title: The title of the plot.
        - xlabel, ylabel: Labels for the X-axis and Y-axis respectively.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - color: The color of the data points.
        - marker: The shape of the marker used for each data point.
        - **kwargs: Additional keyword arguments to be passed to the matplotlib scatter function.
        """
        plt.figure(figsize=figsize)
        plt.scatter(x, y, color=color, marker=marker, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def histogram(data, bins=10, title="Title", xlabel="Value", ylabel="Frequency",
                  figsize=(8, 6), color='green', **kwargs):
        """
        Draws a histogram for the given data.

        Parameters:
        - data: The data for which the histogram will be created.
        - bins: The number of bins (or buckets) to use for the histogram.
        - title: The title of the plot.
        - xlabel, ylabel: Labels for the X-axis and Y-axis respectively.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - color: The color of the histogram bars.
        - **kwargs: Additional keyword arguments to be passed to the matplotlib hist function.
        """
        plt.figure(figsize=figsize)
        plt.hist(data, bins=bins, color=color, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def boxplot(data, title="Title", xlabel="Categories", ylabel="Values",
                figsize=(8, 6), color="skyblue", **kwargs):
        """
        Draws a boxplot for the given data.

        Parameters:
        - data: The data for the boxplot. Can be a Pandas DataFrame, a list of lists, or similar.
        - title: The title of the plot.
        - xlabel, ylabel: Labels for the X-axis and Y-axis respectively.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - color: The color of the box (if using seaborn, this parameter can be added to seaborn style parameters).
        - **kwargs: Additional keyword arguments to be passed to either the matplotlib or seaborn boxplot function.
        """
        plt.figure(figsize=figsize)
        if isinstance(data, list):
            plt.boxplot(data, patch_artist=True, boxprops=dict(facecolor=color), **kwargs)
        elif isinstance(data, pd.DataFrame):
            sns.boxplot(data=data, color=color, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def heatmap(data, title="Title", figsize=(10, 8), cmap="viridis", annot=False, **kwargs):
        """
        Draws a heatmap for the given data matrix.

        Parameters:
        - data: The data matrix for the heatmap. Should be a Pandas DataFrame where each cell represents a value.
        - title: The title of the plot.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - cmap: The colormap to be used.
        - annot: If True, the values will be written in each cell.
        - **kwargs: Additional keyword arguments to be passed to the seaborn heatmap function.
        """
        plt.figure(figsize=figsize)
        sns.heatmap(data, cmap=cmap, annot=annot, **kwargs)
        plt.title(title)
        plt.show()

    @staticmethod
    def lineplot(x, y, title="Title", xlabel="X-axis", ylabel="Y-axis",
                 figsize=(10, 6), color='blue', linestyle='-', linewidth=2, **kwargs):
        """
        Draws a line plot for the given x and y coordinates.

        Parameters:
        - x, y: The x and y coordinates of the data points.
        - title: The title of the plot.
        - xlabel, ylabel: Labels for the X-axis and Y-axis respectively.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - color: The color of the line.
        - linestyle: The style of the line ('-', '--', '-.', ':').
        - linewidth: The thickness of the line.
        - **kwargs: Additional keyword arguments to be passed to the matplotlib plot function.
        """
        plt.figure(figsize=figsize)
        plt.plot(x, y, color=color, linestyle=linestyle, linewidth=linewidth, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def pie(sizes, labels, colors=None, explode=None, title="Title", startangle=90, autopct='%1.1f%%', figsize=(8, 8),
            axis='equal', **kwargs):
        """
        Draws a pie chart for the given sizes.

        Parameters:
        - sizes: The sizes of the pie slices, usually represented as a fraction of the total.
        - labels: Labels for each slice of the pie.
        - colors: Colors for the slices, provided as a list. Optional.
        - explode: A list of values that "explode" slices out from the pie. Optional.
        - title: The title of the plot.
        - startangle: The starting angle of the first slice.
        - autopct: Format of the percentage labels on the slices.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - axis: The axis aspect ratio. 'equal' ensures the pie chart is circular. Optional.
        - **kwargs: Additional keyword arguments to be passed to the matplotlib pie function.
        """
        plt.figure(figsize=figsize)
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=autopct, startangle=startangle, **kwargs)
        plt.title(title)
        plt.axis(axis)  # Allows customization of the axis aspect ratio.
        plt.show()

    @staticmethod
    def violinplot(data, x=None, y=None, hue=None, title="Title", xlabel="X-axis", ylabel="Y-axis",
                   figsize=(10, 6), palette="muted", split=False, inner="quartile", **kwargs):
        """
        Draws a violin plot for the given dataset.

        Parameters:
        - data: The dataset to visualize. Should be a Pandas DataFrame.
        - x, y: Column names in the dataset. `x` should be a categorical variable, and `y` should be a numeric variable.
        - hue: Used to represent a categorical variable that will color the violin plots differently.
        - title: The title of the plot.
        - xlabel, ylabel: Labels for the X-axis and Y-axis respectively.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - palette: The color palette to use for the different levels of the `hue` variable.
        - split: If True, and a `hue` variable is used, draws half of a violin for each level of the hue variable.
        - inner: Representation of the quartiles inside the violin, options are "box", "quartile", "point", "stick", or None.
        - **kwargs: Additional keyword arguments to be passed to the seaborn violinplot function.
        """
        plt.figure(figsize=figsize)
        sns.violinplot(data=data, x=x, y=y, hue=hue, palette=palette, split=split, inner=inner, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def pairplot(data, hue=None, palette="muted", markers="o", height=2.5, aspect=1, suptitle="Pairplot of the Dataset",
                 title_y=1.02, **kwargs):
        """
        Draws a pairplot for visualizing relationships between multiple variables in a dataset.

        Parameters:
        - data: The dataset to visualize, should be a Pandas DataFrame.
        - hue: Categorical variable that will color the plots for different levels.
        - palette: The color palette to use for different levels of the `hue` variable.
        - markers: Marker styles for the scatter plots.
        - height: The height of each subplot.
        - aspect: Aspect ratio of each subplot, so that aspect * height gives the width of each subplot.
        - suptitle: The super title for the entire figure. Default is "Pairplot of the Dataset".
        - title_y: The vertical position of the super title. Default is slightly above the top at 1.02.
        - **kwargs: Additional keyword arguments to be passed to the seaborn pairplot function.
        """
        g = sns.pairplot(data, hue=hue, palette=palette, markers=markers, height=height, aspect=aspect, **kwargs)
        g.fig.suptitle(suptitle, y=title_y)  # Allows customization of the figure title's vertical position
        plt.show()

    @staticmethod
    def timeseries(data, x, y, title="Time Series Plot", xlabel="Time", ylabel="Value",
                   figsize=(12, 6), color='blue', linestyle='-', linewidth=2, **kwargs):
        """
        Draws a time series plot for the specified data.

        Parameters:
        - data: The dataset to be visualized, which should be a Pandas DataFrame with a time series index.
        - x: The column name in the dataset representing the time or date information.
        - y: The column(s) containing the values to be visualized. Can be a single column name or a list of column names.
        - title: The title of the plot.
        - xlabel, ylabel: Labels for the X-axis and Y-axis respectively.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - color: The color of the line(s). This parameter is used only if `y` specifies a single column.
        - linestyle: The style of the line(s) ('-', '--', '-.', ':').
        - linewidth: The thickness of the line(s).
        - **kwargs: Additional keyword arguments to be passed to the matplotlib `plot` function.
        """
        plt.figure(figsize=figsize)
        if isinstance(y, list):
            for column in y:
                plt.plot(data[x], data[column], linestyle=linestyle, linewidth=linewidth, label=column, **kwargs)
            plt.legend()
        else:
            plt.plot(data[x], data[y], color=color, linestyle=linestyle, linewidth=linewidth, **kwargs)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def geo_map(geo_data, title="Geographic Map", figsize=(10, 10), color='lightblue', edgecolor='black', nrows=1,
                ncols=1, **kwargs):
        """
        Draws a geographic map for the given geospatial data.

        Parameters:
        - geo_data: The geospatial dataset to be visualized, which should be a Geopandas GeoDataFrame.
        - title: The title of the map.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - color: The fill color for the geographic areas on the map.
        - edgecolor: The color of the edges/boundaries of the geographic areas.
        - nrows: The number of rows for the subplot grid.
        - ncols: The number of columns for the subplot grid.
        - **kwargs: Additional keyword arguments to be passed to the Geopandas `plot` function.
        """
        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        if nrows * ncols > 1:
            # In case of multiple subplots, `ax` will be an array.
            raise ValueError("geo_map currently supports only a single plot. Please set nrows and ncols to 1.")
        geo_data.plot(ax=ax, color=color, edgecolor=edgecolor, **kwargs)
        ax.set_title(title)
        plt.show()

    ######################################################################################################################

    from pandas.plotting import parallel_coordinates
    import matplotlib.pyplot as plt

    @staticmethod
    def parallel_coordinates(data, class_column, cols=None, color=None, title="Parallel Coordinates Plot",
                             figsize=(12, 6), **kwargs):
        """
        Draws a parallel coordinates plot for multidimensional dataset visualization.

        Parameters:
        - data: The dataset to be visualized, which must be a Pandas DataFrame.
        - class_column: The name of the column in the DataFrame that contains the class labels.
        - cols: An optional list of column names to be included in the plot. If None, all columns will be included.
        - color: An optional parameter to specify the colors of the lines for each class. Can be a list or a colormap.
        - title: The title of the plot.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - **kwargs: Additional keyword arguments to be passed to the pandas `parallel_coordinates` function.
        """
        plt.figure(figsize=figsize)
        # If specific columns are specified, create a DataFrame that includes only these columns along with the class column.
        if cols:
            data = data[cols + [class_column]]
        parallel_coordinates(data, class_column, color=color, **kwargs)
        plt.title(title)
        plt.show()

    import seaborn as sns
    import matplotlib.pyplot as plt

    @staticmethod
    def distplot(data, column, bins=30, kde=True, color="blue", title="Distribution Plot", figsize=(8, 6), **kwargs):
        """
        Visualizes the distribution of data using both a histogram and KDE (Kernel Density Estimate) on the same plot.

        Parameters:
        - data: The dataset to be visualized, which must be a Pandas DataFrame.
        - column: The name of the column in the DataFrame to be visualized.
        - bins: The number of bins to use for the histogram.
        - kde: A boolean indicating whether to overlay a KDE plot on the histogram.
        - color: The color for the plot elements.
        - title: The title of the plot.
        - figsize: The figure size as a tuple (width, height).
        - **kwargs: Additional keyword arguments to be passed to the seaborn `histplot` function.
        """
        plt.figure(figsize=figsize)
        sns.histplot(data=data, x=column, bins=bins, kde=kde, color=color, **kwargs)
        plt.title(title)
        plt.show()

    @staticmethod
    def countplot(data, column, palette="muted", title="Count Plot", figsize=(8, 6), **kwargs):
        """
        Visualizes the counts of observations in each categorical bin using bars.

        Parameters:
        - data: The dataset to be visualized, which must be a Pandas DataFrame.
        - column: The name of the categorical column in the DataFrame to count occurrences.
        - palette: The color palette to use for the different levels of the categorical variable.
        - title: The title of the plot.
        - figsize: The figure size as a tuple (width, height).
        - **kwargs: Additional keyword arguments to be passed to the seaborn `countplot` function.
        """
        plt.figure(figsize=figsize)
        sns.countplot(x=column, data=data, palette=palette, **kwargs)
        plt.title(title)
        plt.show()

    @staticmethod
    def jointplot(data, x, y, kind='scatter', color="blue", title="Joint Plot", title_y=1.03, **kwargs):
        """
        Creates a joint plot showing the relationship (and distributions) between two variables.

        Parameters:
        - data: The dataset to be visualized, which must be a Pandas DataFrame.
        - x: The name of the column in the DataFrame to be used on the X-axis.
        - y: The name of the column in the DataFrame to be used on the Y-axis.
        - kind: The kind of plot to draw, options include 'scatter', 'reg', 'resid', 'kde', and 'hex'.
        - color: The color for the plot elements.
        - title: The title of the entire figure.
        - title_y: The vertical position of the super title. Default is slightly above the top at 1.03.
        - **kwargs: Additional keyword arguments to be passed to the seaborn `jointplot` function.
        """
        g = sns.jointplot(x=x, y=y, data=data, kind=kind, color=color, **kwargs)
        g.fig.suptitle(title, y=title_y)  # Adjusts the title of the figure with customizable vertical position
        plt.show()

    @staticmethod
    def pairplot(data, hue=None, palette="muted", title="Pair Plot", title_y=1.03, **kwargs):
        """
        Generates scatter plots and histograms for each pair of numerical columns in the DataFrame.

        Parameters:
        - data: The dataset to be visualized, which must be a Pandas DataFrame.
        - hue: Categorical variable that will color the plots for different levels.
        - palette: The color palette to use for different levels of the `hue` variable.
        - title: The title of the entire figure.
        - title_y: The vertical position of the super title. Default is slightly above the top at 1.03.
        - **kwargs: Additional keyword arguments to be passed to the seaborn `pairplot` function.
        """
        g = sns.pairplot(data, hue=hue, palette=palette, **kwargs)
        g.fig.suptitle(title, y=title_y)  # Adjusts the title of the figure with customizable vertical position
        plt.show()

    @staticmethod
    def heatmap(data, title="Title", figsize=(10, 8), cmap="viridis", annot=False, **kwargs):
        """
        Draws a heatmap for the given data matrix.

        Parameters:
        - data: The data matrix for the heatmap. Can be either a numpy.ndarray or a pandas.DataFrame.
               If a DataFrame is provided, its correlation matrix will be visualized.
        - title: The title of the plot.
        - figsize: The size of the figure, formatted as (width, height) in inches.
        - cmap: The colormap to be used.
        - annot: If True, the values will be written in each cell.
        - **kwargs: Additional keyword arguments to be passed to the seaborn heatmap function.
        """
        plt.figure(figsize=figsize)
        if isinstance(data, np.ndarray):
            # Direct heatmap drawing for numpy.ndarray
            sns.heatmap(data, cmap=cmap, annot=annot, **kwargs)
        elif isinstance(data, pd.DataFrame):
            # Using the correlation matrix for pandas.DataFrame
            sns.heatmap(data.corr(), cmap=cmap, annot=annot, **kwargs)
        plt.title(title)
        plt.show()

    @staticmethod
    def kdeplot(data, column, shade=True, color="red", title="KDE Plot", figsize=(8, 6), xlabel=None, ylabel=None,
                **kwargs):
        """
        Draws a Kernel Density Estimate (KDE) plot for the specified column in the dataset.

        Parameters:
        - data: The dataset to be visualized, which must be a Pandas DataFrame.
        - column: The name of the column in the DataFrame for which the KDE plot will be generated.
        - shade: A boolean indicating whether to shade the area under the KDE curve.
        - color: The color for the plot.
        - title: The title of the plot.
        - figsize: The figure size as a tuple (width, height).
        - xlabel: The label for the X-axis. If None, no label is set.
        - ylabel: The label for the Y-axis. If None, no label is set.
        - **kwargs: Additional keyword arguments to be passed to the seaborn `kdeplot` function.
        """
        plt.figure(figsize=figsize)
        sns.kdeplot(data[column], shade=shade, color=color, **kwargs)
        plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def updated_violinplot(data, x=None, y=None, hue=None, split=True, inner="quart", palette="muted",
                           title="Violin Plot", figsize=(10, 6), xlabel=None, ylabel=None, **kwargs):
        """
        Draws an updated violin plot to show the density of the data distribution in more detail.

        Parameters:
        - data: The dataset to be visualized, which must be a Pandas DataFrame.
        - x: The name of the column in the DataFrame to be used on the X-axis.
        - y: The name of the column in the DataFrame to be used on the Y-axis.
        - hue: Categorical variable that will color the plots for different levels.
        - split: A boolean indicating whether to split the violin plot by the `hue` variable.
        - inner: Representation of the quartiles inside the violin, options include "box", "quartile", "point", "stick", or None.
        - palette: The color palette to use for different levels of the `hue` variable.
        - title: The title of the plot.
        - figsize: The figure size as a tuple (width, height).
        - xlabel: The label for the X-axis. If None, no label is set.
        - ylabel: The label for the Y-axis. If None, no label is set.
        - **kwargs: Additional keyword arguments to be passed to the seaborn `violinplot` function.
        """
        plt.figure(figsize=figsize)
        sns.violinplot(data=data, x=x, y=y, hue=hue, split=split, inner=inner, palette=palette, **kwargs)
        plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def swarmplot(data, x, y, hue=None, color="blue", title="Swarm Plot", figsize=(10, 6), xlabel=None, ylabel=None,
                  **kwargs):
        """
        Draws a swarm plot for categorical data to show the distribution of values and prevent overlap.

        Parameters:
        - data: The dataset to be visualized, which must be a Pandas DataFrame.
        - x: The name of the column in the DataFrame to be used on the X-axis.
        - y: The name of the column in the DataFrame to be used on the Y-axis.
        - hue: Categorical variable that will color the plots for different levels.
        - color: The color for the plot elements.
        - title: The title of the plot.
        - figsize: The figure size as a tuple (width, height).
        - xlabel: The label for the X-axis. If None, no label is set.
        - ylabel: The label for the Y-axis. If None, no label is set.
        - **kwargs: Additional keyword arguments to be passed to the seaborn `swarmplot` function.
        """
        plt.figure(figsize=figsize)
        sns.swarmplot(x=x, y=y, data=data, hue=hue, color=color, **kwargs)
        plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def facet_grid(data, row, col, plot_kind="scatter", palette="muted", title=None, title_y=1.03, figsize=None,
                   **kwargs):
        """
        Utilizes FacetGrid to partition the dataset by rows and columns, applying the specified plot type for each section.

        Parameters:
        - data: The dataset to be visualized, which must be a Pandas DataFrame.
        - row: The name of the column to define the row in the grid.
        - col: The name of the column to define the column in the grid.
        - plot_kind: The type of plot to apply, options include "scatter", "kde".
        - palette: The color palette for the plots.
        - title: The overall title for the grid of plots.
        - title_y: The vertical position of the super title.
        - figsize: The size of the figure as a tuple (width, height). If None, the default size is used.
        - **kwargs: Additional keyword arguments for the FacetGrid.
        """
        g = sns.FacetGrid(data, row=row, col=col, palette=palette, height=figsize[1] // 2 if figsize else 4,
                          aspect=(figsize[0] / figsize[1] if figsize else 1.5), **kwargs)
        if plot_kind == "scatter":
            g = g.map(plt.scatter, "x", "y")
        elif plot_kind == "kde":
            g = g.map(sns.kdeplot, "x", "y")

        if title:
            g.fig.suptitle(title, y=title_y)
        g.add_legend()
        plt.show()
