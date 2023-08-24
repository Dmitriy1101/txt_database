import os, re, datetime


class TextDatabase():
    '''
    Сущность для работы с файлом
    '''

    def __init__(self, file_name):
        self.file_name = file_name
        self.ping()

    def ping(self):
        '''Тут мы проверим файл на на существование и если надо создадим'''
        p = os.path.isfile(self.file_name)
        if p:
            with open(self.file_name) as f:
                l = len([line for line in f])
            b = os.stat(self.file_name)
            self._id = l
            print(f'Файл {self.file_name} существует, имеет {l} строк, занимает {b.st_size} байт.\n')
        else:
            with open(self.file_name, 'w+', encoding="utf-8") as f:
                self._id = 0
            print(f'\nФайл {self.file_name} не обнаружен и был создан.')
        return p

    def get_date(self):
        '''Дата время сейчас'''
        return datetime.datetime.now()

    def get_none(self):
        '''Заполняем не заполненые поля/Заглушка для значения по умолчанию'''
        return 'Not entered'

    def is_visiable(self, field):
        '''Видимо ли поле True/False'''
        return self._fields[field].get('visible')

    def get_default(self, field):
        '''Возвращает значение поля по умолчанию'''
        move = self._fields[field].get('default')
        if isinstance(move, bool):
            return move
        return move(self)

    def get_related_name(self, field):
        '''Вернем читаемое имя'''
        return self._fields[field].get('related_name')

    def get_id(self):
        '''Наш идентификатор +1'''
        self._id += 1
        return self._id

    def get_basic_namefield(self, r_field):
        '''Преобразуем читаемое имя в имя поля'''
        for field in self._fields:
            if self._fields[field].get('related_name') == r_field:
                return field
        return False

    #при желании можно придумать чтонибудь по куруче но в рамках ТЗ оставим так
    _fields = {
        'id' : {
            'visible' : False, 
            'default' : get_id, 
            'related_name' : 'Идентификатор'
            },
        'name' : {
            'visible' : True, 
            'default' : get_none, 
            'related_name' : 'Имя'
            },
        'surname': {
            'visible' : True, 
            'default' : get_none, 
            'related_name' : 'Фамилия'
            },
        'patrionymic' : {
            'visible' : True, 
            'default' : get_none, 
            'related_name' : 'Отчество'
            },
        'organization' : {
            'visible' : True, 
            'default' : get_none, 
            'related_name' : 'Организация'
            },
        'work_phone' : {
            'visible' : True, 
            'default' : get_none, 
            'related_name' : 'Рабочий_телефон'
            },
        'personal_phone' : {
            'visible' : True, 
            'default' : get_none, 
            'related_name' : 'Личный_телефон'
            },
        'recording_date' : {
            'visible' : False, 
            'default' : get_date, 
            'related_name' : 'Изменялся'
            },
        'modified' : {
            'visible' : False, 
            'default' : False, 
            'related_name' : 'Дата_записи'
            },
    }

    def get_fields(self):
        '''Вернем список полей'''
        return self._fields.keys()

    def show_fields(self):
        '''Вернем список видимых пользователю полей'''
        return [self.get_related_name(a) for a in self.get_fields() if self.is_visiable(a)]

    def get_dict_from_line(self, line):
        '''Преобразуем строку прочитаную из файла в словарь.'''
        line_list = line.split('|')
        line_list.pop(0)
        line_list.pop(-1)
        fields = self.get_fields()
        person = {}
        for field in fields:
            d = line_list.pop(0)
            person.setdefault(field, d)
        return person
        
    def get_line_from_dict(self, obj: dict):
        '''Преобразует словарь в строку, пртгодную для записи в файл'''
        line = '|'
        for item in obj:
            line = f'{line}{obj[item]}|'
        return f'{line}\n'

    def get_data(self):
        '''
        Извлекаем данные из файла.
        Возвращаем список
        '''
        fields = self.get_fields()
        data = []
        with open(self.file_name, 'r', encoding="utf-8") as f:
            for l in f:
                person = self.get_dict_from_line(l)
                data.append(person)
        print('Поиск завершен.\n')
        return data

    def print_obj(self, obj: dict):
        '''Печатаем одну сущность из данных на экран'''
        print(','.join([f' {self.get_related_name(field)} : {obj[field]}' for field in self.get_fields() if self.is_visiable(field)]))

    def print_data(self, data):
        '''
        Печатаем данные на экран.
        '''
        if data:
            for d in data:
                self.print_obj(d)
        else:
            print('Тут пусто')

    def put_data(self, data):
        '''
        Эаппись данных в файл.
        Вернет True в случае успеха.
        '''
        with open(self.file_name, 'a', encoding="utf-8") as f:
            for obj in data:
                f.write(self.get_line_from_dict(obj))
        print('Запись  завершена\n')
        return True

    def input_person(self):
        '''
        Читаем данные с клавиатуры для одной строки.
        Вернет словарь пригодный к записи.
        '''
        print('Вводим данные\n')
        person = {}
        for field in self._fields:
            if self.is_visiable(field):
                name_f = self.get_related_name(field)
                i = input(f'Вводим значение {name_f}:')
                if i:
                    person.setdefault(field, i)
                else:
                    person.setdefault(field, self.get_default(field))
            else:
                person.setdefault(field, self.get_default(field))
        return person

    def get_input_list(self):
        '''Создаем список для записи в базу.'''
        count = True
        data = []
        while count:
            ke = input('Вводим данные [y/n]?')
            ke = ke.lower()
            if ke == 'y':
                data.append(self.input_person())
            elif ke == 'n':
                count = False
            else:
                print(f'Непредвиденная команда:"{ke}", возможно у вас проблемы с руками.\n Отмена ввода.')
                count = False
        return data

    def get_fields_set(self, choise):
        '''Создаем список полей и валидируем его для поиска'''
        fields = []
        second = re.split(' ', choise)
        for s in second:
            if s in self.show_fields() and s not in fields:
                fields.append(s)
            elif s in fields:
                print(f'Исключен дубликат: {s}')
            else:
                print(f'Некорректное поле Исключено: {s}')
        return fields

    def find_somefing(self, data = []):
        '''Поиск в файле'''
        choise = input(f'Вкакихполях будем искать(через пробел)\n Поля: {self.show_fields()}:\n')
        fields_set = self.get_fields_set(choise)
        if not fields_set:
            print('Наеправильный ввод обозначений поля\n')
            return fields_set
        discovered = {}#Словарь с параметрами поиска 'поле поиска':'значене для поиска'
        for field in fields_set:
            text = input(f'Что ищем в значении {field}(ENTER - всё!):')
            discovered.setdefault(self.get_basic_namefield(field), text)
        if not data:
            data = self.get_data()
        correct_data = []
        for obj in data:
            for d in discovered:
                value = obj.get(d)#извлекаем из объекта поле для проверки
                if value.find(discovered.get(d)) != -1:
                    correct_data.append(obj)
        return correct_data
    
    def correction_obj(self, obj):
        '''Исправляем объект из данных'''
        for field in obj:
            if self.is_visiable(field):
                choise = input(f'Поле: {self.get_related_name(field)} \nзначение: {obj.get(field)}\nВведите новое значение или ENTER для пропуска:')
                if choise:
                    obj[field] = choise
        obj['modified'] = True
        obj['recording_date'] = self.get_default('recording_date')
        return obj

    def correction_data(self, data):
        '''Исправляем список данных'''
        new_data = []
        if not data:
            return new_data
        for obj in data: 
            self.print_obj(obj)
            choise = input('Меняем?[y/n]')
            choise = choise.lower()
            if choise == 'y':
                obj = self.correction_obj(obj)
                new_data.append(obj)
            elif choise == 'n':
                print('Отбой.')
            else:
                print('Будем считать что нет.')
        return new_data

    def put_corrected_data(self, data):
        '''Записываем в файл исправленные данные'''
        id_list = [obj.get('id') for obj in data]
        #id_list = sorted(int(a) for a in id_list)
        id_list = sorted(id_list)
        with open(self.file_name, 'r', encoding="utf-8") as f:
            lines = f.readlines()
        id_l = 1
        with open(self.file_name, 'w', encoding="utf-8") as f:
            for line in lines:
                if id_list and str(id_l) == id_list[0]:
                    id_list.pop(0)
                    obj = data.pop(0)
                    f.write(self.get_line_from_dict(obj))
                else:
                    f.write(line)
                id_l += 1
        return True

                        
class SessionFather():
    ''' Команды прописаны тут '''

    def __init__ (self, file_name):
        self.file_name = file_name
        self._driver = TextDatabase(file_name = self.file_name)

    def end_it(self):
        '''Так мы выйдем.'''
        print('See you soon')

    def not_delete(self):
        '''Надеюсь и так понятно.'''
        print('\nDELETE нету в тз!\n')
        return self.get_start()

    def get_description(self, method):
        '''Достаем описание метода.'''
        return self._methods[method].get('description')
        
    def get_move_set(self):
        '''Список методов'''
        return self._methods.keys()

    def run_move(self, method):
        '''Запуск базовых функций обработчика'''
        move = self._methods[method].get('function')
        return move(self)

    #В рамках ТЗ данные будем хранить тут
    operated_data = []

    def get_methods(self):
        '''Создаем форму функционала'''
        s = ''
        for m in self._methods:
            el =  self.get_description(m)
            s = f'{s} {m} : {el}\n'
        return s

    def get_start(self):
        '''Точка входа в наш рабочий процесс. Тут мы выбираем действие.'''
        print(f'\nМы можем:\n{self.get_methods()}')
        while True:
            move = input('Ваш выбор:\n')
            move = move.upper()
            if move in self.get_move_set():
                return self.run_move(move)
            else:
                print('Возникла проблема с вашими руками.')

    def get_data(self):
        '''Формируем запрос на получение данных'''
        choise = input('Введите:\n \t 1 : Чтобы вывести все записи.\n \t 2 : Чтобы выбрать поля и значения для поиска.\n \t 3 : Для поиска в извлеченных данных.\n \t 4 : Для возврата.\n')
        if choise == '1':
            print('Ищем все.\n')
            self.operated_data = self._driver.get_data()
            self._driver.print_data(self.operated_data)
        elif choise == '2':
            self.operated_data = self._driver.find_somefing()
            self._driver.print_data(self.operated_data)
        elif choise == '3':
            if self.operated_data:
                self.operated_data = self._driver.find_somefing(data = self.operated_data)
                self._driver.print_data(self.operated_data)
            else:
                print('\nТут пусто. Идем назад')
        elif choise == '4':
            print('\nИдем назад')
        else:
            #Вариант 'Это все клавиатура'
            print('Ваш палец застрял в носу.\n')
        return self.get_start()

    def check(self):
        '''Проверяем наличие файла и его объём'''
        p = self._driver.ping()
        return self.get_start()

    def put(self):
        '''Считываем данные с клавиатуры и записываем.'''
        data = self._driver.get_input_list()
        res = self._driver.put_data(data)
        if res:
            print('Получилось')
        else:
            print('Беда печаль не повезло...')
        return self.get_start()

    def update(self):
        choise = 'n'
        if self.operated_data:
            self._driver.print_data(self.operated_data)
            choise = input('Хотите править уже извлеченные данные?[y/n]')
            choise = choise.lower()
        if choise == 'n':
            print('Формируем список кандидатов на корректировку:')
            self.operated_data = self._driver.find_somefing()
        if not self.operated_data:
            return self.get_start()    
        print('Начинаем исправлять:')
        self.operated_data = self._driver.correction_data(self.operated_data)
        print('Записываем:')
        self._driver.print_data(self.operated_data)
        self._driver.put_corrected_data(self.operated_data)
        return self.get_start()

    _methods = {
        'GET' : {
            'description' : 'извлечь содержимоефайла или по списку полей.', 
            'function' : get_data
            },
        'CHECK' : {
            'description' : 'Проверить наличие файла и его объём.', 
            'function' : check
            },
        'PUT' : {
            'description' : 'Записать в файл', 
            'function' : put
            },
        'UPDATE' : {
            'description' : 'Найти и исправить запись', 
            'function' : update
            },
        'DELETE' : {
            'description' : 'Нету в тз, ура!', 
            'function' : not_delete
            },
        'EXIT' : {
            'description' : 'Выход.', 
            'function' : end_it
            }
    }



if __name__  == "__main__":
    # Стартуем))
    file_name = 'text_database.txt'
    choise = input(f'Здравствуйте по умолчанию мы работаем с файлом {file_name}, нажмите ввод чтобы продолжить.\n Или введите альтернативное название файла:\n')
    if choise and choise[-4:] == '.txt':
        file_name = choise
    elif not choise:
        print('Выбор по умолчанию.')
    else:
        print('Ошибка в названии, изменение отклонено.\n')
    work = SessionFather(file_name = file_name)
    work.get_start()
