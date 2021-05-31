import csv
import os
import sys
import re

from fixtext import fix_align

project_title = ('ผลผลิต', 'แผนงาน', 'โครงการ')


def replace_dash(text):
    if text == '-':
        return '0'
    else:
        return text


if __name__ == '__main__':
    os.system(f'pdftotext -layout {sys.argv[1]}')
    text_file_name = sys.argv[1].replace('.pdf', '.txt')
    project_budgets = []
    with open(text_file_name) as text_file:
        lines = text_file.readlines()
        is_section_6_2 = False
        project_budget = None
        for line in lines:
            segments = line.split('  ')
            segments = list(filter(lambda x: x != '', segments))
            segments = list(map(str.strip, segments))
            segments = list(map(fix_align, segments))
            segments = list(map(replace_dash, segments))

            # Inside 6.2 section loop fill all value
            if is_section_6_2:
                print(segments)
                no_number_title = re.sub(r'\d', '', segments[0]).replace('.', '').strip()
                if len(segments) == 7:
                    if project_budget is not None and project_budget['project_name'] != 'รวมทั้งสิ้น':
                        project_budgets.append(project_budget)
                    if no_number_title.startswith(project_title):
                        project_budget = {
                            'project_name': segments[0],
                            'personnel_budget': segments[1],
                            'operational_budget': segments[2],
                            'investing_budget': segments[3],
                            'subsidy_budget': segments[4],
                            'other_budget': segments[5],
                            'sum_budget': segments[6],
                        }
                    else:
                        pre = ''
                        if project_budget is not None:
                            pre = project_budget['project_name']

                        project_budget = {
                            'project_name': pre + segments[0],
                            'personnel_budget': segments[1],
                            'operational_budget': segments[2],
                            'investing_budget': segments[3],
                            'subsidy_budget': segments[4],
                            'other_budget': segments[5],
                            'sum_budget': segments[6],
                        }

                # Concat the project name from multiple lines
                if len(segments) == 1 and project_budget is not None and not no_number_title.startswith(project_title):
                    project_budget['project_name'] = project_budget['project_name'] + segments[0]

            # Condition find for section 6.2
            if segments[0].find('จาแนกตามแผนงาน ผลผลิต/โครงการ และงบรายจ่าย') > 0:
                is_section_6_2 = True

            # Condition find for section 7.2 to end 6.2
            if segments[0].find('รายละเอียดงบประมาณจาแนกตามแผนงาน') > 0:
                is_section_6_2 = False
                if project_budget is not None and project_budget['project_name'] != 'รวมทั้งสิ้น':
                    project_budgets.append(project_budget)
                    project_budget = None

    if len(project_budgets) > 0:
        csv_file_name = 'budget_by_project.csv'
        f = open(csv_file_name, 'w')
        w = csv.DictWriter(f, project_budgets[0].keys())
        w.writerows(project_budgets)
        f.close()
