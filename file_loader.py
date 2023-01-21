import os;
import json;

class FileLoader:

    # Check if file exists in project
    @staticmethod
    def exists(relative_path: str):
        if os.path.exists(relative_path):
            return True;

        return False;

    # Check if path is a file
    @staticmethod
    def is_file(relative_path: str):
        if os.path.isfile(relative_path):
            return True;

        return False;

    # Load a project file
    @staticmethod
    def load(relative_path: str):
        if not FileLoader.exists(relative_path):
            raise FileNotFoundError();

        contents = open(relative_path).read();

        if relative_path.endswith(".json"):
            return json.loads(contents);

        return contents;

    # Save text file to the file system
    @staticmethod
    def save(relative_path: str, contents: str):
        with open(relative_path, "w") as file_out:
            file_out.write(contents);

    # Create a new text file
    @staticmethod
    def create(relative_path: str, contents: str):
        if FileLoader.exists(relative_path):
            raise Exception("File already exists");

        with open(relative_path, "w") as file_out:
            file_out.write(contents);

    # List all files in a folder
    @staticmethod
    def list(relative_path: str):
        if not FileLoader.exists(relative_path):
            raise Exception("Path does not exist");

        files = os.listdir(relative_path);

        parsed_files = [
            file for file in files
                if FileLoader.is_file(relative_path + '/' + file)
        ];

        return parsed_files;
