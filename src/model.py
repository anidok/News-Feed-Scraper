class Model:
    def __init__(self, *initial_data, **kwargs):
        for key in kwargs:
            setattr(self, key, kwargs[key])