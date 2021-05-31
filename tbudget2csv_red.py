import csv
import glob
import os
import re

from fixtext import fix_align

project_title_prefix = ('ผลผลิต', 'แผนงาน', 'โครงการ')
org_prefix = [(' ' * 30) + 'กระทรวง', (' ' * 30) + 'สานักนายก', (' ' * 30) + 'องค์กรปกครอง', (' ' * 30) + 'จังหวัดและก']
section_6_2_prefix = [
    '6.2 จาแนกตามแผนงาน ผลผลิต/โครงการ และงบรายจ่าย',
    '6.2 จําแนกตามแผนงาน ผลผลิต/โครงการ และงบรายจ่าย',
    '6. สรุปงบประมาณรายจ่ายประจาปี งบประมาณ'
]


def replace_dash(text):
    if text == '-':
        return '0'
    else:
        return text


def convert_table_6(pdf_budget_file):
    print(f'Start convert: {pdf_budget_file}')
    os.system(f'pdftotext -layout {pdf_budget_file}')
    text_file_name = pdf_budget_file.replace('.pdf', '.txt')
    project_budgets = []
    with open(text_file_name) as text_file:
        count = 0
        lines = text_file.readlines()
        is_section_6 = False
        is_row = False
        org_name = None
        sub_org_name = None
        project_name = ''
        personnel_budget = 0
        operational_budget = 0
        investing_budget = 0
        subsidy_budget = 0
        other_budget = 0
        sum_budget = None
        for line in lines:
            if any(x in line for x in org_prefix):
                org_name = line.strip()
                sub_org_name = lines[count + 1].strip()

            count += 1
            segments = line.split('  ')
            segments = list(filter(lambda x: x != '', segments))
            segments = list(map(str.strip, segments))
            segments = list(map(fix_align, segments))
            segments = list(map(replace_dash, segments))

            # Condition find for section 6.2
            if any(line.startswith(x) for x in section_6_2_prefix):
                is_section_6 = True
                continue

            # Inside 6.2 section loop fill all value
            if line.startswith('รวม') and is_section_6:
                is_row = True
                continue

            if is_section_6 and is_row:
                print(segments)
                no_number_title = re.sub(r'\d\.', '', segments[0]).strip()
                if no_number_title.startswith(project_title_prefix) \
                        or segments[0].find('7. รายละเอียดงบประมาณจ') >= 0:
                    if project_name != '' and sum_budget is not None and sum_budget != 'รวม':
                        is_plan = re.search(r'\d\.', project_name) is not None
                        plan = {
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
                        }
                        print(plan)
                        project_budgets.append(plan)
                        project_name = ''
                        sum_budget = None

                if segments[0].find('7. รายละเอียดงบประมาณจ') >= 0:
                    is_row = False
                    is_section_6 = False
                    sum_budget = None
                    continue

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
        try:
            os.makedirs('output/')
        except OSError:
            pass
        csv_file_name = 'output/' + pdf_budget_file.split('/')[1].replace('.pdf', '.csv')
        f = open(csv_file_name, 'w')
        w = csv.DictWriter(f, project_budgets[0].keys())
        w.writerows(project_budgets)
        f.close()


if __name__ == '__main__':
    pdf_path = 'budget-pdf/'
    list_of_files = sorted(filter(os.path.isfile, glob.glob(pdf_path + '*.pdf')))
    for file in list_of_files:
        if file.endswith('.pdf'):
            convert_table_6(file)
