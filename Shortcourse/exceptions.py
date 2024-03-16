class ColumnNameError(Exception):
    """Raised when column name does not exist"""
    def __init__(self, name=None, name_list=None):
        self.message = f"Column name {name} is not in avalailable names: {name_list}"
        if name == None and name_list == None:
            self.message = f"Column names specified do not exist in excel document"
        super().__init__(self.message)

class EntryIndexOutOfRange(Exception):
    """Raised when entry index is out of range"""
    def __init__(self, index=None, max=None):
        if index == None or max == None:
            self.message = "Index out of range. No details provided."
        self.message = f"Entry index:{index} is out of max range: {max}"
        super().__init__(self.message)

class InvalidExcelPath(Exception):
    """Raised when no Excel found in provided path""" 
    def __init__(self, path="Missing."):
        self.message = f"Excel document not found at path: {path}"
        super().__init__(self.message)

class DirtyData(Exception):
    """Raised when \"Not a Number\" values are found in data"""
    def __init__(self):
        self.message = f"Data was not cleaned before. Run clean first"
        super().__init__(self.message)