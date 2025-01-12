from odd_even_csv import get_data
from get import count_links
from different_actions import create_dir, create_days_of_the_week

import pandas as pd


def add_list_classes(list_classes, j, d):
    if len(j) == 4:
        for v in range(1, 4, 2):
            try:
                if d in j[v]:
                    list_classes[0].append(j[v - 1])
                    list_classes[1].append(j[v])
            except:
                # list_classes[v].append(" ")
                pass
    elif len(j) == 3:
        for v in range(3):
            try:
                if d in j[v] and v != 0:
                    list_classes[1].append(j[v])
                elif v == 0:
                    list_classes[0].append(j[v])
            except:
                pass
    elif len(j) == 2:
        for v in range(2):
            try:
                list_classes[v].append(j[v])
            except:
                pass


def teacher_csv():
    # Создание директорий в проекте
    create_dir("teacher_odd")
    create_dir("teacher_even")

    # Список дней недели пропускаю первое значение, так как оно пустое
    days_of_week = create_days_of_the_week()[1::]

    full_vapor = [
        "Первая пара",
        "Вторая пара",
        "Третья пара",
        "Четвёртая пара",
        "Пятая пара"
    ]
    # Значение для первого параметра сортировки по дням недели
    days_map = {
        'Понедельник': 1,
        'Вторник': 2,
        'Среда': 3,
        'Четверг': 4,
        'Пятница': 5,
        'Суббота': 6,
        'Воскресенье': 7
    }
    # Значение для второго параметра сортировки по парам
    pairs_map = {
        'Первая пара': 1,
        'Вторая пара': 2,
        'Третья пара': 3,
        'Четвёртая пара': 4,
        'Пятая пара': 5
    }
    # Первый цикл для прохода по именам преподавателей
    for d in get_list_teacher():
        # Различные вспомогательные данные
        counter = 0
        list_classes = [[], []]
        right_day = []
        group_number = []
        vapor_number = []
        # Помощь для записи разных данных в DataFrame
        even = {
            "день недели": [],
            "номер пары": [],
            "группа": [],
            "название предмета": [],
            "преподаватель": [],
        }
        # Помощь для записи разных данных в DataFrame
        odd = {
            "день недели": [],
            "номер пары": [],
            "группа": [],
            "название предмета": [],
            "преподаватель": [],
        }
        # Второй цикл для того, чтобы получить количество файлов при помощи ссылок и пройтись по каждому файлу
        for k in range(count_links()):
            # Получаем текст из файла и форматируем его
            list_full_data = get_data(pd.read_csv(f"csv_file/{k}.csv"))
            # Третий цикл для прохода по ранее полученным данным (получаем список)
            for i in list_full_data:
                # Читаем список данных
                for j in i[1::2]:
                    # Использую try для избежания ошибок при появлении нулевых значений (None)
                    try:
                        # Преобразование текста из j для того чтобы в дальнейшем его было удобнее читать
                        j = j.split("\n\n")
                        # Проверка того содержится ли имя преподавателя в полученных значениях
                        if d in j:
                            # Записываем все данные во вспомогательные переменные
                            right_day.append(days_of_week[counter])
                            group_number.append(str(i[0]))
                            vapor_number.append(full_vapor[counter % 5])
                            add_list_classes(list_classes, j, d)
                    except:
                        pass
                    counter += 1
                counter = 0
        # Записываем все вспомогательные данные в основной словарь
        odd["день недели"].extend(right_day)
        odd["номер пары"].extend(vapor_number)
        odd["группа"].extend(group_number)
        # for v in range(len(list_classes)):
        #     odd[f"пара{v}"].extend(list_classes[v])
        odd["название предмета"].extend(list_classes[0])
        odd["преподаватель"].extend(list_classes[1])

        # Записываем в DataFrame словарь odd
        df = pd.DataFrame(odd)

        df['day_num'] = df['день недели'].map(days_map)

        # Преобразуем столбец 'пара' в категориальный тип с заданным порядком
        df['pair_order'] = pd.Categorical(df['номер пары'], categories=pairs_map.keys(), ordered=True)

        # Сортируем сначала по дням недели, затем по парам
        sorted_df = df.sort_values(['day_num', 'pair_order']).drop(columns=['day_num', 'pair_order'])

        sorted_df.to_excel(f"teacher_odd/нечёт {d.replace('/', ' ')}.xlsx", index=False)

        # Вторая операция
        counter = 0
        list_classes = [[], []]
        right_day = []
        group_number = []
        vapor_number = []
        # Повторяем действия выше (стоит потом сделать отдельную функцию)
        for k in range(count_links()):
            list_full_data = get_data(pd.read_csv(f"csv_file/{k}.csv"))
            for i in list_full_data:
                for j in i[2::2]:
                    try:
                        j = j.split("\n\n")
                        if d in j:
                            right_day.append(days_of_week[counter])
                            group_number.append(str(i[0]))
                            vapor_number.append(full_vapor[counter % 5])
                            add_list_classes(list_classes, j, d)
                    except:
                        pass
                    counter += 1
                counter = 0
        even["день недели"].extend(right_day)
        even["номер пары"].extend(vapor_number)
        even["группа"].extend(group_number)
        # for v in range(len(list_classes)):
        #     even[f"пара{v}"].extend(list_classes[v])
        even["название предмета"].extend(list_classes[0])
        even["преподаватель"].extend(list_classes[1])

        df = pd.DataFrame(even)
        df['day_num'] = df['день недели'].map(days_map)

        # Преобразуем столбец 'пара' в категориальный тип с заданным порядком
        df['pair_order'] = pd.Categorical(df['номер пары'], categories=pairs_map.keys(), ordered=True)

        # Сортируем сначала по дням недели, затем по парам
        sorted_df = df.sort_values(['day_num', 'pair_order']).drop(columns=['day_num', 'pair_order'])

        sorted_df.to_excel(f"teacher_even/чёт {d.replace('/', ' ')}.xlsx", index=False)


def get_list_teacher():
    list_teacher = []

    for k in range(count_links()):
        csv_file = pd.read_csv(f'csv_file/{k}.csv')
        list_full_data = get_data(csv_file)

        for i in list_full_data:

            for j in i:
                try:
                    j = j.split("\n\n")
                    if len(j) == 2:
                        list_teacher.append(j[1].replace(" (2 п/г)", "").replace(" (1 п/г)", "").replace(" (1п/г)", "").replace(" (2п/г)", ""))
                    elif len(j) == 3:
                        list_teacher.append(j[1].replace(" (2 п/г)", "").replace(" (1 п/г)", "").replace(" (1п/г)", "").replace(" (2п/г)", ""))
                        list_teacher.append(j[2].replace(" (2 п/г)", "").replace(" (1 п/г)", "").replace(" (1п/г)", "").replace(" (2п/г)", ""))
                    elif len(j) == 4:
                        list_teacher.append(j[1].replace(" (2 п/г)", "").replace(" (1 п/г)", "").replace(" (1п/г)", "").replace(" (2п/г)", ""))
                        list_teacher.append(j[3].replace(" (2 п/г)", "").replace(" (1 п/г)", "").replace(" (1п/г)", "").replace(" (2п/г)", ""))
                except:
                    pass

    return sorted(set(list_teacher))


teacher_list = get_list_teacher()

with open("teacher.txt", "w", encoding="utf-8") as txt_file:
    for i in teacher_list:
        txt_file.write(i + "\n")

teacher_csv()