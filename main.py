import os
import sys


def main():
    host = 'smms'
    if len(sys.argv) > 1:
        host = sys.argv[1]
    os.system('/usr/bin/python2 {}_processer.py'.format(host))


if __name__ == "__main__":
    main()
