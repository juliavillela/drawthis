from cs50 import SQL
from random import randint
from database.table_model import Table

class TablesController:
    # """ gets information from all table models which access the db """

    db = SQL("sqlite:///database/drawthis.db")
    tables = {}
    validation = {
        "language":["en", "pt"],
        "gender":["m", "f", "n"],
        "plural":[True, False, None],
        "position":[1,2,None]
    }
#on initialize, uses input table names to create table models in tables dict
    def __init__(self, table_names):
        self.create_tables(table_names)

#creates instances of Table, adds validation and appends to tables
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

#finds table by name and returns dict to view
    def get_table(self, name):
        table_dict = {
            'name':self.tables[name].name,
            'keys': self.tables[name].columns,
            'data': self.tables[name].list()}
        return table_dict

#passes info to table model for creating a new row in table
    def add(self, name, data_dict):
        self.tables[name].create(data_dict)

#deletes row in table
    def destroy(self, name, item_id):
        self.tables[name].destroy(item_id)

#loads dict in Table according to language filter
    def load(self, language):
        for table in self.tables.values():
            table.load(" WHERE language= '" + language + "'")

#selects a random item in table and returns
    def get_random(self, name):
        length = self.tables[name].count - 1
        index = randint(0 , length)
        random = self.tables[name].phrases[index]
        return random
