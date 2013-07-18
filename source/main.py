import os
import sys
import time
sys.path.append('libs/config')
sys.path.append('libs/handlers')
sys.path.append('libs/algorithms')
sys.path.append('libs/io')
sys.path.append('libs/generator')
from xml_config import XMLConfig
from norvig_algorithm import NorvigAlgorithm
from backtraking_algorithm import BacktrakingAlgorithm
from brute_force_algorithm import BruteForceAlgorithm
from export_sudoku import ExportSudoku
from algorithm import Algorithm
from import_data import ImportData
from sudoku_generator import SudokuGenerator
from sudoku_ui import SudokuUI

class Main():

    def __init__(self):
        self.configuration = XMLConfig()
        self.import_data = ImportData()    
        self.empty_spot_char = self.configuration.get_empty_spot_char()     
        self.export_sudoku = ExportSudoku()
        self.display_main_menu()
         
    def display_main_menu(self):
        """ Displays the Main Menu and validates the entered values for the required options """

        print self.logo()
        self.print_dictionary_list(self.main_menu_options())

        while True:   
            op_main_menu = raw_input("\nPlease enter a number: ")

            if op_main_menu == "1" or op_main_menu == "2" or op_main_menu == "3"\
                                   or op_main_menu == "4" or op_main_menu == "5":
                self.main_menu_options()[op_main_menu]
                break
            else: 
              print "Oops!  That was not a valid option number.  Try again...\n"
        self.execute_main_option(op_main_menu) 

    def logo(self):
        """ Displays the logo on the menu"""

        logo_str = " _____           _       _             ___\n" + \
                   "/  ___|         | |     | |           / _ \\\n" + \
                   "\ `--. _   _  __| | ___ | | ___   _  / /_\ \\\n" + \
                   " `--. \ | | |/ _` |/ _ \| |/ / | | | |  _  |\n" + \
                   "/\__/ / |_| | (_| | (_) |   <| |_| | | | | |\n" + \
                   "\____/ \__,_|\__,_|\___/|_|\_\\\\__,_| \_| |_/\n"
                                                                                       
        return logo_str
    
    def main_menu_options(self):
        """ Defines the 3 available options for the Sudoku Main Menu """

        main_menu_opts = {'1': 'Configure', '2': 'Solve Sudoku', '3': 'Generate Sudoku',\
                          '4': 'Play online!', '5': 'Exit'}
        return main_menu_opts    

    def execute_change_solve_option(self, op_solve_menu):
        """ Executes the Solve Menu for the selected option

            Keyword arguments:
            op_solve_menu -- takes one of the three options to select on the Main Menu
        """

        if op_solve_menu == "1":
            self.solve_sudoku_from_cmd("txt")
            
        if op_solve_menu == "2":
            self.solve_sudoku_from_file("txt")
            
        if op_solve_menu == "3":
            self.solve_sudoku_from_file("txt")

        if op_solve_menu == "4":
            self.display_main_menu()

    def solve_sudoku_from_cmd(self, type_file):
        """ Method used for solving the sudoku given the input by command line

            Keyword arguments:
            type_file -- stores the selected cmd option

        """
        
        cmd_sudoku = raw_input ('\nEnter the sudoku to solve in the same line without spaces or'
                                'commas, it should have 81 numbers as the following example:\n0'
                                '03020600900305001001806400008102900700000008006708200002609500'
                                '800203009005010300\n')

        print "\nSolution:\n"
        sudoku_matrix = self.import_data.read_sudoku_data_from_line(cmd_sudoku)
        self.export_sudoku_to(sudoku_matrix, type_file)        
        self.display_main_menu()

    def export_sudoku_to(self, sudoku_matrix, type_file):
        """ Method used for exporting the solved sudoku to the default "results" path

            Keyword arguments:
            sudoku_matrix -- stores the sudoku on the valid sudoku matrix to solve
            type_file -- stores the selected file type; file or cmd

        """

        path = "../results/"
        algoritms = self.create_algorith_to_solve_sudoku(sudoku_matrix, self.empty_spot_char)        
        for algoritm_to_solve in algoritms:
            sudoku_solved = algoritm_to_solve.solve_sudoku()        
            if sudoku_solved != []:
                export_to = self.configuration.get_output_type()                
                if  export_to == 'file':
                    self.export_file(algoritm_to_solve, type_file, sudoku_solved, path)
                else:
                    self.export_sudoku.export_sudoku(sudoku_solved, "cmd line", "", "")
            else:
                print "\nInvalid sudoku, it cannot be solved!\n" 

    def file_exists(self):
        """ Method used for verifying whether the entered file exists or not """

        result = ""
        path = "../inputs/"
        while True :
            file_name = raw_input('\nEnter the name of the file to solve or enter quit to exit: ')
            file_txt = path + "\\" + file_name
            if os.path.exists(file_txt):
                result = file_txt
                break
            elif file_name == "quit":
                break
            else:
                print "\nThe file provided does not exists, please try again\n"
        return result

    def solve_sudoku_from_file(self, type_file):
        """ Method used for solving the sudoku given a file

            Keyword arguments:            
            type_file -- stores the selected file type, it can be a txt or csv file

        """ 

        file_ext = self.file_exists()
        
        if file_ext != "":            
            sudoku_matrix = self.import_data.read_sudoku_data_from_file(file_ext)            
            self.export_sudoku_to(sudoku_matrix, type_file)              
            #self.display_main_menu()            
        #else:            
        self.display_solve_menu()

    def export_file(self, algoritm_to_solve, type_file, sudoku_solved, path):
        """ Method used for create the solved sudoku in a file on the default "results" path

            Keyword arguments:
            algoritm_to_solve -- the selected algorithm to solve the sudoku           
            type_file -- stores the selected file type; file or cmd
            sudoku_solved -- sores the solved sudoku
            path -- stores the default "results" path for the solutions

        """ 

        file_name = 'sudoku_solved_' + algoritm_to_solve.__class__.__name__ + "_" + \
                    str(algoritm_to_solve.get_time()) + "_" + time.strftime("%Y-%m-%dT%H-%M-%S",
                     time.localtime(time.time())) + "." + type_file  
        if self.export_sudoku.export_sudoku(sudoku_solved, type_file, path, file_name) :
            print "\nThe file was created successfully\n"
        else:
            print "\nThere was a error, the file couldn't be created\n"

    def create_algorith_to_solve_sudoku(self, sudoku_matrix, empty_character):
        """ Method used for create the algorithm to solve given the expected sudoku matrix 
            and empty character
            
            Keyword arguments:
            sudoku_matrix -- stores the sudoku in the valid matrix ready to be solved
            empty_character -- stores the selected character for the empty spots 

        """
         
        algorithm_selected = self.configuration.get_algorithm()
        algoritms = []
        for i in range(0, len(sudoku_matrix)):
            algoritm_to_solve = Algorithm(sudoku_matrix[i][0], empty_character)
            if algorithm_selected == 'norvig':
                algoritm_to_solve = NorvigAlgorithm(sudoku_matrix[i][0], empty_character)                
            elif algorithm_selected == 'backtracking':
                algoritm_to_solve = BacktrakingAlgorithm(sudoku_matrix[i][0], empty_character)
            elif algorithm_selected == 'brute force':
                algoritm_to_solve =  BruteForceAlgorithm(sudoku_matrix[i][0], empty_character)
            algoritms.append(algoritm_to_solve)
        return algoritms
                
    def display_solve_menu(self):
        """ Displays/validates the selected options for solving the sudoku using one of the 
            three valid input types
            
        """ 

        self.print_dictionary_list(self.change_solve_menu_options(), "--- Solve Sudoku Menu ---")

        while True:   
            solve_opts = raw_input("\nPlease enter a number: ")

            if solve_opts == "1" or solve_opts == "2" or solve_opts == "3" or solve_opts == "4":
                self.change_solve_menu_options()[solve_opts]
                break
            else:
              print "\nOops!  That was not a valid option number.  Try again...\n" 
        self.execute_change_solve_option(solve_opts)

    def change_solve_menu_options(self):
        """ Defines the 3 available options for the inputs type for solving the sudoku """

        solve_opts = {'1': 'Solve sudoku entered by command line', 
                      '2': 'Solve sudoku from a txt file', '3': 'Solve sudoku from a csv file',
                      '4': 'Back'}   

        return solve_opts

    def conf_menu_options(self):
        """ Defines the 3 available options for the: "1 . Configure" option """

        conf_opts = {'1': 'Change Output format', '2': 'Change Level',
                     '3': 'Change Algorithm to use', '4': 'Change empty spot character', '5': 'Back'}

        return conf_opts
    
    def execute_main_option(self, op_main_menu):
        """ Executes the Main Menu for the selected option

            Keyword arguments:
            op_main_menu -- takes one of the four options to select on the Main Menu
        """

        if op_main_menu == "1":
            self.display_configure_menu()

        if op_main_menu == "2":
            self.display_solve_menu()              
                        
        if op_main_menu == "3":
            self.display_generate_sudoku_menu()

        if op_main_menu == "4":
            SudokuUI()

        if op_main_menu == "5":
            print "Good bye!"

    def execute_conf_option(self, conf_opts):
        """ Executes the selected option on the "1 . Configure" option 

            Keyword arguments:
            conf_opts -- takes one of the four options available in the option: "1 . Configure"  
        """

        if conf_opts == "1":
            self.display_output_type_menu()

        if conf_opts == "2":
            self.display_level_algorithm_menu()

        if conf_opts == "3":
            self.display_algorithm_menu()

        if conf_opts == "4":
            self.execute_change_empty_spot() 

        if conf_opts == "5":
            self.display_main_menu()

    def execute_change_empty_spot(self):
        """ Method that changes the character used as empty spot """

        empty_spot_char = str(raw_input('Enter a new character used as empty spot or'
                                        ' enter <quit> to go back menu: '))
                            
        if empty_spot_char >= '1' and empty_spot_char <= '9':
            print "\nInvalid empty spot character, please don't use numbers from 1 to 9"

        elif empty_spot_char == ',':
            print "\nInvalid empty spot character, please don't use the comma (,) character"
        
        elif len(empty_spot_char) == 1:
            print "\n", self.configuration.modify_empty_spot_char(empty_spot_char)

        elif empty_spot_char.lower() == 'quit':
            print  "\nDefault empty spot char will be used: "\
                                                    + self.configuration.get_empty_spot_char()

        else:
            print "\nInvalid empty spot character, please use only one character"

        self.display_configure_menu()

    def execute_change_level_option(self, level_opts):
        """ Changes the complexity level for create or solve the sudoku 

            Keyword arguments:
            level_opts -- takes one of the three options for the complexity level
        """

        if level_opts == "1":
            # save Easy level 
            print "\n", self.configuration.modify_complexity('Easy')
            
        if level_opts == "2":
            # save Medium level
            print "\n", self.configuration.modify_complexity('Medium')

        if level_opts == "3":
            # save Hard level
            print "\n", self.configuration.modify_complexity('Hard')

        self.execute_change_algorithm_option('4')

    def execute_change_algorithm_option(self, chng_algorit):
        """ Changes the Algorithm used for create or solve the sudoku 

            Keyword arguments:
            chng_algorit -- takes one of the three options for changing the Algorithm to use
        """ 

        if chng_algorit == "1":
            # save Norvig algorithm              
            print "\n", self.configuration.modify_algorithm('Norvig')

        if chng_algorit == "2":
            # save Backtraking algorithm            
            print "\n", self.configuration.modify_algorithm('Backtracking')

        if chng_algorit == "3":
            # save Brute Force algorithm            
            print "\n", self.configuration.modify_algorithm("brute force")           

        self.display_configure_menu()

    def execute_change_output_option(self, output_opts): 
        """ Changes the output format for the solved the sudoku 

            Keyword arguments:
            output_opts -- takes one of the two options, 
                           solved sudoku could be displayed in console, or in a file
        """ 
        if output_opts == "1":
            # display solved sudoku in console            
            print "\n", self.configuration.modify_output_type('console')            

        if output_opts == "2":
            # save solved sudoku in a file            
            print "\n", self.configuration.modify_output_type('file')       

        self.display_configure_menu()

    def execute_generate_sudoku_option(self, generate_opts): 
        """Executes the action selected by the user save sudoku on TXT file or diplay in console

            Keyword arguments:
            generate_opts -- takes one of the two options, 
                             generated sudoku could be displayed in console, or in a file
        """ 
        if generate_opts in ['1', '2']:
            complexity = self.configuration.get_complexity()
            min_holes = self.configuration.get_min_holes_by_complexity(complexity)
            max_holes = self.configuration.get_max_holes_by_complexity(complexity)
            empty_spot_char = self.configuration.get_empty_spot_char()
            sudoku_generator = SudokuGenerator()
            sudoku_generator.generate_sudoku_pattern_by_complexity(min_holes, max_holes, 
                                                                   empty_spot_char)

        if generate_opts == "1":
            # save sudoku generated in file
            name_sudoku = "sudoku_generated_" + time.strftime("%Y-%m-%dT%H-%M-%S",\
                                                time.localtime(time.time())) + ".txt"

            if self.export_sudoku.export_sudoku(sudoku_generator.sudoku_pattern,
                                                 'txt', "../results/", name_sudoku) is True:
                print "\nSudoku was saved to: '",name_sudoku,"'"                
                self.display_main_menu()

            else:
                print "\nFailed to save in TXT file. Try again...!"                
                self.display_generate_sudoku_menu()              

        if generate_opts == "2":
            # display generate sudoku in console
            print "\nGenerated Sudoku:\n"
            self.export_sudoku.export_sudoku(sudoku_generator.sudoku_pattern, 'cmd line', '', '')
            self.display_main_menu()
            
        if generate_opts == "3":
            self.display_main_menu()
            
    def display_algorithm_menu(self):
        """ Displays/validates the selected options for the option: 
                              3 . Change Algorithm to solve sudokus                              
        """ 

        self.print_dictionary_list(self.change_algorithm_menu_options(), "--- Change Algorithm Menu ---")

        while True:   
            algorit_opts = raw_input("\nPlease enter a number: ")
            
            if algorit_opts == "1" or algorit_opts == "2" or algorit_opts == "3"\
                                   or algorit_opts == "4":
                self.change_algorithm_menu_options()[algorit_opts]
                break
            else:
              print "Oops!  That was not a valid option number.  Try again..." 
        self.execute_change_algorithm_option(algorit_opts)    
    
    def display_level_algorithm_menu(self):
        """ Displays and validates the selected options for the option "2 . Change level" """ 

        self.print_dictionary_list(self.change_level_menu_options(), "--- Change Complexity Level Menu ---")

        while True:   
            level_opts = raw_input("\nPlease enter a number: ")
            
            if level_opts == "1" or level_opts == "2" or level_opts == "3" or level_opts == "4":
                self.change_level_menu_options()[level_opts]
                break
            else:
              print "Oops!  That was not a valid option number.  Try again..." 
        self.execute_change_level_option(level_opts)

    def display_output_type_menu(self):
        """ Displays/validates the selected options for the option: 1 . Change output format """ 

        self.print_dictionary_list(self.change_output_type_options(), "--- Change Output Type Menu ---")

        while True:   
            output_opts = raw_input("\nPlease enter a number: ")
            
            if output_opts == "1" or output_opts == "2" or output_opts == "3":
                self.change_output_type_options()[output_opts]
                break
            else:
              print "Oops!  That was not a valid option number.  Try again..." 
        self.execute_change_output_option(output_opts)

    def display_generate_sudoku_menu(self):
        """ Displays and validates the selected options for the option "3. Generate Sudoku" """

        self.print_dictionary_list(self.change_generate_sudoku_options(), "--- Generate Sudoku Menu ---")

        while True:   
            generate_opts = raw_input("\nPlease enter a number: ")            

            if generate_opts == "1" or generate_opts == "2" or generate_opts == "3":
                self.change_generate_sudoku_options()[generate_opts]
                break
            else:
              print "Oops!  That was not a valid option number.  Try again..." 
        self.execute_generate_sudoku_option(generate_opts)

    def display_configure_menu(self):
        """ Displays and validates the selected options for the option "1 . Configure" """ 

        self.print_dictionary_list(self.conf_menu_options(), "--- Configuration Menu ---")

        while True:   
            config_opts = raw_input("\nPlease enter a number: ")            

            if config_opts == "1" or config_opts == "2" or config_opts == "3"\
                                  or config_opts == "4" or config_opts == "5":
                self.conf_menu_options()[config_opts]
                break
            else:
              print "Oops!  That was not a valid option number.  Try again..." 
        self.execute_conf_option(config_opts)

    def change_generate_sudoku_options(self):
        """ Defines the 3 available options for the option "3. Generate Sudoku" """

        generate_opts = {'1': 'Save Sudoku to TXT file', '2': 'Display Sudoku on console',\
                         '3': 'Back to Main menu'}    

        return generate_opts

    def change_output_type_options(self):
        """ Defines the 3 available options for the option "1 . Change output format" """

        output_opts = {'1': 'Display result in console', '2': 'Save result in a file', '3': 'Back'} 
        return output_opts
    
    def change_algorithm_menu_options(self):
        """ Defines the available Algorithm methods for the sudoku resolution """

        algorit_opts = {'1': 'Norvig', '2': 'Backtracking', '3': 'Brute Force', '4': 'Back'}
        return algorit_opts
    
    def change_level_menu_options(self):
        """ Defines the available levels for the option "2 . Change level" """

        level_opts = {'1': 'Easy', '2': 'Medium', '3': 'Hard', '4': 'Back'}
        return level_opts
    

    def print_dictionary_list(self, dictionary, title_menu = ""):
        """ Prints the dictionary list for each value """ 
        if title_menu != "":
            print "\n" + title_menu + "\n"

        for n in range (1, len (dictionary) + 1):
            for key, value in dictionary.iteritems() :
                if str(n) == key:
                    print key, value
                         
if __name__ == "__main__":
    t = Main()
