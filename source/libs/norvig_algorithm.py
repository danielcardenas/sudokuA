import time

from algorithm import Algorithm

class NorvigAlgorithm(Algorithm):

    def __init__(self, sudoku_to_solve, character):
        """Constructor NorvigAlgorithm.

        Keyword arguments:
        sudoku_to_solve -- the string raw data of the sudoku to solve
        character -- the string character which represents the place to need
                     filled in the sudoku
        
        """   
        super(NorvigAlgorithm, self).__init__(sudoku_to_solve, character)
        # the possible values that the spaces in suduku could contain
        self.digits   = '123456789'
        # the rows that the suduku grid will contain from A to I
        self.rows     = 'ABCDEFGHI'
        # the columns that the suduku grid will contain from 1 to 9
        self.cols     = self.digits
        # tuple each square into the suduku grid it will have 9 squares
        self.squares  = self.cross(self.rows, self.cols)
        # the list of units in the sudoku
        self.unitlist = ([self.cross(self.rows, c) for c in self.cols] +
                   [self.cross(r, self.cols) for r in self.rows] +
                   [self.cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') \
                                       for cs in ('123', '456', '789')])
        # the list of units in the sudoku
        self.units = dict((s, [u for u in self.unitlist if s in u])
                     for s in self.squares)
        # each square has 20 peers see http://norvig.com/sudoku.html 
        self.peers = dict((s, set(sum(self.units[s], []))-set([s]))
                     for s in self.squares)
        
        
    def cross(self, element_a, element_b):
        """Cross product of elements in element_a and elements in element_b.
           
           Keyword arguments:
           element_a -- matrix of elements into sudoku
           element_b -- matrix of elements into sudoku

        """

        return [a+b for a in element_a for b in element_b]


        ################ Search ################

    def solve_sudoku(self):
        """Returns the solution to sudoku using the Norvig Algorithm."""
        if self.sudoku_data_is_valid() == False:
            raise Exception("The sudoku input is incorrect")
        sudoku_to_solve = "Grid\n" + self.sudoku_to_solve
        self.start_tim = time.clock()
        res = self.search(self.parse_grid(sudoku_to_solve))
        self.end_time = time.clock()
        return res

    def search(self, sudoku_values):
        """Searches the solution to the sudoku using depth-first search and
           propagation, try all possible values. Return a dictionary with the
           solution to sudoku or False in case it could not be solved

        Keyword arguments:
        sudoku_values -- the dictionary list which contain the sudoku data

        """  
        if sudoku_values is False:
            return False  # Failed earlier
        if all(len(sudoku_values[s]) == 1 for s in self.squares):
            return sudoku_values  # Solved!
        # Chose the unfilled square s with the fewest possibilities
        n, s = min((len(sudoku_values[s]), s) for s in self.squares \
                                              if len(sudoku_values[s]) > 1)
        return self.some(self.search(self.assign(sudoku_values.copy(), s, d))
                for d in sudoku_values[s])

    ################ Parse a Grid ################

    def parse_grid(self, grid_sudoku):
        """Convert grid sudoku to a dict of possible values, {square: digits},
           or return False if a contradiction is detected

        Keyword arguments:
        grid_sudoku -- the grid of the sudoku to solve 
        
        """
        # To start, every square can be any digit; then assign values from the grid.
        values = dict((s, self.digits) for s in self.squares)
        for s,d in self.grid_values(grid_sudoku).items():
            if d in self.digits and not self.assign(values, s, d):
                return False # Fail if we can't assign d to square s.
        return values

    def grid_values(self, grid_sudoku):
        """Convert grid into a dict of {square: char} with a specified
           character for empties places

        Keyword arguments:
        grid_sudoku -- the grid of the sudoku to solve 
        
        """
        chars = [c for c in grid_sudoku if c in self.digits or c in self.character]
        return dict(zip(self.squares, chars))

    ################ Constraint Propagation ################

    def assign(self, values_sudoku, key_sudoku_dic, value_to_replace):
        """Eliminate all the other values (except d) from values[s] and
           propagate Return dictionary of sudoku to solve, except return
           False if a contradiction is detected.

        Keyword arguments:
        values_sudoku -- the dictionary of the sudoku to solve
        key_sudoku_dic --  the key of the dictionay of the sudoku to solve
        value_to_replace --  the value which will be replaced in a key of the dictionary
              of the sudoku

        """
        other_values = values_sudoku[key_sudoku_dic].replace(value_to_replace, '')
        if all(self.eliminate(values_sudoku, key_sudoku_dic, d2) for d2 in other_values):
            return values_sudoku
        else:
            return False

    def eliminate(self, values_sudoku, key_sudoku_dic, value_to_replace):
        """Eliminate d from values[s]; propagate when values or places <= 2.
           Return dictionary of sudoku to solve, except return False if a
           contradiction is detected..

        Keyword arguments:
        values_sudoku -- the dictionary of the sudoku to solve
        key_sudoku_dic --  the key of the dictionay of the sudoku to solve
        value_to_replace --  the value to eliminate in the dictionary

        """
        if value_to_replace not in values_sudoku[key_sudoku_dic]:
            return values_sudoku  # already eliminated
        values_sudoku[key_sudoku_dic] = values_sudoku[key_sudoku_dic].\
                                        replace(value_to_replace,'')
        # (1) if a square s is reduced to one value d2, then eliminate d2 from the peers.
        if len(values_sudoku[key_sudoku_dic]) == 0:
            return False  # Contradiction: removed last value
        elif len(values_sudoku[key_sudoku_dic]) == 1:
            d2 = values_sudoku[key_sudoku_dic]
            if not all(self.eliminate(values_sudoku, s2, d2)\
                        for s2 in self.peers[key_sudoku_dic]):
                return False
        # (2) if a unit u is reduced to only one place for a value d, then put it there.
        for u in self.units[key_sudoku_dic]:
            dplaces = [key_sudoku_dic for key_sudoku_dic in u\
                                      if value_to_replace in \
                                      values_sudoku[key_sudoku_dic]]
            if len(dplaces) == 0:
                return False # Contradiction: no place for this value
            elif len(dplaces) == 1:
                # d can only be in one place in unit; assign it there
                if not self.assign(values_sudoku, dplaces[0], value_to_replace):
                    return False
        return values_sudoku

    ################ Utilities ################

    def some(self, seq):
        """Return some element of seq that is true.

        Keyword arguments:
        seq -- the sequence of values to look for a true value

        """
        for e in seq:
            if e:
                return e
        return False

    ################ Validate input ################

    def sudoku_data_is_valid(self):
        """Verifies if the sudoku to solve contains the valid data."""
        chars = [c for c in self.sudoku_to_solve if c in self.digits\
                or c in self.character]
        if len(chars) != 81:
            return False
        else:
            return True


