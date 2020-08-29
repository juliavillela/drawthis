import os

from db.controller import TablesController
from db.cards_picker import CardsPicker
from db.db_helper import DbHelper

class Controller:

    def __init__(self, db):
        self.main_db = TablesController(db, "_en")
        self.draw = CardsPicker(self.main_db)
        self.uploads = DbHelper(db, 'images')
        self.users = DbHelper(db, 'users')
        self.bookmarks = DbHelper(db, 'bookmarks')
        # self.user_decks = DbHelper(db, 'decks')

    #formats data into upload format and returns filename, id
    def create_upload(self, user_id, file_extention):
        data =  {'user_id': user_id}
        id = self.uploads.add(data)
        filename = "img" + str(id) + file_extention
        image_data = {'id': id, 'filename':filename}
        return image_data

    def delete_upload(self, item_id):
        file = self.uploads.find(item_id)
        if os.path.isfile(file['path']):
            os.remove(file['path'])
        self.uploads.delete(item_id)

    #from array shaped string, format data into bookmark format
    def create_bookmark(self, user_id, cards):
        #in db % sign reperesents a string break
        s = "%"
        #cleans up array markers in string. then splits at comma
        string = cards
        for c in ["'", "[", "]"]:
            string = string.replace(c, "")
        strings_array = string.split(", ")
        #joins strings with break marker
        cards_string = s.join(strings_array)
        #sends data dict to db manager
        data = {'user_id':user_id, 'cards':cards_string}
        self.bookmarks.add(data)

    def read_bookmarks(self, bookmark):
        cards_array = cards.split("%")
