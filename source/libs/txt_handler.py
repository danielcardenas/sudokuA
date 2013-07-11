import os
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
            file_name = self.get_file_name(path, file_name, 0)
            try:
                myFile = open(path+file_name, 'w')
                myFile.write(string_to_write)
                myFile.close()
                sudoku_was_write = True
            except:
                sudoku_was_write = False
        return sudoku_was_write

    def get_file_name(self, path, file_name, number_file):
        """
        Returns a non-exist file name. If the given file name already
        exists it add a number to the end the file and if the new file
        name does not exist return that name

        Keyword arguments:
        path -- the path of the directory where the file will be created
        file_name -- the file name of the file that will contain the
                     sudoku data
        number_file -- the start number that will be added to the end of
                       the file
                       
        """
        if not os.path.isfile(path + file_name):
            file_name_to_write =  file_name
        else:
            new_number_file = number_file + 1
            new_file_name = file_name[0:(len(file_name)-4)] + str(new_number_file)+'.txt'
            if not os.path.isfile(path + new_file_name):
                file_name_to_write =  new_file_name
            else:
                file_name_to_write = self.get_file_name(path, file_name, new_number_file)
        return file_name_to_write

    def get_sudoku_data(self, file_name):
        """
        Given the a txt file it converts the
        each row in a valid row entry for the sudoku solver
        Returns a matrix[][] which contain the sudoku data
        and its size

        Keyword arguments:
        res -- contains the sudoku and its size
        sudoku -- contains the lines for the sudoku
        sudoku1 -- contains the lines for the sudoku without spaces
        file_string -- used for reading the txt file lines
        sep -- used as separator in order to mark the end of a sudoku
        size_sudoku -- stores the sudoku's size

        """
        res = []      
        sudoku = ""
        sudoku1 = ""
        sep = '\n' 
        
        file_string = file('file_name').readlines()
        
        for line in range(0, len(file_string)):
            sudoku = sudoku + file_string[line]
            sudoku1 = sudoku1 + file_string[line].strip('\n')
            if file_string[line] == sep:
                aux = []
                sudoku = sudoku.strip('\n')
                aux.append(sudoku)
                size_sudoku = math.sqrt(len(sudoku1))                       
                if size_sudoku % 1 > 0:
                    size_sudoku = -1
                aux.append(int(size_sudoku))
                res.append(aux)
                sudoku = ""
                sudoku1 = ""
        print res