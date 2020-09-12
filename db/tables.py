from db.db_helper import DbHelper

class Table(DbHelper):
    data = []

    #loads db into memory
    def load(self, filter=""):
        self.data = []
        #makes sure table exists
        exists = self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=:name", name = self.name)
        if exists:
            self.columns = self.get_columns()
            print(self.columns)
            #then loads if exists
            query = "SELECT * FROM :table " + filter + " ORDER BY id DESC"
            rows = self.db.execute(query, table = self.name )
            if len(rows) > 0:
                for row in rows:
                    self.data.append(row)

    #gets column names in table and sets it up as a dict
    #of column name and validation(to be added by the controller)
    def get_columns(self):
        columns={}
        columns_obj = self.db.execute("SELECT name FROM PRAGMA_TABLE_INFO('" + self.name + "');")
        for column in columns_obj:
            columns[column['name']] = None
        return columns

    #removes from db all data related to deck;
    def clear_deck_data(self, filter):
        query = "DELETE FROM :table " + filter
        self.db.execute(query, table = self.name)

    def add(self, data):
        query= "INSERT INTO :table (deck_id, main) VALUES (:deck_id, :main)"
        self.db.execute(query, table=self.name, deck_id = data['deck_id'], main=data['main'])
