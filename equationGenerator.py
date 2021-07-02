"""
Equation Generator

This class will generate a random equation given a difficulty. This class only
makes one random equation. To generate a new equation with new numbers and
answers, you'd have to create a whole new Equation object. 
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
        self.var_x = random.randrange(self.range)
        self.var_y = random.randrange(self.range)
        self.answer = None
        self.problem = None # will be used in later methods
        
        # no negative answers for difficulties 2 and below 
        if self.isAddition == False and self.canBeNegative == False:
            # if the second is higher than the first, just swamp 'em
            if self.var_y > self.var_x:
                temp = self.var_x
                self.var_x = self.var_y
                self.var_y = temp

        # find the answer, depending on addition/subtraction 
        if self.isAddition:
            self.answer = self.var_x + self.var_y
        else:
            self.answer = self.var_x - self.var_y


    """
    Returns a string containing the unsolved problem.
    """
    def equationUnsolved(self):
        # start with the first variable 
        self.problem = str(self.var_x)

        # add on the operand 
        if self.isAddition:
            self.problem += " + "
        else:
            self.problem += " - "

        # add the second variable and finish with the equals sign, then return
        self.problem += str(self.var_y) + " = "
        return self.problem


    """
    Returns a string containing the solved problem.
    """
    def equationSolved(self):
        # just add the answer to the unsolved version and return it
        self.problem = self.equationUnsolved() + str(self.answer)
        return self.problem


    """
    Returns a set of two incorrect answers chosen from a few possible ones.
    This MUST be called after the object is created. Example:

    x = Equation(0)
    test_set = set()
    x.setIncorrectAnswers(test_set)

    Now test_set has two incorrect choices. 
    """
    def setIncorrectAnswers(self, setPossible):
        # initialize two incorrect answers 
        incorrect_a = 0
        incorrect_b = 0

        # randomly pick incorrect_a's value 
        if random.randrange(0, 1):
            # this incorrect answer is one away from the actual one 
            if self.canBeNegative == False and self.answer - 1 <= 0:
                incorrect_a = (self.answer + 1)
            else:
                if random.randrange(0, 1):
                    incorrect_a = (self.answer + 1)
                else:
                    incorrect_a = (self.answer - 1)
        else:
            # this incorrect answer uses the wrong operator 
            if self.isAddition:
                incorrect_a = (self.var_x - self.var_y)
            else:
                incorrect_a = (self.var_x + self.var_y)

        # incorrect_b is a random number close to the answer
        incorrect_b = random.randrange(self.answer - 5, self.answer + 5)
        while incorrect_b == self.answer:
            incorrect_b = random.randrange(self.answer - 5, self.answer + 5)

        # add these two numbers to the set; remember, 
        # the correct answer itself is not in this set!
        setPossible.add(incorrect_a)
        setPossible.add(incorrect_b)
