from cs50 import SQL
from database.table_model import Table

class TablesController:

    db = SQL("sqlite:///database/drawthis.db")
    tables = {}
    validation = {
        "language":["en", "pt"],
        "gender":["m", "f", "n"],
        "plural":[True, False, None],
        "position":[1,2,None]
    }

    def __init__(self, table_names):
        self.create_tables(table_names)

    def create_tables(self, table_names):
        #make instances of Table for every table in table_names
        for name in table_names:
            #create tables
            table = Table(self.db, name)
            #add validation info
            for val in self.validation:
                if val in table.columns:
                    table.columns[val] = self.validation[val]
            #add table to dict tables
            self.tables[name] = table

    def get_table(self, name):
        table_dict = {
            'name':self.tables[name].name,
            'keys': self.tables[name].columns,
            'data': self.tables[name].list()}
        return table_dict

    def add(self, name, data_dict):
        self.tables[name].create(data_dict)
