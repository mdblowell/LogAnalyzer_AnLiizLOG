import os
import re

def analyze_log_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().lower()

    keywords = ['warning', 'error', 'severity']
    findings = {}

    for keyword in keywords:
        pattern = re.compile(r'({}\s*:\s*\d+\s*-\s*.+?\n)'.format(keyword))
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

def generate_kba_draft(findings):
    draft = 'New KBA Draft:\n\n'
    for keyword, matches in findings.items():
        if matches:
            draft += f'Problem:\n{matches[0]}\nSolution:\nTBD\n\n'
    return draft

upload = input("Please upload up to 3 log files into AnLiizLOG")

def main():
    file_paths = []  # TODO: Prompt the user to upload up to 3 log files

    for file_path in file_paths:
        if os.path.getsize(file_path) > 500 * 1024 * 1024:
            print(f'Warning: File {file_path} is larger than 500MB and will be skipped.')
            continue

        findings = analyze_log_file(file_path)
        report = generate_report(findings)
        print(report)

        kba_draft = generate_kba_draft(findings)
        print(kba_draft)

if __name__ == '__main__':
    main()