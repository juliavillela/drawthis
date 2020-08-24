class ImagesController:
    def __init__(self, db, upload_folder):
        self.dir = upload_folder
        self.db = db

    def get_filename():
        pass

    def create(self, user_id, file_extention, title="", cards=""):
        self.db.execute("INSERT INTO images (user_id, title, cards) VALUES (:user_id, :title, :cards)", user_id=user_id, title=title, cards=cards)
        this_row = self.db.execute("SELECT id FROM images WHERE user_id = :user_id ORDER BY id DESC LIMIT 1", user_id = user_id)
        id = this_row[0]["id"]
        filename = "img" + str(id) + file_extention
        image = {'id': id, 'filename':filename }
        return image

    def delete(self, image_id):
        self.db.execute("DELETE FROM images WHERE id = :id", id = image_id)

    def update(self, image_id, image_path):
        self.db.execute("UPDATE images SET path = :path WHERE id = :id", path=image_path, id=image_id)


    def list(self):
        rows = self.db.execute("SELECT id FROM images")
        filenames = []
        for row in rows:
            filename = "img" + str(row["id"]) + ".jpg"
            filenames.append(filename)
        return filenames
