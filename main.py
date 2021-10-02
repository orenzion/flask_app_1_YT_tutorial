from logging import debug
from website import create_app
''' whenever we add the __init__.py inside a folder we define this folder as a package.
once we import this this folder/package (a package is a folder which contains multiple python files/modules,
each module contains functions and objects. a library is made of multiple packages) it automatically runs the __init__.py file and that's why we can import the modules which
were created in this file.  '''

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
