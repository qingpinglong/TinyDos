# TinyDos

In order to store files on a drive, the drive must have a number of data structures stored on it. These data
structures are sometimes referred to as metadata - data about data. This information has to be stored on the
drive so that when the drive is attached to a computer the operating system can make sense of what is stored.

we implement a very simple disk operating system called TinyDOS which provides the ability to store and retrieve 
data on a virtual drive and allows inspection of that data using cat or similar commands at any time during the 
execution of a program which uses the virtual drive.
