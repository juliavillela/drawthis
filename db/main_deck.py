from random import randint
from db.deck import Deck

from db.tables import Table

class MainDeck(Deck):
    """ gets information from all table models which access the db """
    table_names = ['nouns', 'adjectives', 'actions', 'situations', 'instructions']
    tables = {}
    validation = {
        "require":[],
        "position":["before","after","any"],
        "type":['time', 'mood', 'place', 'environement']
    }

    #on initialize, uses language to create table models in tables dict
    def __init__(self, db, language):
        self.db = db
        self.language = language
        self.filter = None
        self.load(language)

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

    #reloads tables in the new language
    #for __init__ and language change
    def load(self, language):
        self.language = language
        for name in self.table_names:
            self.tables[name] = self.instantiate_table(name + self.language)
        self.set_validation()


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
