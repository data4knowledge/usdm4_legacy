import os
import argparse
from bs4 import BeautifulSoup
from src.usdm4_legacy import USDM4Legacy

def save_html(file_path, result):
    soup = BeautifulSoup(result, "html.parser")
    data = soup.prettify()
    with open(file_path, "w") as f:
        f.write(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='USDM Simple Legacy Protocol Test Program',
        description='Import a legacy PDF protocol',
        epilog='Note: Not that sophisticated! :)'
    )
    parser.add_argument('filename', help="The name of the protocol PDF file.") 
    args = parser.parse_args()
    filename = args.filename
    
    input_path, tail = os.path.split(filename)
    root_filename = tail.replace(".json", "")
    full_filename = filename
    output_path = input_path
    full_output_filename = os.path.join(output_path, f"{root_filename}.html")

    print("")
    print(f"Output path is: {output_path}")
    print(f"Output file is: {full_output_filename}")
    print("")
    legacy = USDM4Legacy()
    legacy.from_pdf(full_filename)
    html = legacy._import._doc
    save_html(full_output_filename, html)