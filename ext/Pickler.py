import os
import pickle

import __main__

'''
Класс для работы с сериализованными файлами
'''
class work_with_pickle:
    '''
    Получение пикл файла
    '''
    def get_pickle_file(filename):
        with open(filename, 'rb') as f:
                d_ = pickle.load(f)
        return d_
    '''
    Дамп объекта
    Вход: объект, имя файла
    '''
    def dump_pickle_file(obj, filename):
        with open(filename, 'wb') as f:
                pickle.dump(obj, f)
    '''
    Достает из папки все pickle файла, присваеваем имя переменной, как в название объекта
    Вход: путь к папке с pickle файлами
    '''
    def fill_dict(path_to):
        list_files = os.listdir(path_to)
        for file in list_files:
            if file.split('.')[-1] == 'pickle':
                name_dict = file.split('.')[0]
                print(name_dict)
                local_dct = work_with_pickle.get_pickle_file(os.path.join(path_to, file))
                setattr(__main__, name_dict, local_dct)


    '''
    Достаём из словаря словари в которые в него входят, присваеваем имя ключа
    Вход: путь к папке с pickle файлами
    '''
    def fill_dict_from_dict(dicts, prod_mode=False):
        if prod_mode is False:
            if isinstance(dicts, list):
                for d in dicts:
                    for name_dict, dic in d.items():
                        setattr(__main__, name_dict, dic)
            elif isinstance(dicts, dict):
                for name_dict, dic in d.items():
                    setattr(__main__, name_dict, dic)
        elif prod_mode is True:
            local_dict = {}
            if isinstance(dicts, list):
                for d in dicts:
                    for name_dict, dic in d.items():
                        local_dict.update({name_dict: dic})
                return local_dict
            elif isinstance(dicts, dict):
                for name_dict, dic in d.items():
                    local_dict.update({name_dict: dic})
                return local_dict
    '''
    Достаём из словаря словари в которые в него входят, присваеваем имя ключа
    Вход: путь к папке с pickle файлами
    '''
    def fill_dict_from_dict_test(dicts):
        local_dict = {}
        if isinstance(dicts, list):
            for d in dicts:
                for name_dict, dic in d.items():
                    # setattr(__main__, name_dict, dic)
                    d.update({name_dict: dic})
            print(d.keys())
            return d
        elif isinstance(dicts, dict):
            for name_dict, dic in d.items():
                setattr(__main__, name_dict, dic)

    '''
    достаем пикл файлы из папки
    '''
    def fill_dict_from_file(path_to):
        list_files = os.listdir(path_to)
        d = {}
        for file in list_files:
            if file.split('.')[-1] == 'pickle':
                name_dict = file.split('.')[0]
                local_dct = work_with_pickle.get_pickle_file(os.path.join(path_to, file))
                setattr(__main__, name_dict, local_dct)
                d.update({name_dict: local_dct})
        return d
