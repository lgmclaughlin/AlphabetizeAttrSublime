Synopsis
========
This is a simple packaged plugin for Sublime Text that will allow one to alphabitize html attributes inside a tag. Simply highlight the tag you would like alphabitized (multiple region selection is allowed) quickly by hitting [ctrl + alt + a].

Usage
=====
Highlight tag (or use multiple selection for multiple tags) and press ctrl + alt + a (super + alt + a for OS X). Alternatively, open the Selection Menu and click Alphabetize Attributes.

In each region of selection, the plugin will find the FIRST tag in said region and alphabetize the tags from only that tag. Everything else will remained unchanged. If no tag is found or a tag is started but never finished, nothing will be changed.

Motivation
==========
I've been getting into using Angular for writing online applications and quickly discovered that attributes and Angular directives inside HTML tags can quickly pile up. As such it gets tough to scan the attributes and see which have already been applied. To remedy this, it is convenient to have the attributes alphabetized. This way, once can scan the attributes easily and find the one they are checking for.

Installation
============
For now, the package can only be installed through the following method:

1. Download [EscapeHTML.sublime-package]
2. Place package into 
  * Windows: %APPDATA%\Sublime Text [version]\Installed Packages
  * OS X:    ~/Library/Application Support/Sublime Text [version]/Installed Packages
  * Linux:   ~/.config/sublime-text-[version]/Installed Packages

Sublime takes care of the rest!

If this gets put on Package Control, I'll modify this README.
