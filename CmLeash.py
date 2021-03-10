#!/usr/bin/env python3
import os
import sys
from datetime import datetime

import CmBoy


class CmLeash:
    """
    This is the leash for the CmBoy. Technical people would call it a wrapper, but that's boring.
    """

    def __init__(self):
        pass

    def go_walkies(self):
        try:
            cm_boy = CmBoy
            cm_boy.main(sys.argv[1:])
        except Exception as exc:
            self.generate_folder()
            file_log_name = "{}_error.log".format(str(datetime.now().strftime("%Y_%m_%d_%H_%M_%S")))
            if __name__ == '__main__':
                with open("./log/{}".format(file_log_name)) as err_file:
                    err_file.write(exc)

    def generate_folder(self):
        if not os.path.isdir("./log"):
            os.mkdir("./log")

if __name__ == "__main__":
    cm_leash = CmLeash()
    cm_leash.go_walkies()
