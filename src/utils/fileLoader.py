import os;
import json;

class FileLoader:

    # Check if file exists in project
    @staticmethod
    def exists(relativePath: str):
        if os.path.exists(relativePath):
            return True;

        return False;

    # Check if path is a file
    @staticmethod
    def isFile(relativePath: str):
        if os.path.isfile(relativePath):
            return True;

        return False;

    # Load a project file
    @staticmethod
    def load(relativePath: str):
        if not FileLoader.exists(relativePath):
            raise FileNotFoundError();

        contents = open(relativePath).read();

        if relativePath.endswith(".json"):
            return json.loads(contents);

        return contents;

    # Save text file to the file system
    @staticmethod
    def save(relativePath: str, contents: str):
        with open(relativePath, "w") as fileOut:
            fileOut.write(contents);

    # Create a new text file
    @staticmethod
    def create(relativePath: str, contents: str):
        if FileLoader.exists(relativePath):
            raise Exception("File already exists");

        with open(relativePath, "w") as fileOut:
            fileOut.write(contents);

    # List all files in a folder
    @staticmethod
    def list(relativePath: str):
        if not FileLoader.exists(relativePath):
            raise Exception("Path does not exist");

        files = os.listdir(relativePath);

        parsedFiles = [
            file for file in files
                if FileLoader.isFile(relativePath + '/' + file)
        ];

        return parsedFiles;
