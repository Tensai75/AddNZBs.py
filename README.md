# AddNZBs

### Add downloaded NZB files to NZBGet - An Extension Script for NZBGet v24.0 or higher from NZBGet.com

If the current download being processed by the script contains NZB files they will be pushed to the NZBGet queue.

If the NZB file names do include an unpack password in the format nzbname{{password}}.nzb the password will be passed over to NZBGet when pushing the NZB file to NZBGet.

If a category was assigned to the currently processed download, this category will be passed over to NZBGet as well.

After the NZB files have been pushed to NZBGet they can optionally be deleted from the download folder and if this results in empty folders they can optionally be deleted as well.

__NOTE:__ This script requires NZBGet v24.0 or higher and Python 3.x to be installed on the system running NZBGet.

See the [NZBGet documentation](https://nzbget.com/documentation/extension-scripts/) for information on how to install extension scripts for NZBGet.