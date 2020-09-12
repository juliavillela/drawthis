from random import randint

class CardsPicker:
    #a dict for storing pick name and rows picked
    pick = {}

    #dict where card name correspond to an array the length of avaiable levels
    #each value in array indicates if card should exist
    levels_chart = {
            #subjec values correspond to adjective draw since noun is always true
            "subject":[False,False,True,True,True,True],
            "complement":[False,True,True,False,False,False],
            "action":[False,False,False,True,True,True],
            "situation":[False,False,False,True,True,True],
            "situation_2":[False,False,False,False,True,True],
            "instruction":[False,False,False,False,False,True]
            }
    level_range = range(0,5)

    def __init__ (self, controller):
        self.db = controller
        self.card = []
        self.instruction = False;
        self.level = 3
        self.instruction_card = []
        # array of dicts: keys identify the picks by name
        # values is an array with 2 items: table names and filter

    #asks db to load new language
    def change_language(self, new_language):
        self.db.load(new_language)

    #sets new value to level
    def change_level(self, new_level):
        if int(new_level) in self.level_range:
            self.level = int(new_level)
        else:
            self.level = 3

    def pick(self):
        self.card = []
        #returns string. noun only if level is false, noun and adjective if level is true
        subject_card = self.subject(self.lvl('subject'))
        self.card.append(subject_card)

        #return dict of row if level is true, none if level is false
        complement = self.get_random(['actions', 'situations'], {'type':'time'}) if self.lvl('complement') else None
        action = self.get_random(['actions']) if self.lvl('action') else None
        situation = self.get_random(['situations']) if self.lvl('situation') else None
        situation_2 = self.get_random(['situations'], {'type': situation['type']}) if self.lvl('situation_2') else None
        instruction = self.get_random(['instructions']) if self.lvl('instruction') else None

        #creates array cards to hold all picks
        cards = [complement, action, situation, situation_2, instruction]
        #names columns which should be extracte to show in view
        main_columns = ['action', 'situation', 'instructions']

        #returns string for each card that has content
        for card in cards:
            if card:
                for row in card:
                    if row in main_columns:
                        self.card.append(card[row])

        return self.card


    #selects noun and article, then calls for adjective selection(if required)
    #returns string
    def subject(self, has_adj):
        noun = self.get_random(['nouns'])
        sentence = [noun['article'], noun['noun']]

        if has_adj:
            adjective = self.adjective(noun)
            sentence = self.format_subject(noun, adjective)

        s = " "
        return s.join(sentence)

    #selects adjective according to noun and filters selected column
    #returns dict
    def adjective(self, noun):
        #sets filter to filter out all rows where required column in empty
        filter = {noun['require']: None}
        adjective = self.get_random(['adjectives'], filter)
        #returns a dict with required version of adjective + position
        return {'adjective': adjective[noun['require']],
            'position': adjective['position']}

    #formats noun, article and adjective in correct order and adjusts article
    #returns array of strings
    def format_subject(self, noun, adjective):
        vowels = ['a', 'e', 'i', 'o', 'u']
        sentence = []
        if adjective['position'] == 'after':
            sentence = [ noun['article'] , noun['noun'],
            adjective['adjective']]
        else:
            if noun['article'] in ['a', 'an']:
                if adjective['adjective'][0] in vowels:
                    noun['article'] = 'an'
                else:
                    noun['article'] = 'a'
            sentence = [ noun['article'] , adjective['adjective'], noun['noun'] ]

        return sentence

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
        me['deck'] = "default"
        me['level'] = self.level
        me['max-level'] = 4
        me['language'] = self.db.language
        me['action'] = "/"
        return me
