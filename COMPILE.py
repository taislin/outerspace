# You will need mingw64 and nuitka installed to run this.

import os
import sys
import shutil
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

if __name__ == '__main__':
    print("Cleaning existing temp files...")
    if os.path.isdir('outerspace.dist'):
        shutil.rmtree('outerspace.dist')
    if os.path.isdir('outerspace.build'):
        shutil.rmtree('outerspace.build')
    if os.path.isdir('outerspace'):
        shutil.rmtree('outerspace')
    if os.path.isfile('outerspace.zip'):
        os.remove('outerspace.zip')
    print("Compiling the game into an executable...")
    os.system('python2 -m nuitka --mingw64 outerspace.py --standalone --follow-imports --plugin-enable=multiprocessing --windows-icon="client\\resources\\icon48.ico"')
    print("Copying dependencies...")
    shutil.copytree('server', 'outerspace.dist\\server')
    shutil.copytree('client', 'outerspace.dist\\client')
    shutil.move('outerspace.dist', 'outerspace')
    print("Zipping the folder...")
    zipf = zipfile.ZipFile('outerspace.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('outerspace/', zipf)
    zipf.close()
    print("Cleaning used temp files...")
    if os.path.isdir('outerspace.dist'):
        shutil.rmtree('outerspace.dist')
    if os.path.isdir('outerspace.build'):
        shutil.rmtree('outerspace.build')
    if os.path.isdir('outerspace'):
        shutil.rmtree('outerspace')
    print("Done!")