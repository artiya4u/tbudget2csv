import csv
import os
import sys
import re

from fixtext import fix_align


def thai_number_to_arabic(thai_number):
    """
    Convert Thai number to Arabic number using ord() and chr()
    :param thai_number:
    :return:
    """
    arabic_number = ''
    for c in thai_number:
        if 3664 <= ord(c) <= 3673:
            arabic_number += chr(ord(c) - 3664 + 48)
        elif c == ',':
            arabic_number += ''
        else:
            arabic_number += c

    return arabic_number


if __name__ == '__main__':
    os.system(f'pdftotext -layout {sys.argv[1]}')
    text_file_name = sys.argv[1].replace('.pdf', '.txt')
    records = []
    with open(text_file_name) as text_file:
        lines = text_file.readlines()
        budget_name = ''
        is_record = False
        section = ''
        organization = ''
        is_org = False
        for line in lines:
            line_strip_arabic = thai_number_to_arabic(line.strip())
            if line_strip_arabic.startswith('มาตรา'):
                section = line_strip_arabic[0:line_strip_arabic.find(' ', 6)]

            if re.match("\d+\.", line_strip_arabic):
                organization = ''
                is_org = True

            if is_org:
                organization += line_strip_arabic

            if line_strip_arabic.endswith('บาท คือ') or line_strip_arabic.endswith('ประกอบด้วย'):
                is_org = False

            if re.match("\(.+\)", line_strip_arabic):
                budget_name = ''
                is_record = True

            if line_strip_arabic.endswith('บาท'):
                amount_strip = line_strip_arabic.replace(' บาท', '')
                amount = re.findall("\d+", amount_strip)[-1]
                budget_name += amount_strip.replace(amount, '').strip()
                budget_name = budget_name[budget_name.find(' ', 0) + 1:]

                find_end = organization.find(' รวม')
                if find_end == -1:
                    find_end = organization.find('ให้')

                organizationStrip = organization[organization.find(' ', 0):find_end].strip().replace(' ', '')
                b = {
                    'section': section,
                    'organization': organizationStrip,
                    'name': fix_align(budget_name),
                    'amount': amount
                }
                budget_name = ''
                if is_record:
                    print(b)
                    records.append(b)
                is_record = False

            if is_record and not is_org:
                budget_name += line_strip_arabic

        if len(records) > 0:
            csv_file_name = sys.argv[1].replace('.pdf', '.csv')
            f = open(csv_file_name, 'w')
            w = csv.DictWriter(f, records[0].keys())
            w.writerows(records)
            f.close()
