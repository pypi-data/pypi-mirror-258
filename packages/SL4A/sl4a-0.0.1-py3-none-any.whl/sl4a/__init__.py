__version_tuple__=(0,0,1)
# Данные о модуле
__version__="{}.{}.{}".format(*__version_tuple__)
__depends__={
  "required":[],
  "optional":[]
  }
__all__=["Android"]
__scripts__=[
  "sl4a-install",
  "sl4a-instructions",
  "sl4a-get",
  ]
__all__.sort()
__scripts__.sort()
from sl4a.android import Android
