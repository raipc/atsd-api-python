import platform

import time

'''
Print python version, timezone and dependencies version.
'''

print('Python version is %s' % platform.python_version())
print('Current timezone %s\n' % str(time.tzname))

required_packages = ['dateutil', 'requests', 'pandas']

for package in required_packages:
    try:
        p = __import__(package)
        print('%s vesrion is %s' % (package, p.__version__))
    except ImportError:
        print('%s uninstalled' % package)
