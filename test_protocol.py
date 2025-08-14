import os
import json
import argparse
import warnings
from bs4 import BeautifulSoup
from src.usdm4_legacy import USDM4Legacy
from usdm4.api.wrapper import Wrapper


# warnings.simplefilter("always")


def save_html(file_path, result):
    soup = BeautifulSoup(result, "html.parser")
    data = soup.prettify()
    with open(file_path, "w") as f:
        f.write(data)


def save_json(file_path, result: Wrapper):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(json.loads(result.to_json()), indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="USDM Simple Legacy Protocol Test Program",
        description="Import a legacy PDF protocol",
        epilog="Note: Not that sophisticated! :)",
    )
    parser.add_argument("filename", help="The name of the protocol PDF file.")
    args = parser.parse_args()
    filename = args.filename

    input_path, tail = os.path.split(filename)
    if not input_path:
        input_path = os.getcwd()
    root_filename, file_extension = os.path.splitext(tail)
    full_input_filename = os.path.join(input_path, tail)
    html_output_filename = os.path.join(input_path, f"{root_filename}.html")
    json_output_filename = os.path.join(input_path, f"{root_filename}.json")

    print("")
    print(f"Input path is: {full_input_filename}")
    print(f"HTML file is: {html_output_filename}")
    print(f"JSON file is: {json_output_filename}")
    print("")
    legacy = USDM4Legacy()
    wrapper: Wrapper = legacy.from_pdf(full_input_filename)
    print(f"Errors: {legacy.errors.count()}, {legacy.errors.error_count()}")
    print(f"Errors: {legacy.errors.dump(0)}")
    # save_html(html_output_filename, legacy._import._html)
    save_json(json_output_filename, wrapper)
