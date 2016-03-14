import sys
import settings
from StringIO import StringIO
import textwrap
import re

__once = set()
output = StringIO()
suppressed = StringIO()

def split(s, wid, lead=''):

    right = lead+(s.strip())    
    res = []
    while len(right) > wid:
        isplit = wid
        
        for char in right[:wid][::-1]:
            if char == ' ': break
            isplit -= 1
            
        if isplit < float(wid)/2: 
            isplit=wid
            
        left, right = right[:isplit], lead+right[isplit:]
        res.append(left)
        
    res.append(right)
    
    return res
    
def fmt(istr, lim):
    
    substrs = []
    for s in istr.split('\n'):
        if len(s) > lim:
            lead = re.match(r'(\s*).*',s).group(1)
            substrs += split(s, lim, lead=lead)
        else:
            substrs.append(s)

    return '\n'.join(substrs)
    
def stdout(msg, log=False, width=80):
    '''Display a message.'''
    wrapped = fmt(msg, width)
    print >> output, wrapped
    print wrapped
    
def log(msg, width=80):
    '''Display a message if settings.silent == False.'''
    
    if not settings.silent: 
        stdout(msg, width=width)
    else:
        print >> suppressed, msg

def once(msg, width=80):
    '''
    Display a message that should be shown only once during runtime. 
    Once printed, msg is stored in module state variable '__once'.
    '''
    if msg not in __once:
        log(msg, width=width)
        __once.add(msg)

def verbose(msg, width=80):
    '''
    Display a message that should only be shown if settings.verbose == True 
    and settings.silent == False.
    '''
    if settings.verbose: 
        log(msg, width=width)
    else:
        print >> suppressed, msg
    
def query(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    Recipe borrowed from http://code.activestate.com/recipes/577058/
    """
    valid = {"yes":True, "y":True, "ye":True,
             "no":False, "n":False}
    
    if settings.silent: 
        print >> suppressed, question+'    [{}]\n'.format(default)
        return valid[default]
    elif settings.force: 
        stdout(question+'    [{}]\n'.format(default))
        return valid[default]
    
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        log(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            log("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

def exit(code=0):
    '''
    Exit rosetta session by raisin sys.exit(code). The contents of 
    settings.output and settings.suppressed are written to 'rosetta.log' and 
    'rosetta.suppressed.log' respectively.
    '''
    with open('rosetta.log', 'w') as logfile:
        logfile.write(output.getvalue())
    with open('rosetta.suppressed.log', 'w') as logfile:
        logfile.write(suppressed.getvalue())
    log('Exit.')
    log('Output and suppressed output written to rosetta.log and '
        'rosetta.suppressed.log respectively.')
    log('#############################')
    log('')
    sys.exit(code)

log('')
once('''########## Rosetta ##########
Adam Falkowski, Benjamin Fuks,
Kentarou Mawatari, Ken Mimasu,
Francesco Riva & Veronica Sanz.
Eur.Phys.J. C75 (2015) 12, 583 
#############################''')
log('')




    