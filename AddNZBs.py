#!/usr/bin/python3
##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###

# Add downloaded NZB files to NZBGet
#
#  
# If the current NZB download being processed by this script contains NZB
# files they will be pushed to the NZBGet queue.
#  
# If the NZB file names do include an unpack password in the format
# nzbname{{password}}.nzb the password will be passed over to NZBGet when 
# pushing the NZB file to NZBGet.
#  
# If a category was assigned to the currently processed NZB download, this
# category will be passed over to NZBGet as well.
#  
# After the NZB files have been pushed to NZBGet they will be deleted from the
# download directory and if this results in an empty directory it will be
# deleted as well.
#  
# NOTE: This script requires Python 3.x to be installed on your system.

### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

import sys
import os
import re
import base64
from urllib.request import quote
from xmlrpc.client import ServerProxy

# priorities options
priorities = {
    "very low": -100,
    "low": -50,
    "normal": 0,
    "high": 50,
    "very high": 100,
    "force": 900
}

# yes or no options
yesNo = {
    "yes": True,
    "no": False
}

# addLocalFileToNZBGet function
def addLocalFileToNZBGet(filename, path, category = '', nzbpassword = ''):
    # Get the info for the XML-RPC requests
    host = os.environ.get('NZBOP_CONTROLIP');
    port = os.environ.get('NZBOP_CONTROLPORT');
    username = os.environ.get('NZBOP_CONTROLUSERNAME');
    password = os.environ.get('NZBOP_CONTROLPASSWORD');
    
    if host == '0.0.0.0': host = '127.0.0.1'

    # Append variables
    priority = priorities[os.environ.get('NZBOP_ADDNZBS_PRIORITY', "normal")]
    addToTop = yesNo[os.environ.get('NZBOP_ADDNZBS_ADDTOTOP', "no")]
    addPaused = yesNo[os.environ.get('NZBOP_ADDNZBS_ADDPAUSED', "no")]

    # DupeCheck variables
    dupekey = ''
    dupescore = 0
    dupemode = os.environ.get('NZBOP_ADDNZBS_DUPEMODE', "force").upper()

    # Build a URL for XML-RPC requests
    rpcUrl = 'http://%s:%s@%s:%s/xmlrpc' % (quote(username), quote(password), host, port);

    # Create remote server object
    server = ServerProxy(rpcUrl)

    # read the NZB file
    file = open(path, 'r') 
    nzb = file.read()
    file.close()

    # Call remote method 'append'
    nzbid = server.append(filename, base64.b64encode(nzb.encode('utf8')).decode('ascii'), category, priority, addToTop, addPaused, dupekey, dupescore, dupemode, [('*unpack:password', nzbpassword)])
    return str(nzbid)

success = 0
error = 0

print('[INFO] Scanning for NZB files.')

# walk through all downloaded files
# r=root, d=directories, f=files
for r, d, f in os.walk(os.environ.get('NZBPP_DIRECTORY')):
    for file in f:
        # Analyse the file name components
        nzbfile = re.search(r'^(.+?)(\{\{(.+)\}\})?\.nzb$', file, re.IGNORECASE)
        # if the file is a NZB file
        if nzbfile:
            #set the full path to the nzb file
            nzbpath = os.path.join(r, file)
            # get the name without password
            nzbname = nzbfile.group(1)
            print('[INFO] Found NZB file "' + nzbname + '"')
            # check if the file name contains also a password
            if nzbfile.group(3):
                # if yes, set the password
                nzbpassword = nzbfile.group(3)
            else:
                # if not, set the password to empty
                nzbpassword = ''
            # check if a category was assigned to this download
            if os.environ.get('NZBPP_CATEGORY'):
                # if yes, set the category
                nzbcategory = os.environ.get('NZBPP_CATEGORY')
            else:
                # if not, set the category to empty
                nzbcategory = ''
            # push the NZB file to NZBGet
            nzbid = addLocalFileToNZBGet(nzbname + '.nzb', nzbpath, nzbcategory, nzbpassword)
            # check if the push was successfull
            if nzbid:
                # if yes, print a success message
                success = success + 1
                print('[INFO] NZB file "' + nzbname + '" successfully added to the queue.')
                # and delete the NZB file
                try:
                    os.remove(nzbpath)
                except Exception as e:
                    print('[WARNING] Cannot delete NZB file "' + nzbpath + '". Error: ' + str(e))
            else:
                # in not, print an error message
                error = error + 1
                print('[ERROR] Unable to add NZB file "' + nzbname + '" to the queue.')
            # if the current directory is now empty, try to delete it
            if not os.listdir(r):
                try:
                    os.rmdir(r)
                except Exception as e:
                    print('[WARNING] Cannot delete empty directory "' + r + '". Error: ' + str(e))

if success or error:
    if success:
        print('[INFO] ' + str(success) + ' NZB file(s) successfully added to the queue.')
    if error:
        print('[ERROR] ' + str(error) + ' NZB file(s) failed to be added to the queue.')
    if error and not success:
        sys.exit(94)
    else:
        sys.exit(93)
else:
    print('[INFO] No NZB file found to process.')
    sys.exit(93)