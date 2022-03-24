# import requests # not used just yet
from bs4 import BeautifulSoup
import xlsxwriter

def parse_table(soup):
    # This function can, and will be refactered, but the inconsistent formatting of the webpage
    # made parsing the table rather annoying. With a more consistent base html this function would be
    # about 1/4 as long and complex
    table = soup.find_all("table")[1]
    rows = table.find_all("tr")
    rows_dict = {}
    for i, row in enumerate(rows):
        if i < 14:
            tds = row.find_all("td")
            row_data = []
            line_cell = tds[0]
            if line_cell.p:
                line_cell = line_cell.p
            if line_cell.strong:
                line_cell = line_cell.strong
            if line_cell.span:
                line_cell = line_cell.span
            line_cell = line_cell.decode_contents()
            line_cell = line_cell.split('<')[0].strip()
            lines = line_cell.split('/')
            for line in lines:
                rows_dict[line] = row_data
            for j in range(1, len(tds)):
                line_cell = tds[j]
                td_str = line_cell.string
                if line_cell.p:
                    p_list = []
                    for p in line_cell.find_all("p"):
                        if p.strong:
                            p = p.strong
                        if p.span:
                            p = p.span
                        p_list.append(p.string)
                    td_str = ''.join(p_list)
                if line_cell.strong:
                    line_cell = line_cell.strong
                if line_cell.span:
                    line_cell = line_cell.span
                if not td_str:
                    td_str = line_cell.string
                td_str = td_str.replace('\xa0', "").replace("\n", "").strip()
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