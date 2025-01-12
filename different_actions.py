import os


def create_dir(dir_name: str):
    try:
        os.mkdir(dir_name)
    except:
        pass


def create_days_of_the_week():
    day_of_week = ['']
    sub = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]
    for i in sub:
        for _ in range(5):
            day_of_week.append(i)

    return day_of_week


def count_links():
    count = 0

    with open("link_pdf/link.txt", "r", encoding="utf-8") as file_pdf:
        for _ in file_pdf.readlines():
            count += 1

    return count