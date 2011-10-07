#!/usr/bin/env python3
"""
This app verifies all zip files in a recursive directory and then optionally 
deletes bad files. By default it runs on PWD but you can feed it a directory to
change that. It doesn't delete by default, just notifies.
"""
import sys
import os
from zipfile import ZipFile, BadZipfile
import argparse


def parseArguments():
    """This sets up all the arguments the program takes and then returns the
    results of parse_args() so none of it needs to be done in main
    """
    parser = argparse.ArgumentParser(description="Verify a directory of zip\
        files & optionally purge bad ones")
    parser.add_argument('directory', nargs='?', default=os.getcwd(),
        help="Optional directory to scan, defaults to CWD")
    parser.add_argument('--purge', '-p', action='store_true',
        help="Delete bad files.")
    parser.add_argument('--verbose', '-v', action='store_true',
        help="Use dots to show progress.")
    return parser.parse_args()


def getRecursiveFiles(directory):
    """ This isn't too special really,
    just a copy paste function for crawling a path and getting all the files
    Feed it a directory and it uses os.walk to return array of files
    """
    fileArray = []
    for (dirname, subdirectories, files) in os.walk(directory):
        for filename in files:
            fileArray.append(os.path.join(dirname, filename))
    return fileArray


def checkZip(file, purge=False, verbose=False):
    """
    Use Zip to see if the file is valid and prints the name of failed files to
    stdout. If purge is set to true it will also delete the file.
    In verbose mode it will print a dot for every good file as well.
    """
    global zip
    try:
        zip = ZipFile(file)
        if zip.testzip() == None:
            if verbose:
                sys.stdout.write('.')
                sys.stdout.flush()
        else:
            if verbose:
                print()
            print("File", file, "failed with corrupted files")
            if purge:
                os.remove(file)
    except BadZipfile:
        if verbose:
            print()
        print("File %s failed with flying colors. Not a valid zip." % file)
        if purge:
            os.remove(file)
    finally:
        zip.close()


if __name__ == '__main__':
    args = parseArguments()
    if args.verbose:
        print("Recursively getting an index of all .zip files in ", args.directory)
    zipFiles = [file for file in getRecursiveFiles(args.directory)
             if file[-4:] == ".zip"]
    print(len(zipFiles), "files indexed. Running tests.")
    for file in zipFiles:
        checkZip(file, args.purge, args.verbose)
    if args.verbose:
            print()
    print("Done!")
