import csv
import os
import sys
import re

from fixtext import fix_align

project_title_prefix = ('ผลผลิต', 'แผนงาน', 'โครงการ')


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
        count = 0
        lines = text_file.readlines()
        is_section_6_2 = False
        is_row = False
        org_name = None
        sub_org_name = None
        plan_name = None
        project_name = ''
        personnel_budget = 0
        operational_budget = 0
        investing_budget = 0
        subsidy_budget = 0
        other_budget = 0
        sum_budget = None
        for line in lines:
            if line.find((' ' * 30) + 'กระทรวง') > 0 or line.find((' ' * 30) + 'สานักนายก') > 0:
                org_name = line.strip()
                sub_org_name = lines[count + 1].strip()

            count += 1
            segments = line.split('  ')
            segments = list(filter(lambda x: x != '', segments))
            segments = list(map(str.strip, segments))
            segments = list(map(fix_align, segments))
            segments = list(map(replace_dash, segments))

            # Inside 6.2 section loop fill all value
            if line.startswith('รวม'):
                is_row = True
                continue
            # Condition find for section 6.2
            if segments[0].find('จาแนกตามแผนงาน ผลผลิต/โครงการ และงบรายจ่าย') > 0:
                is_section_6_2 = True
                continue

            if is_section_6_2 and is_row:
                print(segments)
                no_number_title = re.sub(r'\d\.', '', segments[0]).strip()
                if no_number_title.startswith(project_title_prefix) \
                        or segments[0].find('รายละเอียดงบประมาณจาแนกตามแผนงาน') > 0:
                    if project_name != '' and sum_budget is not None:
                        is_plan = re.search(r'\d\.', project_name) is not None
                        project_budgets.append({
                            'org_name': org_name,
                            'sub_org_name': sub_org_name,
                            'project_name': project_name,
                            'is_plan': is_plan,
                            'personnel_budget': personnel_budget,
                            'operational_budget': operational_budget,
                            'investing_budget': investing_budget,
                            'subsidy_budget': subsidy_budget,
                            'other_budget': other_budget,
                            'sum_budget': sum_budget,
                        })
                        project_name = ''
                if no_number_title.startswith(project_title_prefix):
                    project_name = segments[0]
                else:
                    project_name += segments[0]
                if len(segments) == 7:
                    personnel_budget = segments[1]
                    operational_budget = segments[2]
                    investing_budget = segments[3]
                    subsidy_budget = segments[4]
                    other_budget = segments[5]
                    sum_budget = segments[6]

    if len(project_budgets) > 0:
        csv_file_name = 'budget_by_project.csv'
        f = open(csv_file_name, 'w')
        w = csv.DictWriter(f, project_budgets[0].keys())
        w.writerows(project_budgets)
        f.close()
