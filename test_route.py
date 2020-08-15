from database.tables_controller import TablesController

controller = TablesController(["nouns", "adjectives", "actions", "situations"])

print(controller.validation)
