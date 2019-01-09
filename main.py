import re, openpyxl
from consts import *
from datetime import datetime

class Parser:
    '''
    класс для парсинга ключевых слов в тестовом файле
    '''
    def __init__(self):
        self.file_in = open(NAME_FILE_IN, 'r')
        self.file_out = open(NAME_FILE_OUT, 'w+')
        wb = openpyxl.load_workbook(filename=EXCEL_NAME)
        self.sheet = wb[WB_NAME]

        self.patterns = PATTERNS
        self.line_number = 1

        self.line_numeration = False
        self.line_excel = False
        self.line_title_fanuc = False
        self.line_end_fanuc = False
        self.use_block = False

        self.line = ""
        self.excel_start_row = 1
        self.excel_start_column = 1
        self.excel_number_cell = 1
        self.block_counter = 1
        self.block_task = 1
        self.excel_now_row = 0
        self.excel_now_column = 0
        self.excel_now_cell = 0
        self.block = []

    def start(self):
        '''
        начало работы обработчика
        '''
        # передаем строки в селектор
        [self.selector(line) for line in self.file_in]
        # закрываем все использованные файлы
        self.file_in.close()
        self.file_out.close()
        # запускаем самописный метод постпроцессор
        self.postprocessor()

    def selector(self, line):
        '''
        выбор способа обработки
        :param line: строка из текста для обработки
        '''
        # в начале строки %ptrn()%
        if re.search(self.patterns[0], line) is not None:
            # выделение ключевого слова %ptrn()%
            res_search_in_line = self.try_search(self.patterns[0], line)
            # извлечение параметра из ключевого слова %ptrn()%
            self.excel_number_cell = int(self.extraction_parameters(res_search_in_line)[0])
            # удаление слова %ptrn()% из строки
            self.line = self.delete_parameter(line, self.patterns[0])
            # определение есть ли %sn()% в строке
            self.serial_number(self.line)
            # определение есть ли %cell()% в строке
            self.excel_extr(self.line)
            # определение есть ли %title_fanuc% в строке
            self.line_title_fanuc = self.check_none(self.patterns[3], self.line)
            # определение если ли %end_fanuc% в строке
            self.line_end_fanuc = self.check_none(self.patterns[4], self.line)
            # запуск конструктора строки для замены ключевых слов на значения
            self.designer_ptrn(self.line)
        # в начале строки %block()%
        elif re.search(self.patterns[5], line) is not None:
            # выделение ключевого слова %block()%
            res_search_in_line = self.try_search(self.patterns[5], line)
            # извлечение параметра из ключевого слова %block()%
            self.excel_number_cell = int(self.extraction_parameters(res_search_in_line)[0])
            # ставим флаг self.use_block
            self.use_block = True
        # в начале строки нет %end_block%, но до этого было ключевое слово %block()%
        elif self.use_block and re.search(self.patterns[6], line) is None:
            # добавляем строку в список для обработки блока строчек
            self.block.append(line)
        # в начале строки есть %end_block%
        elif self.use_block and re.search(self.patterns[6], line) is not None:
            # определяем есть ли в строке %end_block%
            self.use_block = False

            self.designer_block()
        # в строке нет ключевых слов
        else:
            self.file_out.write(line)


    def designer_block(self):
        '''
        конструктор %block()%
        '''
        # цикл, копирующий блок из файла требуемое кол-во раз
        for i in range(self.excel_number_cell):
            # цикл, проходится по списку self.block вставляя требуемые значения
            for j in range(len(self.block)):
                # заменяет ключевое слово %sn()% на номер строки
                line = self.numeration(self.block[j])
                # определение есть ли ключевое слово %cell()% в строке
                self.excel_extr(line)
                # в строке есть %cell()%
                if self.line_with_excel:
                    # замена ключевого слова %cell()% на значение из таблицы
                    line = re.sub(self.patterns[2], str(self.excel(self.excel_now_column, self.excel_now_row + i)), line)
                # запись строчки в файл
                self.file_out.write(line)

    def designer_ptrn(self, line):
        '''
        конструктор %ptrn()%
        :param line: обрабатываемая строка
        '''

        line = self.numeration(line)
        if self.line_with_excel and self.excel_number_cell > self.excel_now_cell:
            line = re.sub(self.patterns[2], str(self.excel(self.excel_now_column, self.excel_now_row)), line)
            self.excel_now_cell += 1
            self.excel_now_row += 1
            self.file_out.write(line)
            self.designer_ptrn(self.line)
            return None
        elif self.line_with_excel and self.excel_number_cell == self.excel_now_cell:
            self.line_number -= 1
            return None

        if self.line_end_fanuc:
            line = re.sub(self.patterns[4], str(END_FANUC), line)
        if self.line_title_fanuc:
            line = re.sub(self.patterns[3], self.title_fanuc(TITLE_FANUC, TITLE_FANUC_CONST), line)
        self.file_out.write(line)
        return None

    def numeration(self, line):
        '''

        :param line: обрабатываемая строка
        :return:
        '''
        if self.line_numeration:
            line = re.sub(self.patterns[1], str(self.line_number), line)
            self.line_number += 1
            return line
        else:
            return line

    def excel_extr(self, line):
        '''

        :param line: обрабатываемая строка
        :return:
        '''
        res_search_in_line = self.try_search(self.patterns[2], line)
        if res_search_in_line is not None:
            self.excel_start_column, \
            self.excel_start_row  = [int(x) for x in self.extraction_parameters(res_search_in_line)]
            self.line_with_excel = True
            self.excel_now_row = self.excel_start_row
            self.excel_now_column = self.excel_start_column
            if not self.use_block:
                self.excel_now_cell = 0
        else:
            self.line_with_excel = False

    def postprocessor(self):
        '''
        постобработка текста из файла
        '''
        # открываем файл для чтения
        with open(NAME_FILE_OUT) as file_in:
            text = file_in.read()
        # вставляем в текст кол-во строк программы
        text = text.replace("LINE_COUNT = ",
                            "LINE_COUNT = " + str(self.line_number-1))
        # вставляем текущую дату и время в текст
        text = text.replace("CREATE = ",
                            "CREATE = " + datetime.strftime(datetime.now(), "DATE %y-%m-%d  TIME %H:%M:%S"))
        text = text.replace("MODIFIED = ",
                            "MODIFIED = " + datetime.strftime(datetime.now(), "DATE %y-%m-%d  TIME %H:%M:%S"))
        # перезаписываем открытый в этом методе файл для получения результата
        with open(NAME_FILE_OUT, "w") as file_out:
            file_out.write(text)

    def delete_parameter(self, line, parameter):
        '''
        удаление текста из строки
        :param line: строка для обработки
        :param parameter: удаляемый текст
        :return: возвращаем результат
        '''
        return re.sub(parameter, '', line)

    def serial_number(self, line):
        '''

        :param line: обрабатываемая строка
        :return:
        '''
        res_search_in_line = self.try_search(self.patterns[1], line)
        if res_search_in_line is not None:
            try:
                self.line_number = int(self.extraction_parameters(res_search_in_line)[0])
            except IndexError:
                pass
            self.line_numeration = True
        else:
            self.line_numeration = False

    def extraction_parameters(self, expression):
        return re.findall('\d+', expression)

    def title_fanuc(self, title, title_const):
        return ''.join(map(''.join, zip(title, title_const)))

    def excel(self, column, row):
        '''
        извлекает из определенной ячейки таблицы значение
        :param column: номер столба из таблицы excel
        :param row: номер строки из таблицы excel
        :return: значение из ячейки
        '''
        value = self.sheet[EXCEL_LETTER[column-1]+str(row)].value
        if float(value) % 1 == 0:
            return value
        else:
            return str(round(float(value), 3))

    def check_none(self, pattern, line):
        '''
        проверка наличия паттерна в строке
        :param pattern: патерн для поиска
        :param line: строка в которой ищем
        :return: возвращает True, если нашел. False, если не нашел
        '''
        # получаем "значение" или None
        result = self.try_search(pattern, line)
        # если "значение"
        if result is not None:
            return True
        # если None
        else:
            return False

    def try_search(self, pattern, line):
        '''
        поиск паттерна в строке
        :param pattern: паттерн для поиска
        :param line: строка в которой ищем
        :return: возвращает "значение" или None
        '''
        # обработчик исключений, если "значение"
        try:
            return re.search(pattern, line).group(0)
        # если нет значения
        except AttributeError:
            return None

    def __del__(self):
        '''
        деструктор
        '''
        self.file_in.close()


app = Parser()
app.start()
