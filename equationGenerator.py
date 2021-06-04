"""
Equation Generator

This class will generate a random equation given a difficulty. This class only
makes one random equation. To generate another one, you need to call another
object of this class. In a loop, for example, you'd have to create another 
Equation to have a new randomized equation. 
"""

import random

class Equation:
    def __init__(self, difficulty):
        """
        Sets up difficulty of the equation. 
        """
        # difficulty determines range and operation
        self.range = 10
        self.isAddition = True
        self.canBeNegative = False

        # just addition, numbers 10 or less
        if difficulty == 0:
            pass

        # addition or subtraction, numbers 10 or less
        if difficulty == 1:
            # changes to subtraction if true 
            if random.randrange(2):
                self.isAddition = False

        # addition or subtraction, numbers over 10
        if difficulty == 2:
            # broadens range
            self.range = 20

            # addition or subtraction? 
            if random.randrange(2):
                self.isAddition = False

        # addition/subtraction, numbers less than 10, answers can be negative
        if difficulty == 3:
            if random.randrange(2):
                self.isAddition = False
                self.canBeNegative = True

        # addition/subtraction, numbers less than 20, answers can be negative 
        if difficulty == 4:
            self.range = 20
            if random.randrange(2):
                self.isAddition = False
                self.canBeNegative = True

        """
        Generates the equation based on difficulty.  
        """
        # initialize the operands 
        self.a = random.randrange(self.range)
        self.b = random.randrange(self.range)
        self.c = None
        self.problem = None # will be used in later methods
        
        # no negative answers for difficulties 2 and below 
        if self.isAddition == False and self.canBeNegative == False:
            # if the second is higher than the first, just swamp 'em
            if self.b > self.a:
                temp = self.a
                self.a = self.b
                self.b = temp

        # find the answer, depending on addition/subtraction 
        if self.isAddition:
            self.c = self.a + self.b
        else:
            self.c = self.a - self.b

    """
    Returns a string containing the unsolved problem.
    """
    def equationUnsolved(self):
        # start with the first operand 
        self.problem = str(self.a)

        # add on the operand 
        if self.isAddition:
            self.problem += " + "
        else:
            self.problem += " - "

        # finish with the equals sign and return it 
        self.problem += str(self.b) + " = "
        return self.problem

    """
    Returns a string containing the solved problem.
    """
    def equationSolved(self):
        # just add the answer to the unsolved version and return it
        self.problem = self.equationUnsolved() + str(self.c)
        return self.problem

    """
    Returns a set with the correct and incorrect answers together.
    """
    def setAnswers(self, setPossible):
        # add the correct answer
        setPossible.add(self.c)

        # now set up three incorrect answers

        # first is one that's close to the original answer
        if self.canBeNegative == False and self.c - 1 <= 0:
            setPossible.add(self.c + 1)
        else:
            if random.randrange(0, 1):
                setPossible.add(self.c + 1)
            else:
                setPossible.add(self.c - 1)

        # second is one with the wrong operator 
        if self.isAddition:
            setPossible.add(self.a - self.b)
        else:
            setPossible.add(self.a + self.b)

        # third is a random number
        third = random.randrange(self.range)
        while third == self.c:
            third = random.randrange(self.range)
        setPossible.add(third)

"""
EXAMPLE USAGE
"""

# this will loop four times
for i in range(4):

    # set up random equation and some possible answers
    x = Equation(4)
    setPossibleAnswers = set()
    x.setAnswers(setPossibleAnswers)

    # display the equation to be solved
    print("\nWhich is the answer?\n")
    print(x.equationUnsolved(), "\n")

    # display some choices
    for choice in setPossibleAnswers:
        print(choice)

    # get user input
    userChoice = input(" > ")

    # check user input 
    if int(userChoice) == x.c:
        print("\nCorrect!")
    else:
        print("\nSorry, that's incorrect. The answer was " + str(x.c) + ".")
        print(x.equationSolved())