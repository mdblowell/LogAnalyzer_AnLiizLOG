import os
import re
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import getpass

def analyze_log_file(file_path, keywords):
    with open(file_path, 'r') as file:
        content = file.read()

    findings = {}

    for keyword in keywords:
        pattern = re.compile(r'(\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}\.\d{{3}} \w{{3}} \[\d+\] {}: .*?(?=\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}\.\d{{3}} \w{{3}} \[\d+\] |$))'.format(keyword.upper()), re.DOTALL)
        matches = pattern.findall(content)
        findings[keyword] = matches

    return findings

def generate_report(findings):
    report = ''
    for keyword, matches in findings.items():
        report += f'{keyword.upper()}:\n'
        for match in matches:
            report += f'  {match}\n'
        report += f'Number of occurrences: {len(matches)}\n\n'
    return report

def generate_kba_draft(findings, application_name, application_version, product_name):
    create_kba = input('Do you want to create a KBA draft? (yes/no): ')
    if create_kba.lower() != 'yes':
        return

    draft = 'New KBA Draft:\n\n'
    for keyword, matches in findings.items():
        if matches:
            draft += f'Title: {keyword.capitalize()} in {product_name}\n'
            draft += f'Symptom: {matches[0]}\n'
            draft += f'Environment: {application_name} v{application_version}\n'
            draft += f'Product: {product_name}\n'
            draft += f'Keywords: {keyword}\n\n'

            directory = 'C:\\AnLiizLOG'
            if not os.path.exists(directory):
                os.makedirs(directory)

            file_name = f'{datetime.now().strftime("%Y%m%d")}_{keyword}_{getpass.getuser()}.txt'
            file_path = os.path.join(directory, file_name)

            counter = 1
            while os.path.exists(file_path):
                file_name = f'{datetime.now().strftime("%Y%m%d")}_{keyword}_{getpass.getuser()}{counter}.txt'
                file_path = os.path.join(directory, file_name)
                counter += 1

            with open(file_path, 'w') as file:
                file.write(draft)

def upload_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(title='Please select up to 3 log files',
                                             filetypes=[('Log files', '*.log'), ('Text files', '*.txt'), ('JSON files', '*.json')],
                                             initialdir='/',
                                             multiple=True)
    return file_paths

def main():
    application_name = ''  # TODO: Get the application name
    application_version = ''  # TODO: Get the application version
    product_name = ''  # TODO: Get the product name

    file_paths = upload_files()

    keywords = ['warning', 'error', 'severity', 'statement', 'fatal', 'detail', 'log']
    additional_keywords = input('Enter additional keywords to search for, separated by commas: ')
    keywords.extend([keyword.strip() for keyword in additional_keywords.split(',') if keyword.strip()])

    ignore_keywords = input('Enter keywords to ignore, separated by commas: ')
    ignore_keywords = [keyword.strip() for keyword in ignore_keywords.split(',') if keyword.strip()]
    keywords = [keyword for keyword in keywords if keyword not in ignore_keywords]

    for file_path in file_paths:
        if os.path.getsize(file_path) > 500 * 1024 * 1024:
            print(f'Warning: File {file_path} is larger than 500MB and will be skipped.')
            continue

        findings = analyze_log_file(file_path, keywords)
        report = generate_report(findings)
        print(report)

        generate_kba_draft(findings, application_name, application_version, product_name)

if __name__ == '__main__':
    main()