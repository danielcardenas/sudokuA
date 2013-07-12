import unittest
import sys
import os
sys.path.append( '../libs' )
from txt_handler import TXTHandler

class TestTXTHandler(unittest.TestCase):

    def setUp(self):
        self.txt_handler = TXTHandler()
        # get the pathdir where the application is running
        file = sys.argv[0]
        self.pathname = os.path.dirname(file)
        # create an file to test the existing file case
        myFile = open(self.pathname + '/test_exist_file.txt', 'w')
        myFile.write("te")
        myFile.close()

        # Valid txt format 9x9
        self.txt = open ('valid_sudoku_0.txt', 'rb')
        self.valid_txt = self.txt.read()
        
        # Invalid txt format 9x9
        self.txt = open ('invalid_sudoku_0.txt', 'rb')
        self.invalid_txt = self.txt.read()
        self.size = len(self.valid_txt)

    def tearDown(self):
        os.remove(self.pathname + '/test_exist_file.txt')

    def test_the_name_file_increments_when_the_same_file_exist(self):
        res = self.txt_handler.get_file_name(self.pathname + "/", 'test_exist_file.txt', 0)
        self.assertEquals('test_exist_file1.txt', res)

    def test_the_name_file_is_the_same_when_the_file_not_exist(self):
        res = self.txt_handler.get_file_name(self.pathname + "/", 'test_not_exist_file.txt', 0)
        self.assertEquals('test_not_exist_file.txt', res)

    def test_write_sudoku_returns_true_file_has_been_write(self):
        res = self.txt_handler.write_sudoku(self.pathname + "/", 'test_not_exist_file.txt', "test")
        os.remove(self.pathname + '/test_not_exist_file.txt')
        self.assertTrue(res)

    def test_write_sudoku_writes_the_specified_line(self):
        line_to_write = "test\n" + \
                        "this is a test"
        self.txt_handler.write_sudoku(self.pathname + "/", \
                                     'test_write_specified_line.txt', line_to_write)
        file_written = open(self.pathname+"/" + 'test_write_specified_line.txt', "r")
        content = file_written.readlines()
        res = ""
        for l in content :
            res = res + l
        file_written.close()
        os.remove(self.pathname + '/test_write_specified_line.txt')
        self.assertEquals(res,line_to_write)

    def test_read_sudoku_for_valid_txt_using_separator_0(self):
        txt_file = TXTHandler()
        self.expected = '316578492\n' + \
                        '529134768\n' + \
                        '487629531\n' + \
                        '263415987\n' + \
                        '974863125\n' + \
                        '851792643\n' + \
                        '138947256\n' + \
                        '692351874\n' + \
                        '745286319'

        result = txt_file.get_sudoku_data('valid_sudoku_0.txt')
        self.assertEquals(self.expected, result[0][0])
        
    def test_read_sudoku_for_valid_size_using_0(self):
        txt_file = TXTHandler()
        self.expected_size = 9
        result = txt_file.get_sudoku_data('valid_sudoku_0.txt')
        self.assertEquals(self.expected_size, result[0][1])

    def test_read_sudoku_for_invalid_txt_using_separator_0(self):
        txt_file = TXTHandler()
        self.expected = '31657849\n' + \
                        '529134768\n' + \
                        '487629531\n' + \
                        '263415987\n' + \
                        '974863125\n' + \
                        '851792643\n' + \
                        '138947256\n' + \
                        '692351874'

        result = txt_file.get_sudoku_data('invalid_sudoku_0.txt')
        self.assertEquals(self.expected, result[0][0])
        
    def test_read_sudoku_for_invalid_size_using_0(self):
        txt_file = TXTHandler()
        self.expected_size = -1
        result = txt_file.get_sudoku_data('invalid_sudoku_0.txt')
        self.assertEquals(self.expected_size, result[0][1])

    def test_read_sudoku_for_valid_txt_using_separator_dot(self):
        txt_file = TXTHandler()
        self.expected = '3.657.4.2\n' + \
                        '..913.76.\n' + \
                        '487...531\n' + \
                        '26..15.8.\n' + \
                        '...86..25\n' + \
                        '.5.7.2.4.\n' + \
                        '.389.725.\n' + \
                        '6.2..1.74\n' + \
                        '745.6.1..'

        result = txt_file.get_sudoku_data('valid_sudoku_dot.txt')
        self.assertEquals(self.expected, result[0][0])

    def test_read_sudoku_for_valid_size_using_dot(self):
        txt_file = TXTHandler()
        self.expected_size = 9
        result = txt_file.get_sudoku_data('valid_sudoku_0.txt')
        self.assertEquals(self.expected_size, result[0][1])
        
    def test_read_sudoku_for_invalid_txt_using_separator_dot(self):
        txt_file = TXTHandler()
        self.expected = '3.657..2\n' + \
                        '..913.76.\n' + \
                        '487...531\n' + \
                        '26..15.8.\n' + \
                        '...86..25\n' + \
                        '.5.7.2.4.\n' + \
                        '.389.725.\n' + \
                        '6.2..1.74'                     

        result = txt_file.get_sudoku_data('invalid_sudoku_dot.txt')
        self.assertEquals(self.expected, result[0][0])

    def test_read_sudoku_for_invalid_size_using_dot(self):
        txt_file = TXTHandler()
        self.expected_size = -1
        result = txt_file.get_sudoku_data('invalid_sudoku_0.txt')
        self.assertEquals(self.expected_size, result[0][1])
        
if __name__ == "__main__":
    unittest.main()
