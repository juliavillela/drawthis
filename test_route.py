from db.cards_picker import CardsPicker
from db.controller import TablesController


controller = TablesController('_en')
cards_picker = CardsPicker(controller)
# cards_picker.change_language('_pt')

for i in range(0, 6):
    cards_picker.change_level(i)
    print("------------")
    print("")

    print("lvl: " + str(cards_picker.level))

    cards_picker.pick()
    print(cards_picker.card)

    print("")
    print("------------")
    print("")
    print("")
