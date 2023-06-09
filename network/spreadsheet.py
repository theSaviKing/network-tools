import pandas as pd
from .site_config import SiteConfiguration
from .__utils__ import get_config_filename
from os.path import isfile
from blessed.win_terminal import Terminal

term = Terminal()


def generate_spreadsheet_template():
    """
    Generates a spreadsheet template for access point configurations.

    This function prompts the user to enter a configuration file, loads the site configuration,
    and generates a spreadsheet template with columns for access point name, serial number (SN),
    MAC address, and IP address. The template is saved as an Excel file.

    Note: The function relies on the `pandas` library for generating and manipulating the spreadsheet.
    """
    site = SiteConfiguration(
        get_config_filename("Enter config file to generate spreadsheet for:  ")
    )

    print("\nGenerating spreadsheet...\n", flush=True)

    # Create the template with column headers
    template = [["AP Name", "SN", "MAC", "IP Address"]]

    # Add access point information to the template
    template.extend(
        [config.env["name"], "", "", config.env["ipaddr"]] for config in site.configs
    )

    # Convert the template to a pandas DataFrame
    template = pd.DataFrame(template)

    print("Spreadsheet template generated.\n")

    # Prompt the user for the destination file name
    destination = (
        input("Enter the name of the destination for the Excel file (without .xlsx):  ")
        + ".xlsx"
    )

    # Write the template to an Excel file
    writer = pd.ExcelWriter(destination, engine="xlsxwriter")
    template.to_excel(writer, header=False, index=False)
    worksheet = writer.sheets["Sheet1"]

    # Set column widths
    worksheet.set_column(0, 3, 20)

    writer.close()

    print(f"Successfully created SN/MAC spreadsheet template at '{destination}'")


def merge_spreadsheets():
    def error_print(text):
        print(term.clear_eol + text + term.move_up + term.move_x(0), end="")

    print(
        "Enter filepath for each spreadsheet fragment. Type 'done' to stop entering filenames..."
    )
    fragments = []
    count = 1
    while (file := input(f"└── Fragment #{count}:  " + term.clear_eol)) not in [
        "done",
        "",
    ]:
        if not isfile(file):
            error_print(f"File '{file}' does not exist.")
        elif file.lower().split(".")[-1] != "xlsx":
            error_print(f"File '{file}' is not a valid spreadsheet.")
        else:
            print(term.move_up + term.move_x(0) + "├")
            fragments.append(file)
            count += 1
    print(term.move_up(2) + "└\n" + term.clear_eol)

    def load_spreadsheet(filepath):
        return pd.read_excel(filepath)

    merged = load_spreadsheet(fragments[0])
    for sheet in fragments[1:]:
        df = load_spreadsheet(sheet)
        merged = pd.concat([merged, df], ignore_index=True)
    new_df = [["AP Name", "SN", "MAC", "IP Address"]]
    for _, row in merged.iterrows():
        if pd.notnull(row[1]):
            new_df.append(row.to_list())
    merged_df = pd.DataFrame(new_df[1:], columns=new_df[0]).sort_values("AP Name")
    merged_string = merged_df.to_string(max_rows=7)
    print("Spreadsheet generated:\n\n", merged_string, "\n")

    destination = (
        input("Enter the name of the destination for the Excel file (without .xlsx):  ")
        + ".xlsx"
    )
    writer = pd.ExcelWriter(destination, engine="xlsxwriter")
    merged_df.to_excel(writer, header=False, index=False)
    worksheet = writer.sheets["Sheet1"]
    worksheet.set_column(0, 3, 20)
    writer.close()

    print(f"\nSuccessfully merged {len(fragments)} spreadsheets to '{destination}'.")


if __name__ == "__main__":
    merge_spreadsheets()
