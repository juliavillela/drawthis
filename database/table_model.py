class Table:

    def __init__(self, db, name):
        self.db = db;
        self.name = name
        self.columns = self.get_columns()
        self.row_count = self.row_count()

    def get_columns(self):
        columns={}
        columns_obj = self.db.execute("SELECT name FROM PRAGMA_TABLE_INFO('" + self.name + "');")
        for column in columns_obj:
            columns[column['name']] = None
        return columns

    def row_count(self):
        rows = self.list()
        count = len(rows)
        return count

    def list(self):
        rows = self.db.execute("SELECT * FROM " + self.name)
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

    def find(self, item_id):
        rows = self.db.execute("SELECT * FROM " + self.name + " WHERE id =" + str(item_id))
        if len(rows) != 1:
            return None
        else:
            return rows[0]

    def destroy(self, item_id):
        self.db.execute("DELETE FROM " + self.name + " WHERE id=" + item_id)
