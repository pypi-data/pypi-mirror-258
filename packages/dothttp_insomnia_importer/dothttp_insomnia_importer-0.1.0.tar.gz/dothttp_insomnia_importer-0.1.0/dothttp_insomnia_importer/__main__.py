import os
import argparse

from dotextensions.server.models import Command

from .insomnia import ImportInsomniaCollection

def parse_arguments():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: Parsed command line arguments.
    """
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("input_file", type=str, help="The input file to process")
    parser.add_argument("directory", type=str, help="The directory to use")
    parser.add_argument(
        "--file_type",
        type=str,
        default="notebook",
        help="The type of the file (default: notebook)",
        choices=["notebook", "http"],
    )
    return parser.parse_args()


if __name__ == "__main__":
    """
    This script is used to import a insomina collection into http.

    It takes command line arguments for the input file, directory, and file type.
    The input file should be a insomnia collection file.
    The directory is the target directory where the imported collection will be saved.
    The file type can be either 'notebook' or 'http'.

    The script reads the input file, transforms the data to Postman format,
    and then creates a command to import the collection into Insomnia.
    The imported collection is saved in the specified directory.

    If the import is successful, it prints a success message.
    If there is an error during the import, it prints an error message.
    """

    # Parse the arguments
    args = parse_arguments()

    # Get the arguments
    input_file = args.input_file
    directory = args.directory
    file_type = args.file_type

    command_params = {
        "insomnia-collection": input_file,
        "directory": os.path.abspath(directory),
        "filetype": file_type,
        "save": True,
        "overwrite": True,
    }

    command = Command("insomnia_import", command_params, 1)

    result = ImportInsomniaCollection().run(command)

    # Read the input file
    if result.result.get("error", False):
        print(
            "Failed to import to insomnia with error %s" %
            result.result.get("error_message", "Unknown error"),
        )
    else:
        print("Imported Postman collection to Insomnia successfully.")
        print(
            f"Successfully imported to insomnia into directory {directory} with file type {file_type}"
        )
