from random import randint

class CardsPicker:
    def __init__ (self, controller):
        self.db = controller
        self.card = []
        self.level = 0

    #asks db to load new language
    def change_language(self, new_language):
        self.db.load(new_language)

    #sets new value to level
    def change_level(self, new_level):
        self.level = int(new_level);

    def draw_cards(self):
        self.card = []
        self.subject_card()
        self.complement_card()
        return self.card

    def subject_card(self):
        if self.level < 2:
            self.card.append(self.subject())
        else:
            self.card.append(self.subject(True))

    def complement_card(self):
        if self.level == 0:
            pass
        elif self.level in range(1,3):
            #get random from either actions or situations except where type = time
            complement = self.get_random(['actions', 'situations'], {'type':'time'})
            for col in complement:
                if col in ['action', 'situation']:
                    self.card.append(complement[col])
                    break
        else:
            self.card.append(self.action())
            self.card.append(self.situation())
        if level > 3:
            pass


    def subject(self, adj=False):
        noun = self.get_random(['nouns'])
        sentence = [noun['article'], noun['noun']]

        if adj:
            adjective = self.adjective(noun)
            sentence = self.format_subject(noun, adjective)

        s = " "
        return s.join(sentence)

    #returns adjective dict
    def adjective(self, noun):
        #sets filter to filter out all rows where required column in empty
        filter = {noun['require']: None}
        adjective = self.get_random(['adjectives'], filter)
        #returns a dict with required version of adjective + position
        return {'adjective': adjective[noun['require']],
            'position': adjective['position']}

    #returns action string
    def action(self):
        action = self.get_random(['actions'])
        return action['action']

    #returns situation dict
    def situation(self, count=1):
        typesA = ['time', 'mood']
        typesB = ['place', 'atmosphere']
        if count > 1:
            #TBD
            pass
        else:
            situation = self.get_random(['situations'])
        return situation['situation']

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

    def get_random(self, table_name, filter=None):
        phrase = self.db.get_random(table_name, filter)
        return phrase
