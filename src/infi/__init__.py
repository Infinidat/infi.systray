import sys
if hex(sys.hexversion) < '0x30300f0':
    __import__("pkg_resources").declare_namespace(__name__)
