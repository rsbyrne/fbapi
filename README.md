# fbapi

## What is it?

This is a *Selenium*-based containerised API for downloading data from *Facebook*'s *Data For Good* portal through the command line. Its only prerequisite is a *Facebook* account authorised for *Geoinsights* access and a working *Docker* install. Alternatively, you can use the code and the instructions in the Dockerfile contained in this repository to configure a local install.

## How do I use it?

### On *Unix*-type systems (Linux, Apple, Windows Subsystem for Linux)

1. Either clone the repository or simply copy `fb_pull.sh` to your computer.
2. Open a *bash* shell. (On *Windows* with *WSL* installed, just open a *PowerShell* and type `bash`)
3. Run the script with the following call signature (you may need `sudo` permission). (Note that the nominated output directory and all intermediate directories will be created if they do not already exist.)
```bash
$ sudo sh fb_pull.sh <FB_DATA_PAGE_URL> <FB_USERNAME> <FB_PASSWORD> <OUTPUT_DIRECTORY>
```
For example, for a user named *misterfunnybunny@gmail.com* whose password is *cutebunny64* who wants to download the tile-based population data for Victoria, Australia, to the local directory */home/myfiles/mydata*:
```bash
$ sudo sh fb_pull.sh https://www.facebook.com/geoinsights-portal/downloads/?id=223808228714910 misterfunnybunny@gmail.com cutebunny64 /home/myfiles/mydata
```
4. That's it! Your files should be there in the specified directory. If in future you attempt to download the same data to the same directory, the API will recognise the duplication and skip the redundant files, only downloading what is new.

### On *Windows 10*

The best way to use this API on *Windows* is to use the *Windows Subsystem for Linux* (*WSL*), Microsoft's official built-in Unix-like interface which was introduced in *Windows 10*. Once installed, *WSL* will allow you to use any Linux-based applications natively on your *Windows* machine. *WSL* is a massively underrated feature for any *Windows* machine and is highly recommended. To enable it, follow these instructions:

1. Install *WSL*: https://docs.microsoft.com/en-us/windows/wsl/install-win10
2. Connect your *Docker for Windows* (a.k.a. *Docker Desktop*) to your *WSL*: https://code.visualstudio.com/blogs/2020/03/02/docker-in-wsl2

If you do not want to go down this route, however, this repository also provides a *PowerShell* script. Follow these instructions to use it:

1. Copy or download the file *pull-fb.ps1* from this repository to your local machine.
2. Open a *PowerShell* (search for it in the search bar if you are uncertain) and be sure to **run as administrator** (by right-clicking on the icon).
3. Type `set-executionpolicy remotesigned`, hit `Enter`, and hit `A`. (Be aware that doing this may make your computer more vulnerable to malware.)
4. Open a new *PowerShell* **not** as an administrator. Navigate to where you have stored the *pull-fb.ps1* script and type the following command. (Note that the nominated output directory and all intermediate directories will be created if they do not already exist.)
```powershell
C:\Users\YourName> .\pull-fb <FB_DATA_PAGE_URL> <FB_USERNAME> <FB_PASSWORD> <OUTPUT_DIRECTORY>
```
For example, for a user named *misterwindowsbunny@hotmail.com* whose password is *windowsbunny32* who wants to download the tile-based population data for Victoria, Australia, to the local directory *C:\Users\MisterBunny\mydata\\*:
```powershell
C:\Users\MisterBunny> .\pull-fb 'https://www.facebook.com/geoinsights-portal/downloads/?id=223808228714910' 'misterwindowsbunny@hotmail.com' 'windowsbunny32' C:\Users\MisterBunny\mydata\
```
5. Done! After seeing some prompts in your *PowerShell*, you should eventually be informed that your downloads are complete. The desired files should be in your nominated output directory. Future downloads will refrain from duplicating pre-existing files, so while the first download may be quite slow, further updates will be considerably quicker.

## How does it work?

The API is a containerised application hosting a Linux-based Python-Firefox-Selenium web scraper toolchain. Upon running `fb_pull.sh`, a a fresh image is pulled if necessary, a container is booted up which mounts your target directory to an internal directory inside the container, and a Python process is initiated which boots up a web driver, navigates to the Facebook login page, logs in with the provided credentials, navigates to the specified URL, searches for all download links for `.csv` files that are formatted like dates, filters out all filenames that already appear in the target directory, and then sequentially clicks on each link, waiting between each to see that the file has successfully downloaded. The procedure is not the fastest, but is designed for absolute reliability - and to avoid alarming the bot catchers at Facebook.

## FAQ

Q. Is it secure?

A. It should be! Though the username and password are provided to the command in plaintext, this information shouldn't be able to be intercepted on its way to the web driver, and the entire application - along with the container - gets thrown out with every use, so no compromising data should be retained. But the developer is not a cryptographer and no assurances are given.

Q. Is it legal?

A. While Facebook does not provide or encourage a command-line API for their data services, it is not prohibited to develop or use them; several now exist which are known and tolerated by the Data For Good team.

Q. It's just not working for me!

A. Try providing an absolute filepath for your output directory; sometimes this can cause trouble with the *Docker* mount. Check your *Facebook* credentials by logging in the usual way. Try clearing your *Docker* caches and pulling a fresh image: the command `docker system prune -a` may be helpful. Make sure your `fb_pull.sh` script is up to date. Make sure the path to your target directory has the appropriate permissions. Check that your *Docker* instance is running correctly by trying the command `docker run hello-world`. Make sure you are logged in to *DockerHub* by typing `docker login -u <MYUSERNAME> -p <MYPASSWORD>`.

Q. Should the output path be provided relative to my current working directory, or the script's directory?

A. You can call the script from any directory! In the instructions above, it is suggested to navigate to the script's directory before running it but that is not necessary - this is just for ease of explanation. The provided output path can be either absolute or relative to your current working directory. (It is however recommended to provide an absolute filepath if possible - this is a little more foolproof.)

Q. Should I provide a *Unix*-like filepath or a *Windows*-like filepath?

A. The filepath argument should be provided using whatever syntax is natural for the terminal you are using: e.g. backslashes should be used in *PowerShell*, forward slashes in *Bash*.

Q. Can I reuse the code?

A. The code is provided as is, absolutely free of charge, with no strings attached, and no liability retained by the developer.
