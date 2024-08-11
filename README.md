# AddNZBs

### Add downloaded NZB files to NZBGet - An Extension Script for NZBGet v24.0 or higher from NZBGet.com

If the current download being processed by the script contains NZB files they will be pushed to the NZBGet queue.

If the NZB file names do include an unpack password in the format nzbname{{password}}.nzb the password will be passed over to NZBGet when pushing the NZB file to NZBGet.

If a category was assigned to the currently processed download, this category will be passed over to NZBGet as well.

After the NZB files have been pushed to NZBGet they can optionally be deleted from the download folder and if this results in empty folders they can optionally be deleted as well.

__NOTE:__ This script requires NZBGet v24.0 or higher and Python 3.x to be installed on the system running NZBGet.

See the [NZBGet documentation](https://nzbget.com/documentation/extension-scripts/) for information on how to install extension scripts for NZBGet.

#### Manual installation instructions (until the script is added to the official NZBGet Extension Manager)
1. create an empty folder named `AddNZBs` inside the NZBGet Scripts folder (ScriptDir)
2. clone this repository into this folder or manually place the `AddNZBs.py` and the `manifest.json` file into this folder
3. open the NZBGet settings page and click on the `EXTENSION MANAGER` menu item
4. activate the extension `Add NZBs` by clicking on the green "Play" button (if you see an orange "Pause" button, the extension is already activated)
5. go to the options page of the extensions by clicking on the black "Settings" button or on the menu item `ADD NZBS` below the menu item `EXTENSION MANAGER`
6. set the options of the extensions according to your wishes
7. do not forget to save the settings and to reload NZBGet!