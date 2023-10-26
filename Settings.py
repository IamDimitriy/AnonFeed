class Settings:
    def __init__(self, **settings):
        self.token = settings["token"]
        self.init_function_name = settings["init_function_name"]
        self.init_file_names = settings["init_file_names"]
        self.salt = settings["salt"]
        self.iteration = int(settings["iteration"])
