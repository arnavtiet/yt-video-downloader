import streamlit as st
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import re

# Configuration options
ydl_opts = {
    'format': 'bestaudio/best',  # Download the best quality audio
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save with title as filename
}

# Function to sanitize file names
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

# Function to process audio files (cut first 30 seconds)
def process_audio_files(file_names):
    audio_files = []
    for file_name in file_names:
        try:
            if os.path.exists(file_name):
                audio = AudioSegment.from_mp3(file_name)
                audio = audio[30000:]  # Cut the first 30 seconds
                audio_files.append(audio)
        except Exception as e:
            st.error(f"Error processing {file_name}: {e}")
    return audio_files

# Function to merge audio files
def merge_audio(audio_files):
    if audio_files:
        merged_audio = audio_files[0]
        for audio in audio_files[1:]:
            merged_audio += audio
        return merged_audio
    return None

# Function to zip the audio file
def zip_audio(zip_path, audio_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(audio_path, os.path.basename(audio_path))

# Function to send the zipped file via email
def send_email(zip_path, sender_email, password, receiver_email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Merged Audio File"

    with open(zip_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_path)}')
        msg.attach(part)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        st.success(f"Email sent to {receiver_email}")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Streamlit frontend
st.title("YouTube Audio Downloader & Merger")

search_query = st.text_input("Enter your search query:")
max_videos = st.number_input("How many videos do you want to process?", min_value=1, step=1)
sender_email = st.text_input("Your Email:")
password = st.text_input("Email Password (App Password if 2FA enabled):", type="password")
receiver_email = st.text_input("Recipient Email:")

if st.button("Start Download and Process"):
    if not (search_query and sender_email and password and receiver_email):
        st.error("Please fill in all fields.")
    else:
        try:
            with YoutubeDL(ydl_opts) as ydl:
                search_results = ydl.extract_info(f"ytsearch{max_videos}:{search_query}", download=False)['entries']
                video_urls = [result['webpage_url'] for result in search_results]
                ydl.download(video_urls)

            downloaded_files = [
                f"downloads/{sanitize_filename(result['title'])}.mp3"
                for result in search_results
            ]

            audio_files = process_audio_files(downloaded_files)

            if not audio_files:
                st.error("No valid audio files to process.")
            else:
                merged_audio = merge_audio(audio_files)
                merged_file_path = "downloads/merged_audio.mp3"
                merged_audio.export(merged_file_path, format='mp3')

                zip_path = "downloads/merged_audio.zip"
                zip_audio(zip_path, merged_file_path)

                send_email(zip_path, sender_email, password, receiver_email)
        except Exception as e:
            st.error(f"An error occurred: {e}")
