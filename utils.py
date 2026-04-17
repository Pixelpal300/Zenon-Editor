import sys, os

def resource_path(*paths):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, *paths)