import sys, os

def resource_path(*parts):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    print(os.path.join(base, *parts))
    return os.path.join(base, *parts)