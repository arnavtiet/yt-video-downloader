# YouTube Audio Downloader & Merger

This project provides a Streamlit-based frontend for downloading YouTube audio files, processing them (removing the first 30 seconds), merging them into a single audio file, and sending the result via email.

## Features
- Search for YouTube videos and download the audio.
- Process downloaded audio files by trimming the first 30 seconds.
- Merge multiple audio files into one.
- Compress the merged audio file into a ZIP archive.
- Send the ZIP file as an email attachment.

## Dependencies
The following Python libraries are required:

- `streamlit`
- `yt-dlp`
- `pydub`
- `smtplib` (standard library)
- `email` (standard library)
- `os` (standard library)
- `zipfile` (standard library)
- `re` (standard library)

You also need `ffmpeg` installed on your system for `pydub` to process audio files.

### Installing Dependencies
Run the following command to install the required Python libraries:
```bash
pip install streamlit yt-dlp pydub
```

### Installing ffmpeg
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract, and add the `bin` folder to your system's PATH.
- **Linux**: Install using your package manager (e.g., `sudo apt install ffmpeg` for Debian-based distros).
- **Mac**: Install via Homebrew (`brew install ffmpeg`).

## How to Run
1. Clone this repository or download the script.
2. Ensure `ffmpeg` is installed and available in your system's PATH.
3. Create a folder named `downloads` in the project directory.
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
5. Open the local URL displayed in the terminal (e.g., `http://localhost:8501`) in your web browser.

## Usage
1. Enter your search query for YouTube videos.
2. Specify the number of videos to process.
3. Provide your email credentials (sender email, app password, and recipient email).
4. Click the "Start Download and Process" button to begin.

## Notes
- Use an [App Password](https://support.google.com/accounts/answer/185833?hl=en) if your email account uses two-factor authentication (2FA).
- Ensure the `downloads/` directory exists before running the application.
- The merged audio file and ZIP archive will be stored in the `downloads/` directory.

## License
This project is licensed under the MIT License. 
