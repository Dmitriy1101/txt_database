# txt_database
simple script

# Здравствуйте это выполненное ТЗ:
## https://docs.google.com/document/d/1dIH7lY05hNLSluZgOYsRyTrvLmyz4CnNEtJFFXBbS-c/edit
# Подробности:

- Cкрипт состоит из двух классов:
  - TextDatabase() Отвечающий за работу с файлом и обработку данных.
  - SessionFather() Отвечающий за взаимодействие с пользователем и формирование запросов.
- Краткое описание __ОСНОВНЫХ__ функций: 
  - TextDatabase():
    - ping() проверка на состояние/создание файла.
    - get_fields() список полей.
    - show_fields() список видимых полей, в читабельном формате.
    - get_dict_from_line(line) преобразует страку прочитаную из файла в словарь данных.
    - get_line_from_dict(obj) Преобразуем словарь данных В строку, готовую к  записи в файл.
    - get_data() Создаем список данных, прочитаных из файла.
    - print_obj() Выводим одну сущность данных(dict) на экран.
    - print_data(data) Выводит список данных на экран.
    - put_data(data) Запись данных в файл.
    - input_person() Отвечает за ввод данных одной сущности данных, возвращает dict.
    - get_input_list() Создает список данных готовых к записи в файл.
    - get_fields_set(input_str) Формирует и валидирует список полей для поиска.
    - find_somefing(data = []) Осуществляет поиск в файле или переданых данных.
    - correction_obj(obj) Производит внесение исправлений одну сущность из данных(dict).
    - correction_data(data) Произвводит внесение изменений в список данных.
    - put_corrected_data(data) Вносит исправления в файл на основе полученого списка данных.
  - SessionFather():
    - get_start() Точка входа в нашу программу.
    - get_methods() Формирует строку содерщащую списой функций.
    - get_data() Отвечает за набор запросов поиска и извлечения данных.
    - check() Проверка состояния файла.
    - put() Чтение с клавиатуры и запись в файл.
    - update() Внесение информации в файл.
- Моя логика:
  - Важную часть в работе имеют сущности _methods и _fields из SessionFather и TextDatabase соответственно,  они отвечают за связь между объектами методом_управления/полем_из_строки_файла и их свойствами/методами обработки.
  - За активацию методов свойств отвечают методы: get_default(field) из TextDatabase  и run_move(method) из SessionFather.
  - При построении структуры я изходил из логики возможности внетрения в другой проект + сохранение ручного доступа.
  - Мы можем работать с разными файлами.
- Итог:
  - В рамках ТЗ работу считаю выполненой.
  - Данный код при необходимости можно расширить, как по возможностям функционала, так и по возможностям структуры записей.
  - Все.