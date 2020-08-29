class DbHelper:
    def __init__(self, db, table_name, filter=None):
        self.db = db;
        self.name = table_name;
        self.columns = [];

    #adds new item do db
    def add(self, data_dict):
        #format dict to fit query
        s = ", "
        columns = []
        values = []
        for data in data_dict:
            columns.append(data)
            values.append(self.literal(str(data_dict[data])))
        #add item to db
        query = "INSERT INTO " + self.name + " (" + s.join(columns) + ") VALUES (" + s.join(values) + " );"
        print(query)
        self.db.execute(query)
        id_dict = self.db.execute("SELECT last_insert_rowid()")
        id = id_dict[0].get('last_insert_rowid()')
        return id

    def update(self, item_id, data_dict):
        for data in data_dict:
            string = data + " = " + self.literal(data_dict.get(data))
            query = "UPDATE " + self.name + " SET " + string + " WHERE id = " + str(item_id)
            self.db.execute(query)

    def delete(self, item_id):
        query = "DELETE FROM " + self.name + " WHERE id = :id"
        self.db.execute(query, id=item_id)

    def list(self):
        query = "SELECT * FROM :table"
        all = self.db.execute(query, table=self.name)
        return all

    def all_from_user(self, user_id):
        query = "SELECT * FROM :table WHERE user_id = :value ORDER BY id DESC"
        all = self.db.execute(query, table=self.name, value=user_id)
        return all

    def find(self, item_id):
        query = "SELECT * FROM :table WHERE id = :id"
        item = self.db.execute(query, table=self.name, id=item_id);
        if len(item) == 1:
            return item[0]
        else:
            return None

    #inserts extra quotes in strings for the query
    def literal(self, string):
        literal = "'" + string + "'"
        return literal
