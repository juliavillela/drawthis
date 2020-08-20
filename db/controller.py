from cs50 import SQL
from random import randint

from db.tables import Table

class TablesController:
    """ gets information from all table models which access the db """
    db = SQL("sqlite:///db/drawthis.db")
    table_names = ['nouns', 'adjectives', 'actions', 'situations', 'instructions']
    tables = {}
    validation = {
        "require":[],
        "position":["before","after","any"],
        "type":['time', 'mood', 'place', 'environement']
    }

    #on initialize, uses language to create table models in tables dict
    def __init__(self, language):
        self.language = language
        self.load(language)

    #selects options based on filter, or selects all from table if no filter
    #returns a random item from those options
    def get_random(self, names, filter_out=None):
        options = []
        for name in names:
            if filter_out:
                options.extend(self.filter_out(name, filter_out))
            else:
                options.extend(self.tables[name].data)
        random = randint(0, len(options) - 1)
        return options[random]

    #from dict specifying the unwanted values for each column
    #filters out rows containing those values
    def filter_out(self, name, filter_out):
        options = []
        #for each item in table data, push into options those which dont match filter out
        for row in self.tables[name].data:
            include = True
            for column in row:
                if column in filter_out and filter_out[column] == row[column]:
                    include = False
                    break
            if include:
                options.append(row)
        return options

    #finds table by name and returns dict with table information to view
    #for route admin
    def get_table(self, name):
        table_dict = {
            'name': name,
            'keys': self.tables[name].columns,
            'data': self.tables[name].data
            }
        return table_dict

    def add(self, name, item_data):
        self.tables[name].add_item(item_data)

    def destroy(self, name, item_id):
        self.tables[name].remove_item(item_id)

    #reloads tables in the new language
    #for __init__ and language change
    def load(self, language):
        self.language = language
        self.instantiate_table()
        self.set_validation()

    #make instances of Table for every table in self.table_names
    def instantiate_table(self):
        for name in self.table_names:
            #create tables
            table_name = name + self.language
            table = Table(self.db, table_name)
            table.load()
            self.tables[name] = table

    #add validation values
    def set_validation(self):
        #clears leftover information in require
        self.validation['require'] = []
        # adds columns in adjectives as options for noun requires
        for option in self.tables['adjectives'].columns:
            if option != "id" and option != "position":
                self.validation['require'].append(option)
        #stores validation informatio in tables.
        for table in self.tables.values():
            for val in self.validation:
                if val in table.columns:
                    table.columns[val] = self.validation[val]
