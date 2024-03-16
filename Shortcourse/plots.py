from Shortcourse.core_subdivision import Subdivision, matrixFromColumns

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from typing import Callable

class ScatterResult(Subdivision):
    def __init__(self, start_matrix: list, columnNames: list, fig: Figure, ax: Axes):
        super().__init__(start_matrix, columnNames)
        self.ax = ax
        self.fig = fig

    def saveScatter(self, outpath: str = None) -> None:
        x = self.ax.get_xlabel()
        y = self.ax.get_ylabel()
        if outpath == None:
            outpath = f"./scatter_{y} on {x}"
        self.fig.savefig(outpath)
        print(f"Image saved to: {outpath}")

    def addRegression(self, equation: Callable = None, string_equation: str = None, plot_equation=True, font_size: int = 12) -> None:
        if equation == None:
            equation, string_equation = self.regression()
        else:
            if plot_equation and string_equation == None:
                # Equation plot requested, but unable because string not provided with equation.
                raise ValueError
        model = list(map(equation, self.columns[0]))
        self.ax.plot(self.columns[0], model, label=string_equation)
        plt.legend(fontsize=font_size)

    def plotMultiOutliers(self, high_c: str = "C1", low_c: str = "C2", low_label: str = "low outlier", high_label: str = "high outlier"):
        if self.outliers == None:
            self.remove_outliers(self.columnNames[0], self.columnNames[1])

        x_top = [outlier[0] for outlier in self.top_outlier_entries]
        y_top = [outlier[1] for outlier in self.top_outlier_entries]

        x_bottom = [outlier[0] for outlier in self.bottom_outlier_entries]
        y_bottom = [outlier[1] for outlier in self.bottom_outlier_entries]

        if len(x_bottom) != 0:
            self.ax.scatter(x_bottom, y_bottom, label=low_label, color=low_c)
        else:
            print("no bottom outliers found")
        if len(x_top) != 0:
            self.ax.scatter(x_top, y_top, label=high_label, color=high_c)
        else:
            print("no top outliers found")

    def changesize(self, width=True, smaller=False, value: int = 2):
        if width:
            old = self.fig.get_figwidth()
            if not smaller:
                new = old+value
            else:
                new = old-3
            self.fig.set_figwidth(new)
        else:
            old = self.fig.get_figheight()
            if not smaller:
                new = old+value
            else:
                new = old-value
            self.fig.set_figheight(new)

    def print_outliers(self, columnName: str, parent: Subdivision = None) -> None:
        if parent == None:
            parent = self

        line = "*" * 30
        try:
            index = parent.columnNames.index(columnName)
        except ValueError:
            raise ValueError("This columnName is not in parent")

        print("Outliers:")
        if len(self.low_x_indices) > 0:
            print()
            print("Low X outliers:")
            for i in self.low_x_indices:
                print(parent.matrix[i][index], end=", ")
            print()

        if len(self.high_x_indices) > 0:
            print()
            print("High X outliers:")
            for i in self.high_x_indices:
                print(parent.matrix[i][index], end=", ")
            print()

        if len(self.low_y_indices) > 0:
            print()
            print("Low Y outliers:")
            for i in self.low_y_indices:
                print(parent.matrix[i][index], end=", ")
            print()

        if len(self.high_y_indices) > 0:
            print()
            print("High Y outliers:")
            for i in self.high_y_indices:
                print(parent.matrix[i][index], end=", ")
            print()

        print(line)

class BoxResult(Subdivision):
    def __init__(self, start_matrix: list, columnNames: list, fig: Figure, ax: Axes):
        super().__init__(start_matrix, columnNames)
        self.ax = ax
        self.fig = fig

    def save_box(self, outpath: str = None) -> None:
        if outpath == None:
            outpath = f"./boxplot"
        self.fig.savefig(outpath)
        print(f"Image saved to: {outpath}")

    def changesize(self, width=True, smaller=False, value: int = 2):
        if width:
            old = self.fig.get_figwidth()
            if not smaller:
                new = old+value
            else:
                new = old-value
            self.fig.set_figwidth(new)
        else:
            old = self.fig.get_figheight()
            if not smaller:
                new = old+value
            else:
                new = old-value
            self.fig.set_figheight(new)

def plot_dual_box(subdivision: Subdivision, columnName1: str = None, columnName2: str = None, title: str = None, one_title: str = None, two_title: str = None):
    # Having 2 Subdivisions as the arguments would be better.
    if len(subdivision.columns) == 2 and (columnName1 == None and columnName2 == None):
        columnName1 = subdivision.columnNames[0]
        columnName2 = subdivision.columnNames[1]

    column1 = subdivision.getColumn(columnName1)
    column2 = subdivision.getColumn(columnName2)

    if one_title == None:
        one_title = columnName1
    if two_title == None:
        two_title = columnName2

    if title == None:
        title = f"{one_title} with {two_title}"

    fig, ax = plt.subplots()

    ax.boxplot(x=[column1, column2], vert=False, manage_ticks=True)

    ax.set_yticklabels([one_title, two_title])
    fig.set_figwidth(10)
    ax.set_title(title)
    ax.minorticks_on()
    new_matrix = matrixFromColumns([column1, column2])
    new_columnNames = [columnName1, columnName2]
    return BoxResult(new_matrix, new_columnNames, fig, ax)
 
def plot_scatter(subdivision: Subdivision, columnNameX: str = None, columnNameY: str = None, title: str = "scatter", xTitle: str = None, yTitle: str = None):
    if len(subdivision.columns) == 2 and (columnNameX == None and columnNameY == None):
        columnNameX = subdivision.columnNames[0]
        columnNameY = subdivision.columnNames[1]

    if (subdivision.getColumnType(columnNameX) and subdivision.getColumnType(columnNameY)) not in [float, int]:
        raise TypeError

    if xTitle == None:
        xTitle = columnNameX
    if yTitle == None:
        yTitle = columnNameY

    x = subdivision.getColumn(columnNameX)
    y = subdivision.getColumn(columnNameY)

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.grid(True)
    ax.set_title(title)
    ax.set_xlabel(xTitle)
    ax.set_ylabel(yTitle)
    ax.minorticks_on()
    new_columnNames = [columnNameX, columnNameY]
    new_matrix = matrixFromColumns([x, y])
    return ScatterResult(new_matrix, new_columnNames, fig, ax)