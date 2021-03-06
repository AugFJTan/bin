# File  : bpgen.py
# Author: AugFJTan
# Last Modified 7 Feb 2018 12:37 PM

import sys
import argparse
import platform
import time

available_languages = ("c", "cpp", "java", "python", "html")
comment_styles = ("c", "cpp", "python", "html")
author = "AugFJTan"

class Boilerplate:
	def __init__(self, filename, ext, language, style, content_flag, metadata_flag):
		self.filename = filename
		self.ext = ext
		self.language = language
		self.style = style
		self.content_flag = content_flag
		self.metadata_flag = metadata_flag
	
	def output_file(self):
		comment_start  = ""
		comment_middle = ""
		comment_end    = ""
		metadata = ""
	
		if self.style == "C":
			comment_start  = "/*"
			comment_middle = " *"
			comment_end    = "\n */"
		elif self.style == "C++":
			comment_start  = "//"
			comment_middle = "//"
		elif self.style == "Python":
			comment_start  = "#"
			comment_middle = "#"
			if self.metadata_flag:
				metadata = "\n# Python " + platform.python_version()
		elif self.style == "HTML":
			comment_start = "<!--\n"
			comment_end = "\n-->"
		
		current_time = time.strftime("%d %b %Y %I:%M %p", time.localtime())

		comment = """\
{3} File       : {0}
{4} Description: 
{4}              
{4} Author     : {1}{6}
{4} Last Modified {2}{5}

""".format(self.filename, author, current_time, comment_start, comment_middle, comment_end, metadata)

		content = ""
		
		if self.ext == "h":
			content += """\
#ifndef {0}
#define {0}



#endif {1} {0}""".format(self.filename.replace('.', '_').upper(), comment_start)
			if self.style == "C":
				content += " */\n"
			else:
				content += "\n"
		elif self.language == "C" or self.language == "C++":
			if self.content_flag:
				if self.language == "C":
					content += "#include <stdio.h>\n"
				elif self.language == "C++":
					content += "#include <iostream>\n"

				content += """
int main()
{
	
	
	return 0;
}
"""
		elif self.language == "Java":
			dot_index = self.filename.find('.')
			content += "public class " + self.filename[:dot_index] + " {"
			if self.content_flag:
				content += """
	public static void main(String args[]) {
		
	}
"""
			else:
				content += "\n\t\n"
			content += "}\n"
		elif self.language == "HTML":
			if self.content_flag:
				content += """\
<!DOCTYPE html>
<html>
	<head>
		<title>{}</title>
	</head>
	<body>
		
	</body>
</html>
""".format(self.filename)

		output = comment + content

		file = open(self.filename, 'w')
		file.write(output)	
		file.close()

def get_language_string(language):
	if language == "c":
		return "C"
	elif language == "cpp":
		return "C++"
	elif language == "java":
		return "Java"
	elif language == "python":
		return "Python"
	elif language == "html":
		return "HTML"
		
def validate_filename(filename):
	invalid_characters = ('\\', '/', ':', '*', '?', '<', '>', '|')
	
	for i in invalid_characters:
		if filename.find(i) != -1:
			print("error: the character '{}' cannot be used in a filename".format(i))
			sys.exit()
	
	dot_index = filename.find('.')
	
	if dot_index == -1:
		print("error: filename must end with file extention")
		sys.exit()
	
	return [filename, filename[dot_index+1:]]

def derive_language(ext):
	if ext == "c" or ext == "h":
		language = "C"
	elif ext == "cpp":
		language = "C++"
	elif ext == "java":
		language = "Java"
	elif ext == "py" or ext == "pyw":
		language = "Python"
	elif ext == "html":
		language = "HTML"
	else:
		print("error: '{}' is not a default file extention; please specify a language".format(ext))
		sys.exit()
	
	return language
	
def validate_language(language):
	if language in available_languages:
		return get_language_string(language)
	else:
		print("error: '{}' is not available as a language option".format(language))
		sys.exit()

def validate_comment_style(language, style):
	if style not in comment_styles:
		print("error: '{}' is not available as a comment style".format(style))
		if language == "Java":
			print("hint : Java accepts C or C++ comment styles")
		sys.exit()
	
	style = get_language_string(style)
	
	invalid_style = False
	
	if language == "C" or language == "C++" or language == "Java":
		if style != "C" and style != "C++":
			invalid_style = True
	elif language == "Python":
		if style != "Python":
			invalid_style = True
	elif language == "HTML":
		if style != "HTML":
			invalid_style = True
	
	if invalid_style:
		print("error: {} comment style is incompatible with {}".format(style, language))
		sys.exit()
	
	return style

def eval_cmd_line_options():
	parser = argparse.ArgumentParser(prog="bpgen", description="Create boilerplate code to save on typing!")
	# optional arguments
	parser.add_argument("-n", "--nocontent", help="output block comment only and leave out content", action="store_true")
	parser.add_argument("-m", "--metadata", help="output language metadata in block comment", action="store_true")
	parser.add_argument("--lang", help="set boilerplate code to specified language syntax")
	parser.add_argument("--style", help="set comment style")
	# positional arguments
	parser.add_argument("file", help="file to be output")
	
	args = parser.parse_args()
	
	# defaults
	content_flag = True
	metadata_flag = False
	
	filename, ext = validate_filename(args.file)
	
	if args.lang == None:
		# set language based on extention
		language = derive_language(ext)
	else:
		# set language based on command line argument
		language = validate_language(args.lang)
	
	if args.style == None:
		if language == "Python":
			style = "Python"
		elif language == "C++" or language == "Java":
			style = "C++"
		elif language == "HTML":
			style = "HTML"
		else:
			style = "C"
	else:
		style = validate_comment_style(language, args.style)
	
	if args.nocontent:
		content_flag = False
		
	if args.metadata:
		metadata_flag = True
		
	return Boilerplate(filename, ext, language, style, content_flag, metadata_flag)

boilerplate = eval_cmd_line_options()
boilerplate.output_file()