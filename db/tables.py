class Table:

    def __init__(self, db, name):
        self.db = db;
        self.name = name
        self.columns = self.get_columns()
        self.data = []

    #loads db into memory
    def load(self):
        self.data = []
        rows = self.db.execute("SELECT * FROM " + self.name + " ORDER BY id DESC")
        for row in rows:
            self.data.append(row)

    #adds new item to table and reloads DATA content
    def add_item(self, item_data):
        #format dict to fit query
        s = ", "
        columns = []
        values = []
        for data in item_data:
            columns.append(data)
            values.append(self.literal(item_data[data]))
        #add item to db
        query = "INSERT INTO " + self.name + " (" + s.join(columns) + ") VALUES (" + s.join(values) + " );"
        self.db.execute(query)
        #reload self
        self.load()

    #Deletes item from table and reloads DATA content
    def remove_item(self, item_id):
        if item_id:
            self.db.execute("DELETE FROM " + self.name + " WHERE id=" + item_id)
        self.load()

    #gets column names in table and sets it up as a dict
    #of column name and validation(to be added by the controller)
    def get_columns(self):
        columns={}
        columns_obj = self.db.execute("SELECT name FROM PRAGMA_TABLE_INFO('" + self.name + "');")
        for column in columns_obj:
            columns[column['name']] = None
        return columns

    #inserts extra quotes in strings for the query
    def literal(self, string):
        literal = "'" + string + "'"
        return literal
