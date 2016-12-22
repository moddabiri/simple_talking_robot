__author__ = "Mohammad Dabiri"
__copyright__ = "Free to use, copy and modify"
__credits__ = ["Mohammad Dabiri"]
__license__ = "MIT Licence"
__version__ = "0.0.1"
__maintainer__ = "Mohammad Dabiri"
__email__ = "moddabiri@yahoo.com"

import urllib2

def internet_on():
    try:
        response=urllib2.urlopen('http://www.google.com',timeout=2)
        return True
    except urllib2.URLError as err: pass
    return False