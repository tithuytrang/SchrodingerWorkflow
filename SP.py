#__SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP__
#__SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP____SP__


# __1__: OPEN SCHRODINGER
# import os
# os.system('"C:\Program Files\Schrodinger2018-1\utilities\schrodinger_start.bat" -startcmd')


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
    with open('D:\New\SP\state.txt') as file:
        position = file.read()
    with open("D:\New\SP\glide-dock_SP_10-0001.inp", "w") as file:
        file.write('''COMPRESS_POSES   True
GRIDFILE   "D:\PHARMACOPHORE\LUAN VAN\Project\DOCK 1MIL result\GRID_ FOR DOCKING\glide-grid_6.zip"
KEEP_STATE   True
LIGAND_END   36566
LIGAND_OFFSET   0
LIGANDFILE   "D:\New\SP\glide-dock_SP_10-0001\glide-dock_SP_10-0001_in.maegz"
NOSORT   True
POSE_OUTTYPE   ligandlib
PRECISION   SP
LIGAND_START   '''+ position)
except:
    pass
# Send command
app.window().send_chars('glide -no_cleanup -TMPDIR "D:\New\SP\Temp" "D:\New\SP\glide-dock_SP_10-0001.inp"')
app.window().send_chars('{ENTER}')

#################################___AFTER RUNNING___#################################

# __4__: AFTERMATH PROCESS
import os
import glob
import shutil
import json
# Get latest dir
latest_dir = max(glob.glob(os.path.join('D:\New\SP\Temp\PhiLong', '*/')), key=os.path.getmtime)

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
# pattern = re.compile(r'[0-9]+ \(')
# result = re.findall(pattern, content)[-1]
# final = result[:-2]

# Move temporary file (prevent cleanup)
import datetime
now = datetime.datetime.now()
folder = now.strftime('%Y.%m.%d_%H.%M.%S')
newpath = "D:\New\SP\Screen\\" + folder
if not os.path.exists(newpath):
    os.makedirs(newpath)
shutil.move(latest_dir, newpath)

# Save the last ligand as state.txt
with open('D:\New\SP\state.txt',"w") as file:
    file.write(str(final))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

############################################__JOINING MAEGZ FILES__########################################################
import os
screen_dir = 'D:\New\SP\Screen'
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
#app.window().send_chars('glide_merge -o "D:\New\out_pv.maegz" -r "D:\New\out.rept" ')
app.window().send_chars('glide_sort -o "D:\New\SP\out_pv.maegz" -r "D:\New\SP\out.rept" ')
app.window().send_chars(output)
app.window().send_chars('{ENTER}')

