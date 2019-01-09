PATTERNS = [
    '\%ptrn\(\d+\)\% ',                                # %pattern%
    '\%sn\(\d*\)\%',                               # %sn(x)% - порядковый номер, "число" - кол-во параметров
    '\%cell\(\d+\,\s*\d+\)\%',             # %cell(x, y, z)%
    '\%title\_fanuc\%',                            # заголовок программы для роботов Fanuc
    '\%end\_fanuc\%',                               # конец программы Fanuc
    '\%block\(\d+\)\%',
    '\%end\_block\%'
]
NAME_FILE_IN = 'Fanuc.ptrn'
EXCEL_NAME = 'C:\Kjellberg_cutting_data_table\Kjellberg_cutting_data_table.xlsx'
EXCEL_LETTER = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
WB_NAME = 'Лист1'
NAME_FILE_OUT = 'C:\Kjellberg_cutting_data_table\SET_CUT_PARAMETERS.ls'
TITLE_FANUC = ['/PROG ',                        #1
               '\n/ATTR\nOWNER = ',
               ';\nCOMMENT = "',
               '";\nPROG_SIZE = ',
               ';\nCREATE = ',                  #5
               ';\nMODIFIED = ',
               ';\nFILE_NAME = ',
               ';\nVERSION = ',
               ';\nLINE_COUNT = ',
               ';\nMEMORY_SIZE = ',             #10
               ';\nPROTECT = ',
               ';\nTCD:\tSTACK_SIZE = ',
               ',\n\tTASK_PRIORITY = ',         #15
               ',\n\tTIME_SLICE = ',
               ',\n\tBUSY_LAMP_OFF = ',
               ',\n\tABORT_REQUEST = ',
               ',\n\tPAUSE_REQUEST = ',
               ';\nDEFAULT_GROUP = *,*,*,*,*;\nCONTROL_CODE = 00000000 00000000;\n/APPL\n  ',
               'ARC Welding Equipment : ',
               ';\n\nMPAS ;\nMPAS_NUM_PASSES : 0;\nMPAS_LAST_PASS : 0;\n',
               'MPAS_CURRENT_PASS : 0;\nMPAS_STATUS_PASS : 0;\n/MN']
END_FANUC = '/POS\n/END\n'
TITLE_FANUC_CONST = [
    'SET_CUT_PARAMETERS',        # 1
    'MNEDITOR',
    '',
    '1',
    '',                         #5
    '',
    '',
    '0',
    '',
    '1',                         #10
    'READ_WRITE',
    '0',
    '50',
    '0',
    '0',                        #15
    '0',
    '0',
    '',
    '1,*,*,*,*',
    '',
    ''
]