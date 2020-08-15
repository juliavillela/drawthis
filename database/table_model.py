class Table:

    def __init__(self, db, name):
        self.db = db;
        self.name = name
        self.phrases = []
        self.columns = self.get_columns()
        self.count = 0


    def list(self, filter=""):
        rows = self.db.execute("SELECT * FROM " + self.name + filter)
        return rows

    def create(self, data_dict):
        separator = ", "
        columns = []
        values = []
        for data in data_dict:
            columns.append(data)
            literal = "'" + data_dict[data] + "'"
            values.append(literal)
        data_string = separator.join(values)
        col_strin = separator.join(columns)
        query = "INSERT INTO " + self.name + " (" + col_strin + ") VALUES (" + data_string + " );"

        self.db.execute(query)

    # def find(self, item_id):
    #     rows = self.db.execute("SELECT * FROM " + self.name + " WHERE id =" + str(item_id))
    #     if len(rows) != 1:
    #         return None
    #     else:
    #         return rows[0]

    def destroy(self, item_id):
        self.db.execute("DELETE FROM " + self.name + " WHERE id=" + item_id)

    def load(self, filter):
        self.unload()
        all = self.list(filter)
        for row in all:
            self.phrases.append(row)
        self.update_count()

    def unload(self):
        self.phrases = [];

# """ inner class methods """
    # def literal(string):
    #     literal = "'" + string + "'"
    #     return literal

    def get_columns(self):
        columns={}
        columns_obj = self.db.execute("SELECT name FROM PRAGMA_TABLE_INFO('" + self.name + "');")
        for column in columns_obj:
            columns[column['name']] = None
        return columns

    def update_count(self):
        self.count = len(self.phrases)
