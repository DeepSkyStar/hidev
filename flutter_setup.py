#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-09-06 23:51:36
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-16 18:05:41
FilePath: /hidev/flutter_setup.py
Description: 

Copyright 2024 Cosmade

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import os
import sys
import shutil
import platform
import requests
import zipfile
from hi_basic import *
from common import *


class FlutterSetup(object):
    """Install Flutter setup."""

    _MAC_VER_URL = "https://storage.flutter-io.cn/flutter_infra_release/releases/stable/macos/flutter_macos_3.22.0-stable.zip"
    _MAC_ARM64_VER_URL = "https://storage.flutter-io.cn/flutter_infra_release/releases/stable/macos/flutter_macos_arm64_3.22.0-stable.zip"
    _LINUX_VER_URL = "https://storage.flutter-io.cn/flutter_infra_release/releases/stable/linux/flutter_linux_3.22.0-stable.tar.xz"
    _PATH_CONTENT = """
# Setting PATH for flutter
export flutter_BIN="<BIN_PATH>"
export PATH="${PATH}:${flutter_BIN}"
"""

    def __init__(self) -> None:
        pass

    def __install_url(self) -> str:
        system = platform.system()
        if system == "Darwin":
            if platform.processor() == "arm":
                return self._MAC_ARM64_VER_URL
            return self._MAC_VER_URL
        elif system == "Linux":
            return self._LINUX_VER_URL
        elif system == "Windows":
            raise SystemError("Not support windows yet!")
        else:
            raise SystemError("Not support windows yet!")
        return ""

    def install(self, path: str = Common.DEV_INSTALL_DIR) -> None:
        """Install hidev."""
        # Check cache.
        cache_path = HiPath.cachepath("hidev")
        if not os.path.exists(cache_path):
            os.mkdir(cache_path)

        # Download file.
        cache_file = os.path.join(cache_path, "flutter-install-file.zip")
        if os.path.exists(cache_file):
            os.remove(cache_file)

        self.__request_file(path=cache_file)

        if not os.path.exists(path):
            HiFile.ensure_dirs(path)

        # unzip file.
        unzip_file = os.path.join(path, "flutter")
        if os.path.exists(unzip_file) and os.path.isdir(unzip_file):
            shutil.rmtree(unzip_file)
        elif os.path.exists(unzip_file):
            os.remove(unzip_file)

        os.mkdir(unzip_file)
        if self.__install_url() == self._MAC_VER_URL or self.__install_url() == self._MAC_ARM64_VER_URL:
            self.__unzip_file(src_path=cache_file, dst_path=unzip_file)
        elif self.__install_url() == self._LINUX_VER_URL:
            self.__untar_file(src_path=cache_file, dst_path=unzip_file)
        else:
            raise SystemError("Not Support Yet!")

        # Add path
        HiSys.setup_path(
            content=FlutterSetup._PATH_CONTENT,
            bin_path=os.path.join(unzip_file, "flutter/bin")
            )
        HiLog.info(HiText("flutter_setup_add_to_path", "Path added."))

        # Clear cache.
        os.remove(cache_file)
        pass

    def __request_file(self, path: str) -> bool:
        request = requests.get(url=self.__install_url(), stream=True, allow_redirects=True)
        file_size = int(request.headers['Content-Length'])
        download_size = 0
        with open(path, "wb+") as file:
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    download_size += len(chunk)
                    percent = download_size * 1.0 / file_size
                    print("\r", end="")
                    print("Downloading: {:.1%} >".format(percent), "▓" * (int(percent * 100) // 2), end="")
                    sys.stdout.flush()
        print("\n")
        HiLog.info(HiText("flutter_setup_download_finished", "Download finished."))
        return True

    def __unzip_file(self, src_path: str, dst_path: str) -> bool:
        src_file = zipfile.ZipFile(src_path, "r")
        for info in src_file.infolist():
            src_file.extract(member=info, path=dst_path)
            os.chmod(
                path=os.path.join(dst_path, info.filename),
                mode=(info.external_attr >> 16)
            )
            HiLog.info(HiText("flutter_setup_unziping", "Unziping: ") + info.filename)
        print("\n")
        HiLog.info(HiText("flutter_setup_unzip_finished", "Unzip finished."))
        pass

    def __untar_file(self, src_path: str, dst_path: str) -> bool:
        os.system("tar xf " + src_path + " --directory=" + dst_path)
        HiLog.info(HiText("flutter_setup_unzip_finished", "Unzip finished."))
        pass

    pass
