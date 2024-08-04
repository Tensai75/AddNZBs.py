# AddNZBs.py

### Add downloaded NZB files to NZBGet - An Extension Script for NZBGet

If the current NZB download being processed by this script contains NZB files they will be pushed to the NZBGet queue.

If the NZB file names do include an unpack password in the format nzbname{{password}}.nzb the password will be passed over to NZBGet when pushing the NZB file to NZBGet.

If a category was assigned to the currently processed NZB download, this category will be passed over to NZBGet as well.

After the NZB files have been pushed to NZBGet they will be deleted from the download directory and if this results in an empty directory it will be deleted as well.

__NOTE:__ This script requires Python 3.x to be installed on the system running NZBGet.

See the [NZBGet documentation](https://nzbget.com/documentation/extension-scripts/) for information on how to install extension scripts for NZBGet.