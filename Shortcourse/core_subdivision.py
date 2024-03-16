from Shortcourse.exceptions import ColumnNameError, EntryIndexOutOfRange, InvalidExcelPath
from Shortcourse.maths_subdivision import Mixin
import copy
from pandas import read_excel
"""
This is the core datastructure and related methods & helper functions. 
"""

class Subdivision(Mixin):  
    """ 
    Contains excel data in a raw matrix format. Features manipulation methods\n\n

    Properties:
    - .columns -> list of columns (vertical matrix) representing the excel data
    - .matrix -> like columns but is a list of rows (horizontal matrix). Columns and Matrix are synced.
    - .columnNames -> list of names of columns, in order. 
    - .metadata -> dictionary that holds True/False metadata about the table.
    - .columnTypes -> Stores the type found in each column.
    """

    def __init__(self, start_matrix: list, columnNames: list) -> None:
        self.columns = []  # Setter runs, matrix is declared as empty
        self.matrix = start_matrix
        # Matrix re-assigned here. From now on getter recalculates columns directly from matrix.
        # The column setter can be used for changing matrix by changing columns.
        self.columnNames = columnNames
        self.columnTypes = []
        self.metadata = {
            "clean": False,
            "filtered": False,
            "sorted": False,
            "rounded": False
        }
        # Outlier lists in column y and column x:
        self.outliers = []
        self.bottom_outlier_entries = []
        self.top_outlier_entries = []
        self.high_y_indices = []
        self.low_y_indices = []
        self.high_x_indices = []
        self.low_x_indices = []

    @property
    def columns(self) -> list:
        # Consider implementing caching so recalculation is not not needed as frequently
        return columnsFromMatrix(self.matrix)

    @columns.setter
    def columns(self, newColumns) -> list:
        self.matrix = matrixFromColumns(
            newColumns)  # Matrix first declared here

    @property
    def columnTypes(self) -> list:
        types = []
        if len(self.columns) == 0:
            return types
        for column in self.columns:
            types.append(type(column[0]))
        return types

    @columnTypes.setter
    def columnTypes(self, newTypes) -> list:
        return newTypes

    def __str__(self) -> str:
        """
        CSV format of subdivision.
        """
        message = "-" * 100 + "\n"
        for index, value in enumerate(self.columnNames):
            if index+1 == len(self.columnNames):
                message += f"{value}"
                break
            message += f"{value}, "
        message += "\n"
        for entry_index, entry_value in enumerate(self.matrix):
            row = ""
            for cell_index in range(len(entry_value)):
                if cell_index+1 == len(entry_value):
                    row += f"{self.matrix[entry_index][cell_index]}"
                    break
                row += f"{self.matrix[entry_index][cell_index]}, "
            message += f"{row}\n"
        message += "-" * 100
        return message

    def getColumn(self, columnName: str) -> list:
        """Returns the column with the corresponding columnName."""

        try:
            index = self.columnNames.index(columnName)
        except ValueError:
            raise ColumnNameError(columnName, self.columnNames)
        return self.columns[index]

    def getEntry(self, index: int) -> list:
        """
        Returns the entry (row) with corresponding index.
        """
        if len(self.matrix)-1 < index:
            raise EntryIndexOutOfRange(index, len(self.matrix)-1)

        entry = self.matrix[index]
        return entry

    def getColumnType(self, columnName: str) -> type:
        """Returns the type that appears in the column."""
        index = self.columnNames.index(columnName)
        return self.columnTypes[index]

    def editColumnName(self, oldName, newName) -> None:
        """Changes columnName from oldName to newName."""
        try:
            index = self.columnNames.index(oldName)
        except ValueError:
            raise ColumnNameError(oldName, self.columnNames)
        self.columnNames[index] = newName

    def removeEntries(self, indexes: list) -> list:
        """
        Removes entries (rows) from the subdivision and returns the entries.
        """
        entries = []
        for index in indexes:
            entries.append(self.matrix[index])
            self.matrix[index] = False

        while False in self.matrix:
            self.matrix.remove(False)

        return entries

    def clean(self, columnNames: list) -> list:
        """Removes all entries (rows) with NaN values in the column and returns their indexes."""
        removed_indexes = []
        for columnName in columnNames:
            column = self.getColumn(columnName)
            for index, cell in enumerate(column):
                if str(cell) == "nan":
                    removed_indexes.append(index)

        self.removeEntries(removed_indexes)
        self.metadata["clean"] = True
        return removed_indexes

    def filterByEntry(self, columnName: str, value: str) -> None:
        "Removes all entries (rows) without a certain value in a column."
        column = self.getColumn(columnName)
        removed_indexes = []
        for index, cell in enumerate(column):
            if cell != value:
                removed_indexes.append(index)
        self.removeEntries(removed_indexes)
        self.metadata["filtered"] = True

    def sortEntryValue(self, columnName: str, reverse_srt: bool = False) -> None:
        """Sorts entries (rows) by ascending order based on value in column."""
        column = self.getColumn(columnName)
        if type(column[0]) not in [float, int]:
            raise TypeError

        index_value_pair = list(enumerate(column))

        def getValue(pair): return pair[1]
        def getEntryFromPair(pair): return self.matrix[pair[0]]

        index_value_pair.sort(key=getValue, reverse=reverse_srt)
        self.matrix = [entry for entry in map(
            getEntryFromPair, index_value_pair)]
        self.metadata["sorted"] = True

    def clone(self):
        """"Clones the subdivision"""
        new_matrix = copy.deepcopy(self.matrix)
        new_columnName = copy.deepcopy(self.columnNames)
        return Subdivision(new_matrix, new_columnName)
    

#helper functions:
def columnsFromMatrix(matrix) -> list:
    """Turns the list of rows (matrix) into a list of columns."""
    columns = []
    for entry in range(len(matrix[0])):
        column = []
        for row in matrix:
            column.append(row[entry])
        columns.append(column)
    return columns


def matrixFromColumns(columns) -> list:
    """Turns list of columns into a list of rows (matrix)"""
    if len(columns) == 0:
        return []
    rows = []
    for index in range(len(columns[0])):
        row = []
        for column in columns:
            row.append(column[index])
        rows.append(row)
    return rows  # list of rows is the same as matrix


def subsetSubdivision(parent: Subdivision, columnNames: list) -> Subdivision:
    """Creates a subset of parent subdivision, including only columnNames."""
    if len(columnNames) < 1:
        raise ValueError
    if len(parent.columnNames) < len(columnNames):
        raise ValueError
    new_matrix = []
    for i in range(len(parent.matrix)):
        row = []
        for j in columnNames:
            row.append(parent.getColumn(j)[i])
        new_matrix.append(row)
    return Subdivision(new_matrix, columnNames)

def subdivisionFromExcel(path: str, columnNames: list) -> Subdivision:
    """Creates a subdivision from an Excel file path input. Only includes columnNames as in the Excel file."""
    try:
        raw = read_excel(path)
    except:
        raise InvalidExcelPath(path=path)
    try:
        droped_columns = raw.columns.drop(columnNames)
    except KeyError:
        raise ColumnNameError
    raw.drop(labels=droped_columns, axis="columns", inplace=True)
    messycolumns = []
    messyColumnNames = []  # Used later to order the columns correctly
    for name, content in raw.items():
        messyColumnNames.append(name)
        rows = []
        for i in content:
            rows.append(i)
        messycolumns.append(rows)

    # Create a list with garbage placeholders to overwrite
    columns = [i for i in range(len(columnNames))]
    for index, name in enumerate(columnNames):
        columns[index] = messycolumns[messyColumnNames.index(name)]
        # Fill placeholder list with columns in the correct order.

    matrix = matrixFromColumns(columns)
    new_subdivision = Subdivision(matrix, columnNames)
    return new_subdivision