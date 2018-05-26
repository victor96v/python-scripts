from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os", "numpy"], "includes": ["numpy"]}

setup(name = "custom_detector" ,
      version = "0.1" ,
      description = "" ,
      options={"build_exe": build_exe_options},
      executables = [Executable("custom_detector.py")])
