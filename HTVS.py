#__HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS__
#__HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS____HTVS__

# __1__: OPEN SCHRODINGER
# import os
# os.system('"C:/Program Files/Schrodinger2018-1/utilities/schrodinger_start.bat" -startcmd')


# __2__: CONNECT PROCESS
import psutil
import pywinauto

# Determine process
string = 'schrodinger_start.bat'
assert True
ls = []
for p in psutil.process_iter():
    name_, exe, cmdline = "", "", []
    try:
        name_ = p.name()
        exe = p.exe()
        cmdline = p.cmdline()
    except (psutil.AccessDenied, psutil.ZombieProcess):
        pass
    except psutil.NoSuchProcess:
        continue
    if (string in name_) or (string in exe) or (string in ''.join(cmdline)):
        ls.append(p.pid)
# Connect process
app = pywinauto.Application().connect(process=ls[0])

# __3__: START SCREENING
# Start ligand
try:
    with open('D:/New2/HTVS/state.txt') as file:
        position = file.read()
    with open("D:/New2/HTVS/glide-dock_HTVS_7.in", "w") as file:
        file.write('''OUTPUTDIR "D:/New2/HTVS/Project"
GRIDFILE   "D:/PHARMACOPHORE/Project/DOCK 1MIL result/GRID_ FOR DOCKING/glide-grid_6.zip"
LIGANDFILE   "D:/New2/HTVS/glide-dock_HTVS_7/glide-dock_HTVS_7-0001_in.maegz"
PRECISION   HTVS  
LIGAND_START '''+ position)
except:
    pass
# Send command
app.window().send_chars('glide -no_cleanup -TMPDIR "D:/New2/HTVS/Temp" "D:/New2/HTVS/glide-dock_HTVS_7.in"')
app.window().send_keystrokes('{ENTER}')

#################################___AFTER RUNNING___#################################

# __4__: AFTERMATH PROCESS
import os
import glob
import shutil
import json
# Get latest dir
latest_dir = max(glob.glob(os.path.join('D:/New2/HTVS/Temp/PhiLong', '*/')), key=os.path.getmtime)

# Get last ligand screened position
log_files = []
for filename in os.listdir(latest_dir):
    if '.json' in filename:
        log_files.append(filename)
latest_log_path = os.path.join(latest_dir,max(log_files))

with open(latest_log_path) as file:
    content = json.load(file)
final = content[u'lignum']


# with open(latest_log_path) as file:
#     content = file.read()
# pattern = re.compile(r'[0-9]+ /(')
# result = re.findall(pattern, content)[-1]
# final = result[:-2]

# Move temporary file (prevent cleanup)
import datetime
now = datetime.datetime.now()
folder = now.strftime('%Y.%m.%d_%H.%M.%S')
newpath = "D:/New2/HTVS/Screen//" + folder
if not os.path.exists(newpath):
    os.makedirs(newpath)
shutil.move(latest_dir, newpath)

# Save the last ligand as state.txt
with open('D:/New2/HTVS/state.txt',"w") as file:
    file.write(str(final))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

############################################__JOINING MAEGZ FILES__########################################################
import os
screen_dir = 'D:/New2/HTVS/Screen'
screen_files = []
for (dirpath, dirnames, filenames) in os.walk(screen_dir):
        for item in filenames:
            if '.maegz' in item:
                screen_files.append(os.path.join(dirpath,item))

edit = [r'"'+ string + r'"' for string in screen_files]
output = ' '.join(edit)


# __2__: CONNECT PROCESS
import psutil
import pywinauto

# Determine process
string = 'schrodinger_start.bat'
assert True
ls = []
for p in psutil.process_iter():
    name_, exe, cmdline = "", "", []
    try:
        name_ = p.name()
        exe = p.exe()
        cmdline = p.cmdline()
    except (psutil.AccessDenied, psutil.ZombieProcess):
        pass
    except psutil.NoSuchProcess:
        continue
    if (string in name_) or (string in exe) or (string in ''.join(cmdline)):
        ls.append(p.pid)
# Connect process
app = pywinauto.Application().connect(process=ls[0])

# __3__: START JOINING
# Send command
#app.window().send_chars('glide_merge -o "D:/New2/out_pv.maegz" -r "D:/New2/out.rept" ')
app.window().send_chars('glide_sort -o "D:/New2/HTVS/out_pv.maegz" -r "D:/New2/HTVS/out.rept" ')
app.window().send_chars(output)
app.window().send_keystrokes('{ENTER}')

