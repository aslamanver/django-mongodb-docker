#!/usr/bin/env python
import os
import sys


def main():

    if len(sys.argv) > 1:

        if sys.argv[1] == "login":
            os.system("docker exec -it django-container bash")
            return

        print("There is no argument for: " + sys.argv[1])

    else:
        print("Netmaiesta: You missed the argument")


if __name__ == "__main__":
    main()
