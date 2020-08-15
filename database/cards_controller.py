class CardsController:

    def __init__ (self, language, tables_controller):
        self.db = tables_controller
        self.cards = []
        self.db.load(language)

    def build_cards(self):
        _1 = self.card_1()
        _2 = self.get_random('actions')['action']
        _3 = self.get_random('situations')['situation']
        self.cards = [_1, _2, _3]
        return self.cards

    def card_1(self):
        noun = self.get_random('nouns')
        adjective = self.get_random('adjectives')
        sentence = []
        sentence.append(noun['article'])
        if int(adjective['position']) == 2:
            sentence.append(noun['subject'])
            sentence.append(adjective['adjective'])
        else:
            sentence.append(adjective['adjective'])
            sentence.append(noun['subject'])
        s = " "
        return s.join(sentence)

    def get_random(self, table_name, dependency=None):
        phrase = self.db.get_random(table_name)
        return phrase
