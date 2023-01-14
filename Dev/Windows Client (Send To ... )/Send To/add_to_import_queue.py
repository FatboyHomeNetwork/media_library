import sys

sys.path.append('\\\\SERVER\\Projects\\Fat Boy Home Network (FBHN)\\Import Media\\common')

import add_to_import_queue__common as lib

#
# main()
#

if len(sys.argv) == 2:
    lib.add(sys.argv[1])
