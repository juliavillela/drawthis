from random import randint

class AltPicker:
    #dict where card name correspond to an array the length of avaiable levels
    #each value in array indicates if card should exist
    levels_chart = {
            #subjec values correspond to adjective draw since noun is always true
            "subject":[False,False,False],
            "complement":[False,True,False],
            "action":[False,False,True],
            "situation":[False,False,True]
            }

    def __init__ (self, controller):
        self.db = controller
        self.card = []
        self.level = 2

    def pick(self):
        self.card = []
        subject = self.get_random(['subjects'])
        self.card.append(subject['main'])
        if self.lvl('complement'):
            complement = self.get_random(['actions', 'situations'])
            self.card.append(complement['main'])
        if self.lvl('action'):
            action = self.get_random(['actions'])
            situation = self.get_random(['situations'])
            self.card.append(action['main'])
            self.card.append(situation['main'])
        return True

    #sets new value to level
    def change_level(self, new_level):
        self.level = int(new_level['lvl'])

    #in levels charts selects value corresponding to both card name and current level
    #returns boolean
    def lvl(self,card_name):
        return self.levels_chart[card_name][self.level]

    #calls for get_random function in db
    #returns row dict
    def get_random(self, table_name, filter=None):
        row = self.db.get_random(table_name, filter)
        return row

    def details(self):
        me = {}
        me['deck'] = self.db.deck_id
        me['level'] = self.level
        me['max-level'] = 2
        me['language'] = None
        me['action'] = "/custom/" + self.db.deck_id + "/_" 
        return me
