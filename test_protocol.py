import os
import argparse
import warnings
from bs4 import BeautifulSoup
from src.usdm4_legacy import USDM4Legacy

#warnings.simplefilter("always")

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
    if not input_path:
        input_path = os.getcwd()
    root_filename, file_extension = os.path.splitext(tail)
    full_input_filename = os.path.join(input_path, tail)
    full_output_filename = os.path.join(input_path, f"{root_filename}.html")

    print("")
    print(f"Input path is: {full_input_filename}")
    print(f"Output file is: {full_output_filename}")
    print("")
    legacy = USDM4Legacy()
    legacy.from_pdf(full_input_filename)
    print(f"Errors: {legacy.errors.dump(0)}")
    save_html(full_output_filename, legacy._import._html)