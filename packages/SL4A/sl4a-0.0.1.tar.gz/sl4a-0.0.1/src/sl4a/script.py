import sys,os,shutil
class path:
  me=os.path.dirname(__file__)
  sl4a="/sdcard/sl4a"
def instructions():
  guide=[
    "Startup instructions",
    "1. Open the SL4A app on your phone",
    "2. Run the SL4A-SERVER script and leave it running",
    "3. Go back to Termux and you can use the SL4A module",
    "4. When finished using, it is recommended to turn off the SL4A to save battery power",
    ]
  for i in guide:
    print(i.rstrip())
def install():
  if not "TERMUX_VERSION" in os.environ:
    print("This module is designed for use in Termux",file=sys.stderr)
    print("But the installation will still be attempted",file=sys.stderr)
  files={
    path.me+"/apk/SL4A.apk":path.sl4a+"/apk/SL4A.apk",
    path.me+"/apk/Py4A.apk":path.sl4a+"/apk/Py4A.apk",
    path.me+"/scripts/SL4A-SERVER.py":path.sl4a+"/scripts/SL4A-SERVER.py",
    path.me+"/scripts/SL4A-SERVER.py":path.sl4a+"/scripts/SL4A-SERVER.py3",
    }
  update=False
  for i in ["-U","--update"]:
    if i in sys.argv:
      update=True
      break
  exists=False
  for fr,to in files.items():
    if not os.path.exists(to):
      dir=os.path.dirname(to)
      if not os.path.exists(dir):
        os.makedirs(dir)
      if os.path.exists(to):
        if update:
          shutil.copy(fr,to)
        else:
          print(f'File "{to}" already exists',file=sys.stderr)
          exists=True
      else:
        shutil.copy(fr,to)
  if exists:
    print('Use the "-U" or "--update" argument to replace these files',file=sys.stderr)
  guide=[
    "Installation instructions:",
    "1. Install 2 applications on your phone that are located in the folder",
    "   "+path.sl4a+"/apk",
    "2. Install Python in SL4A application",
    "3. Check the functionality of the SL4A-SERVER script inside SL4A",
    "4. Installation completed!",
    ]
  for i in guide:
    print(i.rstrip())
  instructions()
def get(files=None):
  with open(path.me+"/example.txt","r") as f:
    example=[]
    for i in f.read().rstrip().split("\n"):
      i=i.rstrip()
      if i!="":
        example.append(i)
    ex="\n".join(example)+"\n"
  if file==None:
    if len(sys.argv)==1:
      for i in example:
        print(i)
    else:
      file=sys.argv[1]
  if os.path.exists(file):
    with open(file,"r") as f:
      code=f.read()
  else:
    code=""
  with open(file,"w") as f:
    f.write(ex+code)
  print(f'The module import is written to the file "{file}"')
