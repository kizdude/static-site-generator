import os, shutil
    
from generate_page import generate_pages_recursive

def delete_public():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")

def create_static_directories(path_from, path_to):
    source_directories = os.listdir(path_from)
    for directory in source_directories:
        if os.path.isfile(os.path.join(path_from, directory)):
            copy_file(os.path.join(path_from, directory), os.path.join(path_to, directory))
        else:
            os.mkdir(os.path.join(path_to, directory))
            create_static_directories(os.path.join(path_from, directory), os.path.join(path_to, directory))

def copy_file(path_from, path_to):
    shutil.copy(path_from, path_to)

def copy_static_to_public(): 
    create_static_directories("static/content/", "public")

def main():
    delete_public()
    copy_static_to_public()
    generate_pages_recursive("static/content/", "template.html", "public/")

main()