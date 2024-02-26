from dotextensions.server.handlers.postman2http import ImportPostmanCollection
from dotextensions.server.models import Command

from .loader import transform_data


class ImportInsomniaCollection:
    def run(self, command):
        input_file = command.params.get("insomnia-collection")
        directory = command.params.get("directory")
        file_type = command.params.get("filetype")
        save = command.params.get("save", False)
        overwrite = command.params.get("overwrite", False)

        with open(input_file, "r") as file:
            input_file_data = file.read()
        # Transform the data to postman format
        postman_collection_format_data = transform_data(input_file_data, input_file)

        # create a command and run it
        command_params = {
            "postman-collection": postman_collection_format_data,
            # import postman expects absolute path
            "directory": directory,
            "save": save,
            "overwrite": overwrite,
            "filetype": file_type,
        }
        command = Command("insomnia_import", command_params, 1)
        result = ImportPostmanCollection().run(command)
        return result