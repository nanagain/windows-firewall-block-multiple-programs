#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tree Blocking Firewall

Nan Again <nanagain@pm.me> https://github.com/nanagain

This program creates a Windows NT Command Script file (*.cmd) with Windows Firewall rules.
Use it to block network traffic from executable files.
"""
import os
import sys
import getopt


def usage():
    u = f"""
Usage:

    python {sys.argv[0]} -r MyRuleName -p "/path/one" -p "/path/two" -p "/path/three"

    -h or --help: print this
    -r or --rule: set rule name
    -p or --path: set directory base path

Examples:

    python {sys.argv[0]} -h
    python {sys.argv[0]} -r MyRule -p "C:\\Pogram1\\"
    python {sys.argv[0]} -r MyOtherRule -p "C:\\Program2\\" -p "C:\\Program3\\" -p "C:\\Program4\\"

A big example:

    python main.py -r IWantToBlock -p "C:\\Program Files (x86)\\Adobe" -p "C:\\Program Files\\7-Zip" -p "C:\\Program Files\\BiglyBT"
    """
    print(u)


def main():
    print('Tree Blocking Firewall')
    print('')
    print('This program creates a Windows NT Command Script file (*.cmd) with Windows Firewall rules.')
    print('Use it to block network traffic from executable files.')
    print('Enjoy! ;)')
    print()

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hr:p:', ['rule=', 'path='])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    rule = ''
    directories = []
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(0)
        elif opt in ('-r', '--rule'):
            rule = arg
        elif opt in ('-p', '--path'):
            directories.append(arg)

    if rule == '' or len(directories) == 0:
        print("Syntax error, so nothing to do. Try with -h.")
        exit(1)

    command = ['@echo off\n\n']
    for directory in directories:
        for root, subdirs, files in os.walk(directory):
            for file in files:
                candidate = os.path.join(root, file)
                if candidate.lower().endswith('.exe'):
                    print(f'Get: "{candidate}"')
                    command.append(f'netsh advfirewall firewall add rule name="{rule}" dir=in  action=block program="{candidate}"\n')
                    command.append(f'netsh advfirewall firewall add rule name="{rule}" dir=out action=block program="{candidate}"\n')
    if len(command) > 1:
        batch = f'fw_{rule}.cmd'
        with open(batch, 'w') as f:
            f.writelines(command)
            f.write('\npause\n')
        print(f'\nDone. Check "{batch}" and run it with elevated privileges.')
    else:
        print('Executables not found. Nothing to do.')


if __name__ == '__main__':
    main()
