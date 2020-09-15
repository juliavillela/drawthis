import os

# from db.controller import TablesController
# from db.cards_picker import CardsPicker
from db.db_helper import DbHelper
from db.uploads import Uploads
from db.users import Users
from db.deck import Deck
from db.alt_picker import AltPicker

from random import randint

from format import str_arr, join, split, cards_imd

class Controller:

    def __init__(self, db):
        # self.main_db = TablesController(db, "_en")
        # self.draw = CardsPicker(self.main_db)
        self.db = db
        self.uploads = Uploads(db, 'uploads')
        self.avatars = DbHelper(db, 'avatars')
        self.users = Users(db, 'users')
        self.bookmarks = DbHelper(db, 'bookmarks')
        self.decks = DbHelper(db, 'decks')
        self.alt_deck = Deck(db)
        self.alt_picker = AltPicker(self.alt_deck)


    def create_user(self, data):
        data["type"] = "user"
        # avatars = self.avatars.list()
        # id = randint(0, len(avatars)-1)
        # data["avatar_id"] = avatars[id]['id']
        data["avatar_id"] = self.pick_avatar()
        user_id = self.users.add(data)
        return user_id

    def pick_avatar(self):
        avatars = self.avatars.list()
        id = randint(0, len(avatars)-1)
        return avatars[id]['id']

    #formats data into upload format and returns filename, id
    def create_upload(self, user_id, file_extention):
        data =  {'user_id': user_id}
        id = self.uploads.add(data)
        filename = "img" + str(id) + file_extention
        image_data = {'id': id, 'filename':filename}
        return image_data

    #from array shaped string, format data into bookmark format
    def create_bookmark(self, user_id, cards):
        cards_string = join(str_arr(cards))
        #sends data dict to db manager
        data = {'user_id':user_id, 'cards':cards_string}
        self.bookmarks.add(data)

    def delete_upload(self, item_id):
        file = self.uploads.find(item_id)[0]
        if os.path.isfile(file['path']):
            os.remove(file['path'])
        self.uploads.delete(item_id)

    #formats cards and sends to db
    def update_upload(self, image_id, imd):
        data = {}
        data['cards'] = cards_imd(imd)
        print("-----in update print data:")
        print(data)
        self.uploads.update(image_id, data)

    def update_user_avatar(self, user_id):
        data={}
        data['avatar_id'] = self.pick_avatar()
        self.users.update(user_id, data)

    def read(self, data):
        parse = ['cards']
        for row in data:
            for col in row:
                if col in parse:
                    row[col] = split(row[col])
        print("-----in read print data:")
        print(data)
        return data

    def user_bookmarks(self, user_id):
        all = self.bookmarks.all_from_user(user_id)
        for item in all:
            item['cards'] = split(item['cards'])
        return all

    def custom_deck(self, user_id, deck_id):
        if type(deck_id) != str:
            deck_id = str(deck_id)
        self.alt_deck.load(deck_id)

    def delete_deck(self, deck_id):
        self.alt_deck.clear_deck_data(deck_id)
        self.decks.delete(deck_id)
