#!/usr/bin/python
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
# If the NZB file names do not include an unpack password but the currently
# processed NZB download was assigned an unpack password, this password will
# be passed over to NZBGet instead.
#  
# If a category was assigned to the currently processed NZB download, this
# category will be passed over to NZBGet as well.
#  
# After the NZB files have been pushed to NZBGet they will be deleted from the
# download directory and if this results in an empty directory it will be
# deleted as well.
#  
# NOTE: This script requires Python to be installed on your system.

### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

import sys
import os
import re
import shutil
import base64
from urllib2 import quote
try:
	from xmlrpclib import ServerProxy # python 2
except ImportError:
	from xmlrpc.client import ServerProxy # python 3

# addLocalFileToNZBGet function
def addLocalFileToNZBGet(filename, path, category = '', nzbpassword = ''):
    host = os.environ['NZBOP_CONTROLIP'];
    port = os.environ['NZBOP_CONTROLPORT'];
    username = os.environ['NZBOP_CONTROLUSERNAME'];
    password = os.environ['NZBOP_CONTROLPASSWORD'];

    if host == '0.0.0.0': host = '127.0.0.1'

    # Build a URL for XML-RPC requests
    rpcUrl = 'http://%s:%s@%s:%s/xmlrpc' % (quote(username), quote(password), host, port);

    # Create remote server object
    server = ServerProxy(rpcUrl)

    # read the NZB file
    file = open(path, 'r') 
    nzb = file.read()
    file.close()

    # Call remote method 'append'
    nzbid = server.append(filename, base64.b64encode(nzb.encode('utf8')).decode('ascii'), category, 0, True, False, '', 0, 'ALL', [('*unpack:password', nzbpassword)])
    return str(nzbid)

success = 0
error = 0

# walk through all downloaded files
# r=root, d=directories, f = files
for r, d, f in os.walk(os.environ.get('NZBPP_DIRECTORY')):
    for file in f:
        # if the file is a NZB file
        if re.search(r'^(.+?)(\{\{(.+)\}\})?\.nzb$', file):
            #set the full path to the nzb file
            nzbpath = os.path.join(r, file)
            # Analyse the file name components
            nzbfile = re.search(r'^(.+?)(\{\{(.+)\}\})?\.nzb$', file)
            # get the name without password
            nzbname = nzbfile.group(1)
            print '[INFO] Found NZB file "' + nzbname + '"'
            # check if the file name contains also a password
            if nzbfile.group(3):
                # if yes, set the password
                nzbpassword = nzbfile.group(3)
            else:
                # if not, check if a password was assigned to this download
                if os.environ.get('NZBPR_*Unpack:Password'):
                    # if yes, set the password
                    nzbpassword = os.environ.get('NZBPR_*Unpack:Password')
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
                print '[INFO] NZB file "' + nzbname + '" successfully added to the queue.'
                # and delete the NZB file
                try:
                    os.remove(nzbpath)
                except Exception, e:
                    print '[WARNING] Cannot delete NZB file "' + nzbpath + '". Error: ' + str(e)
            else:
                # in not, print an error message
                error = error + 1
                print '[ERROR] Unable to add NZB file "' + nzbname + '" to the queue.'
            # if the current directory is now empty, try to delete it
            if not os.listdir(r):
                try:
                    os.rmdir(r)
                except Exception, e:
                    print '[WARNING] Cannot delete empty directory "' + r + '". Error: ' + str(e)

if success or error:
    if success:
        print '[INFO] ' + str(success) + ' NZB file(s) successfully added to the queue.'
    if error:
        print '[ERROR] ' + str(error) + ' NZB file(s) failed to be added to the queue.'
    if error and not success:
        sys.exit(94)
    else:
        sys.exit(93)
else:
    print '[INFO] No NZB file found to process.'
    sys.exit(93)