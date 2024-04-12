# Folder Synchronization

## Overview

This program synchronizes two folders: source and replica. The 
program should maintain a full, identical copy of source folder at replica folder.

## Features

- Synchronization must be one-way: after the synchronization content of the 
replica folder should be modified to exactly match content of the source 
folder;

- Synchronization should be performed periodically.

- File creation/copying/removal operations should be logged to a file and to the 
console output;

- Folder paths, synchronization interval and log file path should be provided 
using the command line arguments;

## How to execute

`python3 sync.py <source-folder-path> <replica-folder-path> <log-file-path> <sync-interval>`
