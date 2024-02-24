class FileGen:
    def __init__(self):
        pass

    @staticmethod
    def create_file(name, content=None):
        with open(name, "w") as file:
            if content is not None:
                file.write(content)

    @staticmethod
    def create_files(file_names, content=None):
        for file_name in file_names:
            FileGen.create_file(file_name, content)
