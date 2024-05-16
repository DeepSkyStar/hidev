#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-09-06 23:51:36
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-16 18:04:01
FilePath: /hidev/common.py
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

class Common(object):
    """Common Setting."""
    DEV_INSTALL_DIR = os.path.join(os.path.expanduser('~'), ".hidev")
    pass
