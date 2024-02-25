__version__ = "0.1.0"
__author__ = 'ShiYuan Fan'

class Tree: # This the 'trunk'(base) of all the Fruits and Branches
    """Create a decision tree"""
    def __init__(self, name:str):
        self.name = name # A Tree MUST has a name
        self.father = None  # Tree(Trunk) has no father
        self.open = True  # Tree(Trunk) is always open
        self.branches = []
        self.fruits = []

    def add_branch(self, father, condition:tuple, name:str=''):
        """Create a decision branch"""
        if father.__class__ != Branch and father.__class__ != Tree:
            raise TypeError("Incorrect 'father' augument for Branch. It should be Tree or Branch.")
        new_branch = Branch(father=father, condition=condition, name=name)
        self.branches.append(new_branch)
        return new_branch # Return a object

    def add_fruit(self, father, value=None, command=None, name:str=''):
        """Create a result(fruit) connected to a branch"""
        if father.__class__ != Branch:
            raise TypeError("Incorrect 'father' augument for Fruit. It should be Branch.")
        new_fruit = Fruit(father=father, value=value, name=name, command=command)
        self.fruits.append(new_fruit)
        return new_fruit # Return a object

    def run(self):
        """Simulate the decision tree, and show the results(fruits) of the tree"""
        for branch in self.branches:
            branch.run()
        for fruit in self.fruits:
            fruit.run()

        print()
        for fruit in self.fruits:
            if fruit.open == False:
                print(f"{fruit.name} : X ({fruit.current_value})")
            if fruit.open == True:
                print(f"{fruit.name} : √ ({fruit.current_value})")

        print("\nSimulation complete")

class Child_Of_Tree(): # Both Branch and Fruit are the children of the tree
    def __init__(self):
        pass
    
    def find_trunk(self): 
        father = self.father
        while True: # Father's father's father.... is always the Trunk(Tree)
            if father.father == None:
                return father
            father = father.father
                    
class Branch(Child_Of_Tree): # !: User should not be allowed to use this class, only create branch by Tree.add_branch
    def __init__(self, father, condition:tuple, name:str=''):
        self.father = father  # Branch or Tree
        self.trunk = self.find_trunk()
        self.open = False # Branch is open or close. False for close, True for open.
        if self.father.__class__ != Branch and self.father.__class__ != Tree:
            raise TypeError("Incorrect 'father' augument for Branch. It should be Tree or Branch.")
        
        # Give default name to the branch if user doesn't set
        if name == '':
            __ = len(self.trunk.branches)
            self.name = f"Branch {__}"
        else:
            self.name = name

        self.condition = condition

        self.detect_target = self.condition[0]
        self.operator = self.condition[1]
        self.expected_value = self.condition[2]
        number_types = [int, float, complex, list, tuple, bool]
        
        # Because of different inputs types, so we need different ways to process them.
        # Divide inputs to two types: number(bool) or string
        # Seems a little bit ugly
        if type(self.detect_target) in number_types:
            if type(self.expected_value) in number_types:
                self.condition_statement = f"{self.detect_target} {self.operator} {self.expected_value}"
            else:
                self.condition_statement = f"{self.detect_target} {self.operator} '{self.expected_value}'"
        else:
            if type(self.expected_value) in number_types:
                self.condition_statement = f"'{self.detect_target}' {self.operator} {self.expected_value}"
            else:
                self.condition_statement = f"'{self.detect_target}' {self.operator} '{self.expected_value}'"
    
        try:
            eval(self.condition_statement)
        except SyntaxError:
            raise ValueError("Incorrect condition statement for Branch.")

    def run(self): # User should not to be able to use this function
        if eval(self.condition_statement):
            if self.father.open == True:
                self.open = True

# Explanation for Fruit(class):
# Fruit can be added both on the end of the branch and between two branches
# Like this: (The following two are OK and legal)
# Example1: Trunk -- Branch1(Fruit1) -- Branch2 -- Fruit2 / Example2:  Trunk -- Branch1 -- Branch2(Fruit1)
# Fruit only represents a result. For Example1, if only Branch1 is activated but Branch2 not, Fruit1 will be activated. Branch2 doesn't connect to Fruit1, it actually connects to Branch1.

class Fruit(Child_Of_Tree): # Fruit represents result
    def __init__(self, father, value=None, command=None, name:str=""):
        self.father = father  # Branch
        self.trunk = self.find_trunk()
        if not callable(command) and command != None:
            raise TypeError("The input for 'command' parameter of Fruit must be a function.")
        self.command = command # Like a tkinter button. If the fruit is activated, command(a function) will run.
        self.open = False
        if name == '':
            __ = len(self.trunk.fruits)
            self.name = f"Fruit {__}"
        else:
            self.name = name
        if self.father.__class__ != Branch and self.father.__class__ != Tree:
            raise TypeError("Incorrect 'father' augument for Fruit. It should be Tree or Branch.")
        self.current_value = None
        self.expected_value = value

    def run(self):
        if self.father.open == True:
            self.open = True
            self.current_value = self.expected_value
            if self.command != None:
                self.command()