import os

def config(k):
    with open(f'/configs/default/es-index-names/{k}', 'r') as f:
        return f.read()


def main():
    print("hello")

    test = config("INDEX_AIRQUALITY")
    if test is None:
        return "Environment variable INDEX_AIRQUALITY is not set"

    return test