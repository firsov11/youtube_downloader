YouTube Downloader GUI

A simple desktop application written in Python with a graphical interface for downloading YouTube videos in MP4 format with selectable quality.

Features
•	Paste link from clipboard
•	Choose download folder
•	Select maximum video quality (720p, 1080p, 1440p, 2160p)
•	Progress bar with percentage, speed, and ETA
•	Bundles ffmpeg.exe automatically
•	No installation required — just run the .exe

How to Use
1.	Paste a YouTube video link manually or using the "Paste from clipboard" button.
2.	Choose a folder to save the file.
3.	Select the desired maximum quality.
4.	Click "Download" and wait for the process to complete.

Build .exe from Source
For Windows only. Requires Python 3.9+ and installed dependencies.
1. Install dependencies:
pip install yt-dlp
pip install pyinstaller
•	yt-dlp — an improved fork of youtube-dl with better format and API support
•	pyinstaller — used to bundle the Python script into a standalone executable
2. Place the following files next to youtube_gui.py:
•	ffmpeg.exe — download from official source
•	youtubelogo.ico — your app icon
3. Build the executable:
pyinstaller --noconfirm --onefile --windowed --icon=youtubelogo.ico --add-data "youtubelogo.ico;." --add-data "ffmpeg.exe;." youtube_gui.py

After the build, the file youtube_gui.exe will appear in the dist folder.



