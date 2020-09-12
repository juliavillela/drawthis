from random import randint

from db.tables import Table

class Deck:
    """ gets information from all table models which access the db """
    table_names =["subjects", "actions", "situations"]
    tables = {}

    #on initialize, uses language to create table models in tables dict
    def __init__(self, db):
        self.db = db
        self.deck_id = None
        self.filter = ""

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

    #finds table by name and returns dict with table information to view
    #for route admin
    def get_table(self, name):
        table_dict = {
            'name': name,
            'keys': self.tables[name].columns,
            'data': self.tables[name].data
            }
        return table_dict

    #add deck id to data dict recieved from view, then adds to table and reloads
    def add(self, name, item_data):
        item_data['deck_id'] = self.deck_id
        self.tables[name].add(item_data)
        self.tables[name].load(self.filter)

    def destroy(self, name, item_id):
        self.tables[name].delete(item_id)
        self.tables[name].load(self.filter)

    #reloads tables in the new language
    #for __init__ and language change
    def load(self, deck_id):
        self.tables = {}
        self.deck_id = deck_id
        self.filter = "WHERE deck_id = " + deck_id

        for name in self.table_names:
            self.tables[name] = self.instantiate_table(name)
        # adds placeholder data for empty tables
        for table in self.tables:
            data = self.tables[table].data
            if len(data) < 1:
                tmp = {}
                tmp['id'] = 0;
                tmp['main'] = "no content yet!"
                tmp['deck_id'] = self.deck_id
                data.append(tmp)

    #make instances of Table for every table in self.table_names
    def instantiate_table(self, name):
            #create tables
            table = Table(self.db, name)
            if self.filter:
                table.load(self.filter)
            else:
                table.load()
            return table

    #deletes all items in tables from the selected deck id
    def clear_deck_data(self, deck_id):
        self.tables = {}
        self.deck_id = deck_id
        self.filter = "WHERE deck_id = " + deck_id
        for name in self.table_names:
            table = Table(self.db, name)
            table.clear_deck_data(self.filter)
        self.deck_id = None
        self.tables= {}
