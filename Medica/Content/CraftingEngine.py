import Zero
import Events
import Property
import VectorMath

class Recipe:
    def __init__(self, Rewards, Components):
        self.Flags = None
        self.Rewards = Rewards
        self.Components = Components
    
    def setFlags(self, Flag, State):
        pass

class CraftingEngine:
    RecipeDocument = Property.TextBlock()
    
    def Initialize(self, initializer):
        self.Recipes = {}
        
        self.populateRecipes()
        self.printRecipes()
    
    def populateRecipes(self):
        recipeText = self.RecipeDocument.Text
        splitLines = recipeText.split("\n")
        self.Recipes = {}
        
        for line in splitLines:
            reward, recipe = line.split("=")
            reward = reward.strip()
            recipe = recipe.strip()
            
            
            
            rewards = self.parseItems(reward)
            components = self.parseItems(recipe)
            
            self.Recipes[reward] = Recipe(rewards, components)
    
    def parseItems(self, items):
        splitStrings = items.split(",")
        returner = {}
        
        for lines in splitStrings:
            splitted = lines.split(":")
            
            name = splitted[0]
            amount = None
            
            if len(splitted) > 1:
                amount = splitted[1]
            
            if amount:
                if isinstance(amount, int):
                    if amount <= 0:
                        amount = 1
                elif amount.isdigit():
                    myValue = int(amount.strip())
                    
                    if myValue <= 0:
                        myValue = 1
                    
                    amount = myValue
                elif amount.find("Flag"):
                    #if "Flag" is found then we need to ignore the flag
                    # and then set the names and amount accordingly
                    moreSplit = amount.split(":")
                    name = splitted[1].strip()
                    amount = self.stringToBool(splitted[2])
                    
                else:
                    compare = amount.capitalize()
                    if compare == "False" or compare == "True":
                        amount = bool(compare)
                    else:
                        amount = compare
            else:
                amount = 1
            
            name = name.strip()
            returner[name] = amount
        
        return returner
    
    def printRecipes(self):
        print("#############################")
        print("Crafting Recipes")
        for recipe in self.Recipes.keys():
            print("\tRecipe:", recipe)
            print("\t\tRewards:", self.Recipes[recipe].Rewards)
            
            print("\t\tComponents:")
            
            components = self.Recipes[recipe].Components
            
            for requirement in components.keys():
                print("\t\t\t{0}: x{1}".format(requirement, components[requirement]))
        print("#############################")
    
    def stringToBool(self, compare):
        return compare.capitalize() in ["True", "T", "Y"]

Zero.RegisterComponent("CraftingEngine", CraftingEngine)