# -coding: UTF-8
import os


if __name__ == '__main__':
    os.system("python ../../stickynotes/manage.py makemigrations")
    os.system("python ../../stickynotes/manage.py migrate")