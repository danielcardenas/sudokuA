import os
import math
class TXTHandler:
    
    def write_sudoku(self, path, file_name, string_to_write):
        """
        Write a sodoku in a txt file 
        Returns True if the data has been written successfully
        otherwise return False

        Keyword arguments:
        path -- the path of the directory where the file will be created
        file_name -- the file name of the file that will contain the
                     sudoku data
        string_to_write -- the sudoku data to write in the txt file
                       
        """
        sudoku_was_write = False
        if os.path.exists(path):
            try:
                my_file = open(path+file_name, 'w')
                my_file.write(string_to_write)
                my_file.close()
                sudoku_was_write = True
            except:
                sudoku_was_write = False
        return sudoku_was_write


    def get_sudoku_data(self, file_name):
        """
        Given a txt file it converts each row in a valid row entry for the sudoku 
        solver, the method returns a matrix[][] which contains the sudoku data and its size

        Keyword arguments:
        file_name -- stores the sudoku to solve 

        """

        result_data = []      
        sudoku_line = ""
        sudoku_no_spcs = ""
        separator = '\n' 
        
        file_string = file(file_name).readlines()      
        
        for line in range(0, len(file_string)):            
            sudoku_line = sudoku_line + file_string[line]
            sudoku_no_spcs = sudoku_no_spcs + file_string[line].strip('\n')
            if file_string[line] == separator or line == len(file_string)-1:                
                sudoku_matrix = []
                sudoku_line = sudoku_line.strip('\n')
                sudoku_matrix.append(self.get_line_with_end_of_line(sudoku_line))
                size_sudoku = math.sqrt(len(sudoku_no_spcs))                       
                if size_sudoku % 1 > 0:
                    size_sudoku = -1
                if size_sudoku != 0:
                    sudoku_matrix.append(int(size_sudoku))
                    result_data.append(sudoku_matrix)
                sudoku_line = ""
                sudoku_no_spcs = ""            
        return result_data

    def get_line_with_end_of_line(self, line):
        """
        Method that adds an empty line (if does not have one) for the last sudoku within the file 

        Keyword arguments:
        line -- stores the lines for the given sudoku

        """
        if len(line) > 0:
            if line[-1] != "\n":
                line += "\n"
        return line
