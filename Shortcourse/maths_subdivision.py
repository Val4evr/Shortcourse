from Shortcourse.exceptions import DirtyData
import sigfig as sig
import statistics as stats
from typing import Tuple, Callable, Optional
from scipy.stats import pearsonr

class Mixin():
    def round_entries(self, sigfig: int = 3, columnNames: list = None) -> None:
        """Rounds all entries in columnNames."""
        if self.metadata["clean"] == False:
            raise DirtyData
        # Round all values with columnNames
        if columnNames == None:
            columnNames = self.columnNames  # Round all columns

        new_columns = []
        for columnName in columnNames:
            column = self.getColumn(columnName)
            if type(column[0]) not in [float, int]:  # skip non-numerical columns
                continue
            new_column = []
            for cell in column:
                new_column.append(sig.round(cell, sigfigs=sigfig))
            new_columns.append(new_column)

        self.columns = new_columns
        self.metadata["rounded"] = True

    def quartileValue(self, columnName: str, q: int = 1) -> float:
        """
        Calculates the greatest value to fall into quartile q.
        """
        if self.getColumnType(columnName) not in [float, int]:
            raise ValueError  # Maybe write a custom exception
        column = self.getColumn(columnName)
        cuts = stats.quantiles(column)
        return cuts[q-1]

    def quartileRange(self, columnName: str) -> float:
        """
        Returns the interquartile range for the column.
        """
        return self.quartileValue(columnName, q=3) - self.quartileValue(columnName, q=1)

    def findQuartile(self, columnName: str, value) -> int:
        """
        Returns the quartile in which the value is located.
        """
        q1 = self.quartileValue(columnName, q=1)
        q2 = self.quartileValue(columnName, q=2)
        q3 = self.quartileValue(columnName, q=3)

        if value < q1:
            return 1
        elif value < q2:
            return 2
        elif value < q3:
            return 3
        else:
            return 4

    def remove_outliers(self, columnNameX: str = None, columnNameY: str = None, boxplot: bool = False) -> list:
        """
        Removes outliers in both the x and y columns and returns them.
        """
        if (columnNameX == None) and (columnNameY == None):
            columnNameX = self.columnNames[0]
            columnNameY = self.columnNames[1]

        x = self.getColumn(columnNameX)
        y = self.getColumn(columnNameY)

        topX = self.quartileValue(columnNameX, 3) + \
            1.5 * self.quartileRange(columnNameX)
        bottomX = self.quartileValue(
            columnNameX, 1) - 1.5 * self.quartileRange(columnNameX)
        topY = self.quartileValue(columnNameY, 3) + \
            1.5 * self.quartileRange(columnNameY)
        bottomY = self.quartileValue(
            columnNameY, 1) - 1.5 * self.quartileRange(columnNameY)

        bottom_outlier_indices = []
        top_outlier_indices = []

        for index, entry in enumerate(x):
            if entry > topX:
                top_outlier_indices.append(index)
                self.high_x_indices.append(index)
            elif entry < bottomX:
                bottom_outlier_indices.append(index)
                self.low_x_indices.append(index)

        if not boxplot:
            for index, entry in enumerate(y):
                if entry > topY:
                    if index not in top_outlier_indices:
                        top_outlier_indices.append(index)
                        self.high_y_indices.append(index)
                elif entry < bottomY:
                    if index not in bottom_outlier_indices:
                        bottom_outlier_indices.append(index)
                        self.low_y_indices.append(index)
        else:
            for index, entry in enumerate(y):
                if entry > topY:
                    top_outlier_indices.append(index)
                    self.high_y_indices.append(self.matrix[index])
                elif entry < bottomY:
                    bottom_outlier_indices.append(index)
                    self.low_y_indices.append(self.matrix[index])

        self.bottom_outlier_entries = [self.matrix[index]
                                        for index in bottom_outlier_indices]
        self.top_outlier_entries = [self.matrix[index]
                                    for index in top_outlier_indices]

        self.remove_entries(bottom_outlier_indices + top_outlier_indices)

        self.outliers = self.top_outlier_entries + self.bottom_outlier_entries

        return self.outliers

    def mean(self, columnName: str) -> float:
        """
        Calculates the mean for column with columnName.
        """

        if self.getColumnType(columnName) not in [float, int]:
            raise ValueError  # Maybe write a custom exception

        column = self.getColumn(columnName)
        return stats.mean(column)

    def regression(self, columnNameX: str = None, columnNameY: str = None) -> Tuple[Callable, str]:
        """
        Returns function for drawing the regression line and string representation of function. 
        """
        if len(self.columns) == 2 and (columnNameX == None and columnNameY == None):
            columnNameX = self.columnNames[0]
            columnNameY = self.columnNames[1]

        if (self.getColumnType(columnNameX) and self.getColumnType(columnNameY)) not in [float, int]:
            raise TypeError

        x = self.getColumn(columnNameX)
        y = self.getColumn(columnNameY)
        slope, intercept = stats.linear_regression(x, y)
        def equation(x): return slope * x + intercept
        string_equation = f"y={sig.round(slope, sigfigs=3)}x + {sig.round(intercept, sigfigs=3)} (3s.f)"
        return equation, string_equation

    def stdev(self, columnName) -> float:
        """
        Returns the standard deviation of the column.
        """
        if self.getColumnType(columnName) not in [float, int]:
            raise ValueError
        column = self.getColumn(columnName)
        return stats.stdev(column)

    def pmcc(self, columnNameX: str = None, columnNameY: str = None) -> float:
        """
        Returns the pmcc value for the columns.
        """
        if len(self.columns) == 2 and (columnNameX and columnNameY) == None:
            columnNameX = self.columnNames[0]
            columnNameY = self.columnNames[1]
        if (self.getColumnType(columnNameX) and self.getColumnType(columnNameY)) not in [float, int]:
            raise TypeError
        x = self.getColumn(columnNameX)
        y = self.getColumn(columnNameY)
        return stats.correlation(x, y)

    def hypothesis_test(self, columnNameX: str = None, columnNameY: str = None, test_type: str = "two-tailed", value_table: bool = True, sig_level: float = 0.05) -> Optional[Tuple[float, float]]:
        """
        Tests the hypothesis that columnNameX and columnNameY have no linear correlation, at the specified significance level.

        The following test_types are supported:
        - "two-tailed" -> Accept alternate if ANY correlation is found. 
        - "positive" -> Accept alternate ONLY IF POSITIVE correlation is found.
        - "negative" -> Accept alternate ONLY IF NEGATIVE correlation is found. 

        There is an option to interpolate between pre-calculated critical PMCC values that is on by default.
        Setting value_table to False disables it and is the better method.
        Interpolating is only useful because it can be marked. 

        If value_table is False, the PMCC and p-value will be returned. 
        """

        def import_criticals():
            with open(r"Shortcourse/resources/pearson_values.csv", "r") as criticals:
                n_values = {}
                for index, value in enumerate(criticals):
                    if index == 0:
                        continue
                    splits = value.split(",")
                    splits = [float(i.strip()) for i in splits]
                    n = int(splits.pop())
                    n_values[n] = splits
                return n_values

        def print_test(pmcc):
            print("***************************")
            print(f"Hypothesis test of {columnNameX} and {columnNameY}:")
            print(f"N:{n}")
            print(f"PMCC:{pmcc}")
            print("H0: r = 0")
            if pmcc > 0:
                print("H1: r > 0")
            else:
                print("H1: r < 0")

        def interpolate(criticals, n, index):
            digit1 = n // 10

            low_n = digit1 * 10
            high_n = digit1 * 10 + 10

            low_c = criticals[low_n][index]
            high_c = criticals[high_n][index]

            cvalue = ((n-low_n) * (high_c-low_c)/(high_n-low_n)) + low_c
            cvalue = sig.round(cvalue, sigfigs=3)
            return cvalue

        match test_type:
            case "two-tailed":
                test_type = "two-sided"
            case "positive":
                test_type = "greater"
            case "negative":
                test_type = "less"
            case _:
                ValueError("Invalid test type")

        if len(self.columns) == 2 and (columnNameX and columnNameY) == None:
            columnNameX = self.columnNames[0]
            columnNameY = self.columnNames[1]

        if (self.getColumnType(columnNameX) and self.getColumnType(columnNameY)) not in [float, int]:
            raise TypeError

        x = self.getColumn(columnNameX)
        y = self.getColumn(columnNameY)

        pmcc, pvalue = pearsonr(x, y, alternative=test_type)
        pmcc = sig.round(pmcc, sigfigs=3)

        n = len(x)

        if not value_table: # Returns PMCC and p-value if not in interpolation mode.
            print_test(pmcc)
            print(f"P ={pvalue}")
            if pvalue > sig_level:
                print("Accept H0")
            else:
                print("Reject H0")
                print("***************************")
            return pmcc, pvalue

        if (test_type not in ["greater", "less"]) or (sig_level not in [0.1, 0.05, 0.025, 0.01, 0.005]):
            ValueError(
                f"Only one tailed tests supported in table mode with only these sig levels: 0.1, 0.05, 0.025, 0.01, 0.005")

        value_index = [0.1, 0.05, 0.025, 0.01, 0.005].index(sig_level)
        criticals = import_criticals()
        if n < 4 or n > 100:
            ValueError(f"The n value: {n} is outside the table range")
        if n in criticals:
            critical_value = sig.round(
                criticals[n][value_index], sigfigs=3, warn=False)
            interpolated = False
        else:
            critical_value = interpolate(criticals, n, value_index)
            interpolated = True

        print_test(pmcc)
        if interpolated:
            print(f"INTERPOLATED Critical value: {critical_value}")
        else:
            print(f"Critical value: {critical_value}")
        if abs(pmcc) > critical_value:
            print(f"{abs(pmcc)} > {critical_value}")
            print("Reject H0. There is correlation")
        else:
            print(f"{abs(pmcc)} < {critical_value}")
            print("Accept H0. No correlation")
        print("***************************")