from cs50 import SQL

class DB:
    def __init__(self, path):
        self.db = SQL("sqlite:///" + path)
        self.tables = ["nouns", "adjectives", "actions", "situations"]


    def get_all(self):
        tables = []
        for table in self.tables:
            data = self.get_all_from(table)
            tables.append(data)
        return tables

    def get_all_from(self, table_name):
        table = {'table_name':table_name, 'keys': None, 'data':[]}
        table['keys'] = self.db.execute("SELECT name FROM PRAGMA_TABLE_INFO('" + table_name + "');")
        data = self.db.execute("SELECT * FROM " + table_name)
        for r in data:
            row = r.values()
            table['data'].append(row)
        return table
