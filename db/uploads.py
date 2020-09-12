from db.db_helper import DbHelper

class Uploads(DbHelper):

    def gallery(self):
        query = "SELECT username, cards, path, user_id FROM users JOIN uploads ON users.id = uploads.user_id"
        return self.db.execute(query)
