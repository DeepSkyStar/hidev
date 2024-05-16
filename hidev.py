#!/usr/bin/env python3
# coding=utf-8
'''
Author: Cosmade
Date: 2022-09-06 23:51:36
LastEditors: deepskystar deepskystar@outlook.com
LastEditTime: 2024-05-16 18:04:19
FilePath: /hidev/hidev.py
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

from hi_basic import *
from flutter_setup import *
from android_setup import *
import os
import argparse
import textwrap


def __info(args):
    curpath = os.path.dirname(os.path.abspath(__file__))
    appinfo = HiAppInfo(curpath)
    print(appinfo.name + " " + appinfo.version + " by " + appinfo.owner if appinfo.owner else "Unknown")
    pass


def __flutter(args):
    if args["install"]:
            FlutterSetup().install()
    else:
        HiLog.info(HiText("menu_flutter_nothing", "Nothing happens."))
    pass


def __android(args):
    is_fix_bigsur = args["fix_bigsur"]
    if is_fix_bigsur:
        AndroidSetup.fix_install_bug()
    else:
        HiLog.info(HiText("menu_android_nothing", "Nothing happens."))
    pass


def __setup_parser():
    # Define the menu.
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
        hidev
        This is the hidev project.
        Thank you for used.
        """),
        epilog=textwrap.dedent("""
        """)
        )

    # Create sub commands.
    subparsers = parser.add_subparsers(
        title="Command List",
    )

    # Add command for show app info.
    parser_info = subparsers.add_parser(
        name="info",
        help="View tool's version and owner."
        )

    parser_info.set_defaults(func=__info)

    # Add flutter tools.
    parser_flutter = subparsers.add_parser(
        name="flutter",
        help="Flutter's tools"
        )

    parser_flutter_group = parser_flutter.add_mutually_exclusive_group()

    parser_flutter_group.add_argument(
        '-i',
        '--install',
        help=HiText("menu_flutter_install_desc", "Auto install and update to the newest version."),
        action="store_true"
        )

    parser_flutter.set_defaults(func=__flutter)

    # Add android tools.
    parser_android = subparsers.add_parser(
        name="android",
        help="Android's tools"
        )

    parser_android_group = parser_android.add_mutually_exclusive_group()

    parser_android_group.add_argument(
        '--fix-bigsur',
        help=HiText("menu_android_fix_bigsur_desc", "Fix android studio cannot install bug."),
        action="store_true"
        )

    parser_android.set_defaults(func=__android)

    # parse the input.
    args = parser.parse_args()

    if len(vars(args)) == 0:
        # if no input print help.
        parser.print_help()
    else:
        # select the function
        args.func(vars(args))
    pass


def main():
    """Entry."""
    __setup_parser()
    pass


if __name__ == "__main__":
    main()
    pass
