import os;
import json;

class FileLoader:

    # Check if file exists in project
    @staticmethod
    def exists(relative_path: str):
        if os.path.exists(relative_path):
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


    @staticmethod
    def save(relative_path: str, contents: str):
        with open(relative_path, "w") as file_out:
            file_out.write(contents);


    @staticmethod
    def create(relative_path: str, contents: str):
        if FileLoader.exists(relative_path):
            raise Exception("File already exists");

        with open(relative_path, "w") as file_out:
            file_out.write(contents);