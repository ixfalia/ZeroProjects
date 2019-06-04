import Zero
import Events
import Property
import VectorMath

import Color

KeyItems = Property.DeclareEnum("KeyItems", ["Undefined Key", "Undefined Pendant"]);

items = ["Undefined Herb", "Salvia Leaf", "Kampur Sap", "Glacia Berry"]
ItemList = Property.DeclareEnum("ItemList", items)

categories = ["Mineral", "Fungal", "Plant", "Liquid", "Powder", "Bottle","Flower","Seed", "Crystal", "Berry", "Bag", "Mystery", "Entry"]
Categories = Property.DeclareEnum("Categories", categories)

entryTypes = ["Item", "Entry", "Character", "Location"]
EntryTypes = Property.DeclareEnum("EntryTypes", entryTypes)

class ItemsEnumerations:
    def Initialize(self, initializer):
        pass

Zero.RegisterComponent("ItemsEnumerations", ItemsEnumerations)