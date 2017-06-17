import shutil
import os

# SOURCE_PATH = 'NODE3/F_Rai\'s/lan-tv/data'
# SOURCE_PATH = r"\\NODE3\F_Rai's\lan-tv\data"
REMOTE_PATH = r"//raspberrypi3/users"

SOURCE_PATH = r"data"

source = os.listdir(SOURCE_PATH)

destination = "data/newfolder/"
for files in source:
    if files.endswith(".txt"):
        print files
        sourceFile = '%s\\%s' % (SOURCE_PATH,files);
        print sourceFile
        shutil.copy(sourceFile,destination)
