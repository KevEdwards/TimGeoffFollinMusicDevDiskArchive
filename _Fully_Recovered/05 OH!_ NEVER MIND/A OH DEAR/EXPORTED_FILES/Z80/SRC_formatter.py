#!/usr/bin/python3

# Title:		Formatter for Tatung Einstein Z80 and 6502 plain text ( ASCII ) SRC files
#               This utility was originally named format_z80.py, but it works for 6502 too so it got renamed!
# Authors:		Dean Belfield
#               Kevin Edwards ( various tweeks! )

# Created:		06/05/2023
# Last Updated:	04/03/2024
#
# Modinfo:
# 04/03/2024: KE EOF token 0xff is now processed. At the moment it is only accepted if at start of file so it better handles corrupt files. Hacky, but works well enough.
#             KE Renamed this file 'SRC_formatter.py'
# 27/02/2024: KE Re-worked slightly to process all *.src and *.bak files recursively. Output files have .txt appended! You need to manually separate out the Z80 source files!
#                Fix to copy comment lines as they are and not get confused by hex values 0x80-0xff. Some comment lines contain these values as ASCII art!
#                'Fixes' to help with corrupt files = incorrect EOF mid-file due to corruption.
#                Now uses utf-8 encoding for the output file to cope with strange characters!
# 06/05/2023:	Tweaked for comments on first line, and file EOL

import sys
import os
import struct
from pathlib import Path

def list_files(filepath, filetype):
   print( 'list_files', filepath )
   paths = []
   for root, dirs, files in os.walk(filepath):
      print( 'root', root )
      for file in files:
         if file.lower().endswith(filetype.lower()):
            print( file )
            paths.append(os.path.join(root, file))
   return(paths)


def format_file( name ):
    # Open the file for reading
    #
#    name = sys.argv[1]										# Get the filename
    full_path = os.path.expanduser(name)					# Expand the full path to the file and
    file = open(full_path, "rb")							# Open it up as a binary file

    file_stdout = sys.stdout								        # Store the current stdout file handle
    sys.stdout = open(full_path + ".TXT", "w", encoding='utf-8')	# Redirect stdout for the detokenised file output, use UTF-8 as encoding some characters fails otherwise ( weird chars in some of Tim's src comments! )

    col = 0			# Current column # (used for tabbing the listing)
    comment = False	# Are we in a comment?
    string = False	# Are we in a string?
    label = False	# Does this line contain a comment?
    indent = 16		# Indent for first column
    line = ""		# Storage for line

    # Iterate through the file
    #
    while True:
        data = file.read(1)									# Read 1 byte into the buffer data
        if not data:										# If EOF then exit the loop
            break			
        byte = data[0]										# Fetch the byte 
        if byte == 0x1A and col == 0:                       # EOF 'byte' ( 0x1A ) only accepted when it's at the start of a line. This is hacky fix for corrupt files that have 0x1A splattered in the middle of the source file.
            break

        if byte == 0xFF and col == 0:                       # EOF 'byte' ( 0xFF ) only accepted when it's at the start of a line. This is hacky fix for corrupt files that have 0x1A splattered in the middle of the source file.
            break

        asc = chr(byte)
        if asc == ";":										# Flag when in a comment or string literal
            comment = True

        if(byte < 0x80) or comment:     					# Check bounds - caveat...comments can have character values >= 0x80, so output as they are! Tim used funny characters in some comment blocks.
            line += asc
            col += 1										# Increment the column number
        else:								    			# Otherwise
            token = "<UNKNOWN " + hex(byte) + ">"	        # It's an invalid token output this
            line += token
#            print(token, end="")							# Print it
            col += len(token)								# Adjust column by the width of the token

        if asc == '"':
            string = not string
        if asc == ":" and not comment and not string:		# If it is a colon (following a label) and not in comment or string then indent
            line += " "*(indent-col)						# Indent
            label = True	
        if byte == 0x0D:									# If it is CR then
            if not label and line[0] != ";":				# If this line doesn't contain a label and the first character isn't a comment
                line = (" "*indent) + line 					# Indent 
            print(line, end="")								# Print the line
            col = 0											# Reset the column to 0
            comment = False									# Reset the comment flag
            label = False									# Reset the label flag	
            line = ""										# Reset the line

    file.close()											# We've done so close the files

    sys.stdout.close()										# Close and restore stdout
    sys.stdout = file_stdout



# Main Entry Point

# This is the default 'root' location to use, the current working directory!
my_files_list = list_files( os.getcwd(), '.src' )
my_files_list += list_files( os.getcwd(), '.bak' )

for fpath in my_files_list:
   print('\t%s' % fpath)
   format_file( fpath )
