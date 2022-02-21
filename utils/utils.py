def get_root_path():
    from sys import path
    return(path[1])

def set_root_dir():
    from sys import path
    from os import chdir
    chdir(path[1])

def del_file(loc):
    import os
    if os.path.exists(loc):
      os.remove(loc)
    else:
      print("The file does not exist")


if __name__ == "__main__":
    print(f"Root path is: \n\t{get_root_path()}")