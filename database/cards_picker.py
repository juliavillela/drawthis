from random import randint

class CardsPicker:

    def __init__ (self, language, tables_controller):
        self.db = tables_controller
        print(self.db)
        self.card = []
        self.level = 0
        self.db.load(language)

    def change_language(self, new_language):
        self.db.load(new_language)

    def change_level(self, new_level):
        self.level = int(new_level);

    def draw_cards(self):
        self.card = []
        print(self.card)
        self.subject_card()
        print(self.card)
        self.complement_card()
        print(self.card)
        return self.card

    def subject_card(self):
        if self.level < 2:
            print(self.subject())
            self.card.append(self.subject())
        else:
            self.card.append(self.subject(True))

    def complement_card(self):
        if self.level == 0:
            pass
        elif self.level in range(1,3):
            if randint(0,1) == 0:
                self.card.append(self.action())
            else:
                self.card.append(self.situation())
        elif self.level == 3:
            self.card.append(self.action())
            self.card.append(self.situation())
        else:
            pass

    def subject(self, adj=False):
        noun = self.get_random('nouns')
        print(noun)
        sentence = []
        s = " "
        sentence.append(noun['article'])
        if adj:
            adjective = self.get_random('adjectives')
            if int(adjective['position']) == 2:
                sentence.append(noun['subject'])
                sentence.append(adjective['adjective'])
                return s.join(sentence)
            else:
                sentence.append(adjective['adjective'])
        sentence.append(noun['subject'])
        return s.join(sentence)

    def action(self):
        action = self.get_random('actions')
        return action['action']

    def situation(self, count=1):
        typesA = ['time', 'mood']
        typesB = ['place', 'atmosphere']
        if count > 1:
            situation = self.get_random('situations', "WHERE type = place")
        else:
            situation = self.get_random('situations')
        return situation['situation']

    def get_random(self, table_name):
        phrase = self.db.get_random(table_name)
        return phrase
