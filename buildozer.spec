[app]
title = UniversalVideoDownloader
package.name = universalvideodownloader
package.domain = org.jubito.uvd
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
orientation = portrait
icon = appicon.png
# (Python deps)
requirements = python3,kivy==2.2.1,kivymd,yt-dlp,pyrogram,tgcrypto,requests,android,libffi
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (for Telegram video downloads and web browsing)
android.use_fork = False
android.allow_backup = True
android.minapi = 21
android.ndk = 23b
android.api = 33
android.release_artifact = apk  
android.archs = armeabi-v7a, arm64-v8a
android.gradle_dependencies = com.android.support:appcompat-v7:28.0.0

# ✅ Correct SDK/NDK paths (set in GitHub Actions)
android.sdk_path = /home/runner/android-sdk
android.ndk_path = /home/runner/android-sdk/ndk/25.2.9519653

# ✅ Release signing (ensure your keystore is present or set this via GitHub Secrets)
android.release_keystore = keystore/my-release-key.jks
android.release_store_password = pass@123
android.release_key_alias = key_alias
android.release_key_password = pass@123

# ✅ Use the latest stable python-for-android branch
p4a.branch = develop
# p4a.fork =  # Leave blank unless you have a custom fork
