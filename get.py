import pandas as pd
import requests as rq
import bs4
import pdfplumber

from different_actions import create_dir, count_links

main_link = "https://polyt-amur.ru/studentu/raspisanie"


def main_code_html():
    req = rq.get(main_link)

    with open("new_file.html", "w", encoding="utf-8") as file:
        file.write(req.text)


def link_pdf_file():
    with open("new_file.html", "r", encoding="utf-8") as file:
        info_file = file.read()

    soup = bs4.BeautifulSoup(info_file, 'lxml')

    main_div = soup.find_all('div', class_="su-list")

    links = []

    for i in main_div:
        links.append(i.find_all("li"))

    create_dir("link_pdf")

    with open("link_pdf/link.txt", "w", encoding="utf-8") as file_pdf:

        for i in links:
            for j in i:
                file_pdf.write(j.find("a")["href"] + "\n")


def get_links():
    links = []

    with open("link_pdf/link.txt", "r", encoding="utf-8") as file_pdf:
        for i in file_pdf.readlines():
            links.append(i.replace("\n", ""))

    return links


def save_pdf_local_disc():
    create_dir("pdf")

    links = get_links()

    d = 0

    for i in links:

        req = rq.get(i.replace("\n", ""))

        with open(f"pdf/file{d}.pdf", "wb") as file2:
            file2.write(req.content)

        d += 1


def write_text_pdf_in_csv_file():

    create_dir("csv_file")

    d = 0

    for i in range(count_links()):
        full_data = []
        temp_list = []

        with pdfplumber.open(f"pdf/file{i}.pdf") as file:
            for page in file.pages:
                tables = page.extract_table()
                for table in tables:
                    temp_list.append(table)

        for j in range(len(temp_list)):

            if (j == len(temp_list) - 1 and
                    temp_list[j][1] is not None):
                full_data.append(['' for _ in range(len(temp_list[j]))])

            elif (j != len(temp_list) - 1 and
                  temp_list[j][2::] == ['' for _ in range(len(temp_list[j][2::]))] and
                  temp_list[j+1][1] is not None and
                  temp_list[j][1] is not None):

                full_data.append(['' for _ in range(len(temp_list[j]))])

            full_data.append(temp_list[j])

        new_full_data = []

        for j in range(2, len(full_data[0])):
            temp_data = []
            for k in range(len(full_data)):
                if full_data[k][j] is None:
                    if full_data[k-1][j] == "":
                        temp_data.append("Пусто")
                    else:
                        temp_data.append(full_data[k-1][j].replace("\n", '\n\n'))
                elif full_data[k][j] == "":
                    temp_data.append("Пусто")
                else:
                    temp_data.append(full_data[k][j].replace("\n", '\n\n'))

            new_full_data.append(temp_data)

        df = pd.DataFrame(new_full_data)

        df.to_csv(f"csv_file/{d}.csv", mode="w", columns=[i for i in range(len(full_data))])

        d += 1


def main():
    main_code_html()
    link_pdf_file()
    save_pdf_local_disc()
    write_text_pdf_in_csv_file()


if __name__ == "__main__":
    main()