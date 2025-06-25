[app]
title = UniversalVideoDownloader
package.name = universalvideodownloader
package.domain = org.jubito.uvd
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
orientation = portrait

# (Python deps)
requirements = python3,kivy,kivymd,yt-dlp,pyrogram,tgcrypto
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (for Telegram video downloads and web browsing)
android.use_fork = False
android.allow_backup = True
android.minapi = 21
android.ndk = 23b
android.api = 33
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0
