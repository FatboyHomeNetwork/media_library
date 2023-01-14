import sys
from media_library..media_library_manager import media_library_manage as mgn



if __name__ == "__main__":
    if len(sys.argv) == 2:
        mgn.next()