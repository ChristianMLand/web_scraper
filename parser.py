# import requests # not used just yet
from bs4 import BeautifulSoup
import xlsxwriter

def filter_down_tags(tag):
    if tag.strong:
        tag = tag.strong
    if tag.span:
        tag = tag.span
    return tag

def parse_table(soup):
    '''
    Lots of inconsistencies in the html structure made this file much 
    more complicated than it needed to be, if the original html was cleaned
    up this function would be about half as complex
    '''
    table = soup.find_all("table")[1]
    rows = table.find_all("tr")
    rows_dict = {}
    for i in range(14):
        row = rows[i]
        tds = row.find_all("td")
        row_data = []
        for j in range(len(tds)):
            td = tds[j]
            td_str = ''
            if td.p:
                p_list = []
                for p in td.find_all("p"):
                    p = filter_down_tags(p)
                    p_str = p.decode_contents()
                    p_str = p_str.split("<")[0]
                    p_list.append(p_str)
                td_str = ''.join(p_list)
            td = filter_down_tags(td)
            if td.span:
                td = td.span
            if not td_str:
                td_str = td.decode_contents()
            td_str = td_str.replace('\xa0', "").replace("\n", "").strip()
            if j == 0:
                lines = td_str.split('/')
                for line in lines:
                    rows_dict[line] = row_data
            else:
                row_data.append(td_str)
    return rows_dict

def format_table(table_dict):
    new_table = {}
    line_types = None
    for i, line in enumerate(table_dict):
        row = table_dict[line]
        if i == 0:
            line_types = row
        else:
            new_table[line] = {
                "picks" : [],
                "drops" : []
            }
            for j, val in enumerate(row):
                if j % 2 == 0 and val == "YES":
                    new_table[line]["drops"].append(line_types[j].split(" ")[0])
                elif val == "YES":
                    new_table[line]["picks"].append(line_types[j].split(" ")[0])
    return new_table

def write_to_worksheet(worksheet, formatted_table):
    #TODO refactor 
    worksheet.write("A1", "")
    table_count = 0
    for i, line in enumerate(formatted_table):
        worksheet.write(0, i + table_count * 2, f"{line} picks")
        for j, pick in enumerate(formatted_table[line]['picks']):
            worksheet.write(j + 1, i + table_count * 2, pick)
        worksheet.write(0, i + table_count * 2 + 1, f"{line} drops")
        for j, drop in enumerate(formatted_table[line]['drops']):
            worksheet.write(j + 1, i + table_count * 2 + 1, drop)
        table_count += 1

def main():
    file = open(file='terminal_table.html', mode='r')
    soup = BeautifulSoup(markup=file, features='html.parser')
    table_dict = parse_table(soup)
    formatted_table = format_table(table_dict)

    workbook = xlsxwriter.Workbook("sample_output.xlsx")
    worksheet = workbook.add_worksheet("picks and drops")

    for k,v in formatted_table.items():
        print(k, v)

    write_to_worksheet(worksheet, formatted_table)
    workbook.close()


if __name__ == "__main__":
    main()