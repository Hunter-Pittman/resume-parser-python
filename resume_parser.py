import os
import argparse
import csv
import PyPDF2
import time, datetime

class Resume:
    def __init__(self, filename, count):
        self.filename = filename
        self.count = count

def search_pdf(pdf_path, keywords):
    analyzed_resumes = []
    for file in os.listdir(pdf_path):
        if file.endswith(".pdf"):
            count = []
            filename = os.path.join(pdf_path, file)
            with open(filename, 'rb') as f:
                pdf_reader = PyPDF2.PdfFileReader(f)
                pdf_text = ""
                for page in pdf_reader.pages:
                    pdf_text += page.extractText()
            for keyword in keywords:
                count.append(pdf_text.lower().count(keyword.lower()))
            analyzed_resumes.append(Resume(filename, count))
    return analyzed_resumes

def generate_csv(analyzed_resumes, keywords, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Filename"] + keywords + ["Total"])
        for resume in analyzed_resumes:
            total = sum(resume.count)
            writer.writerow([resume.filename] + resume.count + [total])


def wordlist_separate(keyword_list_file):
    with open(keyword_list_file, 'r') as f:
        keywords = f.read().splitlines()
    return keywords

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Parse PDF resumes and generate a CSV report")
    parser.add_argument('-p', '--pdf-path', required=True, help='Specify directory containing PDF resume files')
    parser.add_argument('-k', '--keyword-list', required=True, help='Specify file with keywords. Each keyword and/or phrase should be separated by a new line')
    parser.add_argument('-o', '--output-csv', required=True, help='Specify the full path where the CSV output will be saved. This should be a path, not a file name')
    args = parser.parse_args()

    if not os.path.isdir(args.pdf_path):
        print("PDF path does not exist!")
        exit()

    if not os.path.isfile(args.keyword_list):
        print("Keyword list file does not exist!")
        exit()

    if not os.path.isdir(args.output_csv):
        print("Output CSV path does not exist!")
        exit()

    keywords = wordlist_separate(args.keyword_list)
    analyzed_resumes = search_pdf(args.pdf_path, keywords)

    
    d = datetime.datetime.now()

    generate_csv(analyzed_resumes, keywords, args.output_csv + d + "parsed_resume.csv")
