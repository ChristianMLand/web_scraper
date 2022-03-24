# import requests # not used just yet
from bs4 import BeautifulSoup
import xlsxwriter

def filter_down_tag(tag):
    if tag.strong:
        tag = tag.strong
    if tag.span:
        tag = tag.span
    return tag

def parse_table_into_dict(table):
    # Lots of inconsistencies in the html structure made this file much 
    # more complicated than it needed to be, if the original html was written
    # properly this function would be about half as complex ( see below )
    rows = table.find_all("tr")
    table_dict = {}
    for i, tr in enumerate(rows):
        if i < 14:# only parse data from the rows we care about
            tds = tr.find_all("td")
            row_data = []
            for j, td in enumerate(tds):
                td_str = ''
                if td.p:
                    p_list = []
                    for p in td.find_all("p"):
                        p = filter_down_tag(p)# catch inner tags if they exist and filter them out
                        p_str = p.decode_contents()
                        p_str = p_str.split("<")[0]
                        p_list.append(p_str)
                    td_str = ''.join(p_list)
                td = filter_down_tag(td)
                if td.span:
                    td = td.span
                if not td_str:
                    td_str = td.decode_contents()
                td_str = td_str.replace('\xa0', "").replace("\n", "").strip()# discard any uneccessary special characters
                if j == 0:
                    lines = td_str.split('/')
                    for line in lines:
                        table_dict[line] = row_data
                else:
                    row_data.append(td_str)
    return table_dict

# def parse_table_into_dict(table):
#     # If website HTML was structured more consistently,
#     # the above function could be simplified to this
#     rows = table.find_all("tr")
#     table_dict = {}
#     for tr in rows:
#         tds = tr.find_all("td")
#         row_data = []
#         for j, td in enumerate(tds):
#             td = filter_down_tag(td)
#             td_str = td.decode_contents()
#             td_str = td_str.replace('\xa0', "").replace("\n", "").strip()
#             if j == 0:
#                 lines = td_str.split('/')
#                 for line in lines:
#                     table_dict[line] = row_data
#             else:
#                 row_data.append(td_str)
#     return table_dict

def format_table_dict(table_dict):
    new_table = {}
    line_types = None
    for i, line in enumerate(table_dict):
        row = table_dict[line]
        if i == 0:
            line_types = row
        else:
            new_table[line] = { "picks" : [], "drops" : [] }
            for j, val in enumerate(row):
                if val == "YES":
                    new_table[line]["drops" if j % 2 == 0 else "picks"].append(line_types[j].split(" ")[0])
    return new_table

def write_to_worksheet(worksheet, formatted_table):
    table_count = 0
    for i, line in enumerate(formatted_table):
        for j, key in enumerate(formatted_table[line]):
            worksheet.write(0, table_count * 2 + i + j, f"{line} {key}")
            for k, val in enumerate(formatted_table[line][key]):
                worksheet.write(k + 1, table_count * 2 + i + j, val)
        table_count += 1

def main():
    file = open(file='terminal_table.html', mode='r')
    soup = BeautifulSoup(markup=file, features='html.parser')
    table_dict = parse_table_into_dict(soup.find_all("table")[1])
    formatted_table = format_table_dict(table_dict)

    workbook = xlsxwriter.Workbook("sample_output.xlsx")
    worksheet = workbook.add_worksheet("picks and drops")

    write_to_worksheet(worksheet, formatted_table)
    workbook.close()


if __name__ == "__main__":
    main()