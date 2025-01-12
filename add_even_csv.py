import pandas as pd

from different_actions import create_dir, create_days_of_the_week, count_links


def get_data(name_file):
    new_list = []
    list_full_data = []
    # Находим количество групп и следовательно, строк информации в расписании
    for i in range(len(name_file["0"])):
        # Группируем всю информацию по столбцам и записываем её в список
        for j in name_file.columns[1:]:
            new_list.append(name_file[j][i])
        # Создаём список списков для дальнейшей работы
        list_full_data.append(new_list)
        new_list = []
    return list_full_data


def even_odd_day():
    for k in range(count_links()):
        file = pd.read_csv(f'csv_file/{k}.csv')
        list_full_data = get_data(file)
        even = []  # Чётные
        odd = []  # Нечётный

        day_of_the_week = create_days_of_the_week()

        group_number = [*file["0"]]

        d = 0

        # Получаем данные из списка
        for i in list_full_data:

            # Записываем занятия на нечётные дни
            temp = [group_number[d]]
            for j in i[1::2]:
                temp.append(j)
            odd.append(day_of_the_week)
            odd.append(temp)
            odd.append(["\n\n" for _ in range(len(temp))])

            # Записываем занятия на чётные дни
            temp = [group_number[d]]
            for j in i[2::2]:
                temp.append(j)
            even.append(day_of_the_week)
            even.append(temp)
            even.append(["\n\n" for _ in range(len(temp))])

            d += 1

        create_dir('csv_odd')
        create_dir('csv_even')

        sub_str_group_number = ""

        # Получаем номера групп для дальнейшей записи их в имя файла
        for f in group_number:
            str_format_f = str(f).replace("\n\n", "")

            sub_str_group_number += str_format_f
            sub_str_group_number += " "

        pd.DataFrame(odd).to_csv(f'csv_odd/{sub_str_group_number}odd(чётная неделя).csv', mode="w")
        pd.DataFrame(even).to_csv(f'csv_even/{sub_str_group_number}even(нечётная неделя).csv', mode="w")
        pd.DataFrame(odd).to_csv(f'csv_odd/{k}.csv', mode="w")
        pd.DataFrame(even).to_csv(f'csv_even/{k}.csv', mode="w")


def main():
    even_odd_day()


if __name__ == "__main__":
    main()