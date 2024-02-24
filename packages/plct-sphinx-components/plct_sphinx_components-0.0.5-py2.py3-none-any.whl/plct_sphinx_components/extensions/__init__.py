import os

modules = ['notes', 'multiple_choice', 'fill_in_the_blank', 'py_code', 'python_kernel', 'database_queries']

def static_dirs():
    basedir = os.path.dirname(__file__)
    subdirs = ['js','css', 'images', 'misc']
    dirs0 = [basedir + '/' + m + '/' + s for m in modules for s in subdirs]
    dirs = [dir for dir in dirs0 if os.path.exists(dir)]
    return dirs
