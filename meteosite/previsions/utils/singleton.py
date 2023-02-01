# /--------------------------------------------------------------------\
#    Nicolas Georgemel
#    Coder pour changer de vie : https://coder-pour-changer-de-vie.com
# \--------------------------------------------------------------------/
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
