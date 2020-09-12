from db.db_helper import DbHelper

class Users(DbHelper):

    def find(self, item_id):
        s=" "
        query =["SELECT users.id, username, hash, path as avatar FROM",
        "users JOIN avatars",
        "ON avatars.id = users.avatar_id",
        "WHERE users.id = :user_id"]

        item = self.db.execute(s.join(query), user_id=item_id);
        if len(item) == 1:
            return item
        else:
            return None

    def usernames(self):
        names = self.db.execute("SELECT username FROM users")
        name_array =[]
        for row in names:
            name_array.append(row['username'])
        return name_array
