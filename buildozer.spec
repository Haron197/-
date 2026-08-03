[app]
title = InspectionApp
package.name = inspectionapp
package.domain = org.haron
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 0.1
requirements = python3,kivy==2.2.1,kivymd==1.2.0,pillow
orientation = portrait
osx.kivy_version = 2.2.1
fullscreen = 0
android.presplash_color = white
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
