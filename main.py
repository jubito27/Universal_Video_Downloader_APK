from kivymd.app import MDApp # type: ignore
from kivymd.uix.screen import MDScreen # type: ignore
from kivymd.uix.button import MDRaisedButton # type: ignore
from kivymd.uix.textfield import MDTextField # type: ignore
from kivymd.uix.dialog import MDDialog# type: ignore
from kivymd.uix.boxlayout import MDBoxLayout# type: ignore
from kivymd.uix.relativelayout import MDRelativeLayout # type: ignore
from kivymd.uix.button import MDIconButton # type: ignore
from kivymd.uix.label import MDLabel# type: ignore
from kivymd.uix.progressbar import MDProgressBar  # type: ignore
from kivy.clock import Clock # type: ignore
from kivy.utils import platform # type: ignore
from kivy.properties import StringProperty, NumericProperty # type: ignore
import yt_dlp # type: ignore
import os
import re
import logging
import threading
import webbrowser
from pathlib import Path
from pyrogram import Client # type: ignore
import asyncio


# Android imports
if platform == 'android':
    from android.permissions import request_permissions, Permission # type: ignore
    from android.storage import primary_external_storage_path # type: ignore
    from jnius import autoclass # type: ignore


class MyLogger:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): print(msg)

class UniversalVideoDownloader(MDApp):
    download_status = StringProperty("")
    download_percent = NumericProperty(0)
    
    def build(self):
        # Request Android permissions
        if platform == 'android':
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
        
        # Configure theme
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "Amber"
        
        # Create UI
        self.screen = MDScreen()
        self.layout = MDBoxLayout(
            orientation="vertical",
            padding="40dp",
            spacing="20dp",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.8, 0.8)
        )
        
        # App title
        self.title_label = MDLabel(
            text="Universal Video Downloader",
            halign="center",
            font_style="H4",
            theme_text_color="Primary"
        )
        
        # Description label
        self.desc_label = MDLabel(
            text="Download videos from YouTube, Instagram, TikTok, Snapchat & more with ease and free of cost without adds and signup or login.",
            halign="center",
            font_style="Subtitle1",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="30dp"
        )
        
        # URL input field
        self.url_input = MDTextField(
            hint_text="Enter video link",
            mode="rectangle",
            size_hint_x=0.9,
            pos_hint={"center_x": 0.5},
            helper_text="Supported: YouTube, Instagram, TikTok, Snapchat, Telegram",
            helper_text_mode="persistent"
        )
        
        # Download button
        self.download_btn = MDRaisedButton(
            text="Download",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
            md_bg_color=self.theme_cls.primary_color
        )
        self.download_btn.bind(on_release=self.start_download)
        
        # Progress bar
        self.progress_bar = MDProgressBar(
            type="determinate",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.9,
            opacity=0
        )
        
        # Percentage label
        self.percent_label = MDLabel(
            text="Downloading... 0%",
            halign="center",
            font_style="H6",
            theme_text_color="Primary",
            opacity=0
        )
        
        # Status label
        self.status_label = MDLabel(
            text=self.download_status,
            halign="center",
            theme_text_color="Secondary",
            size_hint_y=None,
            height="30dp"
        )

        

        self.open_folder_button = MDRaisedButton(
            text="Open Folder",
            on_release=self.open_downloads_folder
        )

        # Footer container
        footer = MDRelativeLayout(size_hint_y=None, height="50dp")

        # Developer label
        developer_label = MDLabel(
            text="Developed by\nJubito Corporation",
            halign="center",
            valign="middle",
            theme_text_color="Secondary",
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        # GitHub button
        github_btn = MDIconButton(
            icon="github",
            pos_hint={"right": 0.95, "center_y": 0.5},
            on_release=lambda x: webbrowser.open("https://github.com/jubito27")
        )

        # LinkedIn button
        linkedin_btn = MDIconButton(
            icon="linkedin",
            pos_hint={"right": 0.85, "center_y": 0.5},
            on_release=lambda x: webbrowser.open("https://www.linkedin.com/in/abhishek-sharma2775")
        )



        # Add footer elements
        footer.add_widget(developer_label)
        footer.add_widget(github_btn)
        footer.add_widget(linkedin_btn)
        
        # Add widgets to layout
        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.desc_label)
        self.layout.add_widget(self.url_input)
        self.layout.add_widget(self.download_btn)
        self.layout.add_widget(self.progress_bar)
        self.layout.add_widget(self.percent_label)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(footer)
        self.screen.add_widget(self.layout)
        return self.screen
    
    def is_valid_url(self, url):
        """Check if URL is from a supported platform"""
        platforms = {
            "youtube": [
                "youtube.com",
                "youtu.be",
                "youtube.com/shorts"
            ],
            "instagram": [
                "instagram.com",
                "www.instagram.com"
            ],
            "facebook": [
                "facebook.com",
                "www.facebook.com",
                "fb.watch"
            ],
            "twitter": [
                "twitter.com",
                "x.com"
            ],
            "tiktok": [
                "tiktok.com",
                "www.tiktok.com"
            ],
            "snapchat": [
                "snapchat.com",
                "www.snapchat.com"
            ],
            "telegram": [
                "t.me",
                "telegram.org"
            ]
        }
        
        for platform, domains in platforms.items():
            if any(domain in url for domain in domains):
                return platform
        return False
    
    def start_download(self, instance):
        url = self.url_input.text.strip()
        
        if not url:
            self.show_dialog("Error", "Please enter a video link.")
            return
            
        platform = self.is_valid_url(url)
        if not platform:
            self.show_dialog("Unsupported Link", 
                           "Supported platforms:\n"
                           "- YouTube\n- Instagram\n- TikTok\n"
                           "- Snapchat\n- Telegram\n- Facebook\n- Twitter/X")
            return
        
        # Show progress UI
        self.progress_bar.opacity = 1
        self.percent_label.opacity = 1
        self.download_btn.disabled = True
        self.update_status(f"Starting {platform} download...")
        
        threading.Thread(target=self.download_video, args=(url, platform)).start()


    def parse_t_me_c_link(self , link):
        parts = link.rstrip('/').split('/')
        chat_id = int("-100" + parts[-2])
        message_id = int(parts[-1])
        return chat_id, message_id
    
    def download_video(self, url, platform):
        try:
            downloads_folder = self.get_downloads_folder()
            output_template = os.path.join(downloads_folder, '%(title)s.%(ext)s')
            
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_template,
                'progress_hooks': [self.update_progress],
                'quiet': True,
                'no_warnings': True,
                'extractor_args': {
                    'instagram': {'skip': ['stories']},
                    'snapchat': {'format': 'best'}
                },
                'referer': url,
                'logger': MyLogger(),
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Platform-specific adjustments
            if platform == "telegram":
                api_id = 23078902      # Replace with your own from my.telegram.org
                api_hash = "7efb5b92d6760e933bb75040a9765710"
                session_name = "tg_session"

                async def telegram_download():
                    chat_id, message_id = self.parse_t_me_c_link(url)
                    async with Client(session_name, api_id=api_id, api_hash=api_hash) as app:
                        msg = await app.get_messages(chat_id, message_id)
                        if msg.video:
                            filename = os.path.join(downloads_folder, msg.video.file_name or "telegram_video.mp4")
                            await app.download_media(msg, file_name=filename)
                            Clock.schedule_once(lambda dt: self.show_download_complete(filename))
                        else:
                            raise Exception("No video found in this message.")

                asyncio.run(telegram_download())
                return
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                Clock.schedule_once(
                    lambda dt: self.show_download_complete(filename))
                
        except Exception as e:
            error_message = f"Download failed: {str(e)}"
            self.update_status(error_message)
            Clock.schedule_once(
                lambda dt: self.show_dialog("Download Failed", 
                                          f"Could not download from {platform}:\n{error_message}"))
            print("error occured:", error_message)
        finally:
            Clock.schedule_once(self.reset_ui)

    def strip_ansi(self, text):
        ansi_escape = re.compile(r'\x1b[^m]*m')
        return ansi_escape.sub('', text)

    
    def update_progress(self, d):
        if d['status'] == 'downloading':
            clean_percent_str = self.strip_ansi(d['_percent_str']).strip('%')
            percent = float(clean_percent_str)
            self.download_percent = percent
            Clock.schedule_once(lambda dt: (
                self.progress_bar._set_value(percent),
                self.percent_label._set_text(f"{percent:.1f}%"),
                self.update_status(
                    f"Downloading: {d['_percent_str']} "
                    f"({d['_speed_str']})"
                )
            ))

    
    def get_downloads_folder(self):
        """Returns system downloads folder path"""
        if platform == 'android':
            downloads_path = os.path.join(primary_external_storage_path(), 'Download')
            if not os.path.exists(downloads_path):
                os.makedirs(downloads_path)
            return downloads_path
        elif platform == 'win':
            import ctypes
            from ctypes import windll, wintypes
            CSIDL_DOWNLOADS = 0x0011
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_DOWNLOADS, None, 0, buf)
            return buf.value
        else:  # Linux/Mac
            return str(Path.home() / "Downloads")
    
    def show_download_complete(self, file_path):
        filename = os.path.basename(file_path)
        self.dialog = MDDialog(
            title="✅ Download Complete!",
            text=f"Video saved to:\n{filename}",
            buttons=[
                MDRaisedButton(
                    text="Open Folder",
                    on_release=self.open_downloads_folder
                ),
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()
    
    def open_downloads_folder(self, instance=None):
        downloads_folder = self.get_downloads_folder()
        if platform == 'win':
            os.startfile(downloads_folder)
        elif platform == 'linux':
            os.system(f'xdg-open "{downloads_folder}"')
        elif platform == 'macosx':
            os.system(f'open "{downloads_folder}"')
        elif platform == 'android':
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            
            intent = Intent(Intent.ACTION_VIEW)
            intent.setDataAndType(Uri.parse("file://" + downloads_folder), "resource/folder")
            PythonActivity.mActivity.startActivity(intent)
        
        self.dialog.dismiss()
    
    def reset_ui(self, dt=None):
        self.progress_bar.opacity = 0
        self.percent_label.opacity = 0
        self.download_btn.disabled = False
        self.download_percent = 0
        self.progress_bar.value = 0
    
    def show_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def update_status(self, message):
        self.download_status = message
        self.status_label.text = message

if __name__ == "__main__":
    UniversalVideoDownloader().run()