import sys
from os import path
sys.path.insert(0, path.dirname(path.dirname(path.realpath(__file__))))
from getway.nginx import watch
from com.vars import ETCD


def main():
    watch(ETCD.NAMESPACE)


if __name__ == '__main__':
    main()
