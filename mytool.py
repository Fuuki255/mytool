# -*- coding: UTF-8 -*-

MYTOOL_PROGRAMMER	= "ふうき"
MYTOOL_VERSION		= {2, 4, 3}


##### Libraries #####

import os;
import fnmatch;
import importlib.util;
import time;
import _io;

from math import *;

# Install library in use

libOpencv2 = None;
libPilImage = None;
libNumpy = None;

libGoogleTranslator = None;

libYoutube = None;
libAudioSegment = None;

def CheckLibrary(libraryName: str) -> bool:
	spec = importlib.util.find_spec(libraryName);
	return spec is not None;


def InstallLibrary(libraryName: str) -> bool:
	if (not hasattr(InstallLibrary, "installCommands")):
		InstallLibrary.installCommands = ["py -m pip", "pip"];
	
	# Execute command -> try another command
	while (InstallLibrary.installCommands):
		if (os.system("%s install %s" % (InstallLibrary.installCommands[0], libraryName))):
			InstallLibrary.installCommands.pop(0);
			continue;

		return True;
	
	# ERROR: No command to call 'pip'
	print("ERROR: InstallLibrary: Couldn't found 'pip'");
	return False;


def __Loads(modu, installs: dict) -> int:
	if (modu != None):
		return 1;
	
	for item in installs.items():
		if (not CheckLibrary(item[0]) and not InstallLibrary(item[1])):
			return 0;
	
	return 2;


def __LoadOpencv2():
	global libOpencv2;
	ret = __Loads(libOpencv2, {"cv2": "opencv-python"});
	
	if (ret == 1):
		return libOpencv2;
	if (ret == 2):
		import cv2;
		libOpencv2 = cv2;
		return libOpencv2;
		
	return None;

def __LoadGoogleTranslate():
	global libGoogleTranslator;
	ret = __Loads(libGoogleTranslator, {"googletrans": "googletrans==4.0.0rc1"});
	
	if (ret == 1):
		return libGoogleTranslator;
	if (ret == 2):
		import googletrans;
		libGoogleTranslator = googletrans.Translator();
		return libGoogleTranslator;
		
	return None;

def __LoadPIL_Image():
	global libPilImage;
	ret = __Loads(libPilImage, {"PIL": "pillow"});
	
	if (ret == 1):
		return libPilImage;
	if (ret == 2):
		from PIL import Image;
		libPilImage = Image;
		return libPilImage;
		
	return None;

def __LoadNumpy():
	global libNumpy;
	ret = __Loads(libNumpy, {"numpy": "numpy"});
	
	if (ret == 1):
		return libNumpy;
	if (ret == 2):
		import numpy;
		libNumpy = numpy;
		return libNumpy;
		
	return None;

def __LoadlibYoutube():
	global libYoutube;
	ret = __Loads(libYoutube, {"pytubefix": "pytubefix"});
	
	if (ret == 1):
		return libYoutube;
	if (ret == 2):
		from pytubefix import YouTube;
		libYoutube = YouTube;
		return libYoutube;
		
	return None;

def __LoadPydub():
	global libAudioSegment;
	ret = __Loads(libAudioSegment, {"pydub": "pydub", "ffmpeg": "ffmpeg"});
	
	if (ret == 1):
		return libAudioSegment;
	if (ret == 2):
		import pydub;
		libAudioSegment = pydub.AudioSegment;
		return libAudioSegment;
		
	return None;



##### Constants #####

# Environment

IS_WIN: bool = os.name == "nt";


# Terminal Color

if (IS_WIN):
	os.system("color");

TERMCOLOR_CLEAR: str = "\033[0m";

TERMCOLOR_RED: str = "\033[31m";
TERMCOLOR_GREEN: str = "\033[32m";
TERMCOLOR_YELLOW: str = "\033[33m";
TERMCOLOR_BLUE: str = "\033[34m";

TERMCOLOR_BOLD: str = "\033[1m";
TERMCOLOR_GRAY: str = "\x1b[2m"



# Constant Time

DAY:	int = 24 * 60;
HOUR:	int = 60;


# Other

true: bool = True;
false: bool = False;


# Methods

METHODCOLOURS = [
	TERMCOLOR_GREEN,
	TERMCOLOR_BOLD + TERMCOLOR_YELLOW,
	TERMCOLOR_BOLD + TERMCOLOR_BLUE,
	TERMCOLOR_YELLOW,
	TERMCOLOR_BOLD + TERMCOLOR_GREEN,
	TERMCOLOR_BLUE,
	"",
	"\x1b[2m",
	TERMCOLOR_RED,
];

METHOD_CLASS	= 0;
METHOD_FUNCTION	= 1;
METHOD_STRUCTURE= 2;
METHOD_STRING	= 3;
METHOD_NUMBER	= 4;
METHOD_BOOL		= 5;
METHOD_NORMAL	= 6;
METHOD_NONE		= 7;
METHOD_ERROR	= 8;



##### Commands #####

class ClassClearScreen:
	def __repr__(self):
		self.Clear();
		return "";
	def __call__(self):
		self.Clear();
	
	def Clear(self):
		if (IS_WIN):
			os.system("cls");
		else:
			print("\x1b[2J\x1b[0;0H", end="");
		return "";

class ClassChangeDirectory:
	def __repr__(self):
		return os.getcwd();
	def __call__(self, path = ""):
		self.set(path);

	def set(self, path = ""):
		if (not path):
			return;
		try:
			os.chdir(path);
		except FileNotFoundError:
			print("ERROR: Cwd: Couldn't find path!");

class ClassListDirectory:
	def __repr__(self):
		self.Listdir();
		return "";
	def __call__(self, path = ""):
		self.Listdir(path);

	def Listdir(self, path = ""):
		os.system(("dir " if IS_WIN else "ls ") + ('"' + path + '"' if (path) else ""));


def ListTree(top = os.curdir, patterns = ("*")):
	topLength = len(top);
	
	for r, ds, fs in os.walk(top):
		totalSpace = r[topLength:].count(os.sep);
		
		files = [fn for pattern in patterns for fn in fnmatch.filter(fs, pattern)];
		
		if (files and r != top):
			print(TERMCOLOR_BOLD + r[topLength+1:] + os.sep + TERMCOLOR_CLEAR);
		
		for fn in files:
			print("\t" * totalSpace + fn);

def Touch(files: str, *others: list[str]):
	# Touch files input by multi-line or path split text
	for filename in [fn for fn in files.split('\n') for fn in fn.split(os.pathsep)]:
		if (filename and not os.path.exists(filename)):
			open(filename, "x");
	
	# Touch files input by multi-args
	for filename in others:
		if (filename and type(filename) == str and not os.path.exists(filename)):
			open(filename, "x");


cls = CLS = clear = CLEAR = ClassClearScreen();

cd = CD = cwd = CWD = chdir = CHDIR = ClassChangeDirectory();

ls = LS = listdir = LISTDIR = ClassListDirectory();


##### Ask Open File #####

def AskOpenFile(fileTypes: list = [tuple[str, str]]):
	from tkinter import filedialog;
	return filedialog.askopenfile(filetypes = fileTypes);


##### Images Methods #####

def LoadImage(filename: str):
	__LoadOpencv2();
	return libOpencv2.imread(filename);


def ShowImage(image = None, size: list[int, int] = [0, 720], windowName: str = "imshow", wait: int = 0):
	"""Show Image and wait untail window closed
	
	@param image : Image input for show it to window, you can enter file path, PIL Image or Opencv Image.
	@param windowName : Preview window name (default: "imshow")
	@param wait : How long to show image (default: 0)
	
	"""
	__LoadOpencv2();

	# Different Image Format Supports
	if (type(image) == str):
		if (not os.path.isfile(image)):
			print("ERROR: ShowImage: File not exists!");
			return;
		
		image = libOpencv2.imread(image);
	
	if (image == None):
		file = AskOpenFile([("Image Files", "*.png *.jpg *jpeg *.webp *.ico")]);
	
		if (not file):
			return;
	
		image = LoadImage(file.name);
		file.close();
	
	className = type(image).__module__ + '.' + type(image).__name__;
	if (className[:4] == "PIL."):
		__LoadNumpy();
		image = libOpencv2.cvtColor(libNumpy.array(image.convert('RGB')), libOpencv2.COLOR_RGB2BGR);		# double convert since libPilImage not support to convert to BGR format.
	
	className = type(image).__module__ + '.' + type(image).__name__;
	if (className != "libNumpy.ndarray"):
		print("ERROR: ShowImage: Couldn\'t show \'" + className + "\'");
		return;

	# Show
	w = image.shape[0]; h = image.shape[1];
	
	if (size[0] != 0 and w > size[0]):
		h = h * size[0] / w;
		w = size[0];
	if (size[1] != 0 and h > size[1]):
		w = w * size[1] / h;
		h = size[1];
	
	image_scaled = libOpencv2.resize(image, (int(w), int(h)));
	libOpencv2.imshow(windowName, image_scaled);
	libOpencv2.waitKey(wait);


##### Video Methods #####

def LoadVideo(filename: str):
	__LoadOpencv2();

	video = libOpencv2.VideoCapture(filename);
	if (video.isOpened()):
		return video;

	print("ERROR: LoadVideo: Failed to load video!");
	video.release();
	return None;


def IsVaildVideo(video, errorFuncName: str = None) -> bool:
	"""if video vaild, return True. if no, return False.
	Giving errorFuncName will print error message if video invalid.
	"""

	if (type(video) != libOpencv2.VideoCapture):
		if (errorFuncName):
			print("ERROR: %s: %s is not a valid type." % [errorFuncName, type(video).__name__]);
		return False;
	if (not video.isOpened()):
		if (errorFuncName):
			print("ERROR: %s: Invalid video." % [errorFuncName]);
		return False;
	return True;


def ShowVideoCurrentFrame(video, windowName):
	"No debug including"

	ret, frame = video.read();

	if (ret):
		libOpencv2.imshow(windowName, frame);
		video.set(1, video.get(1) - 1);

	return ret, frame;


def PlayVideo(video = None, windowName: str = "imshow",
				maxWidth: int = 1920, maxHeight: int = 1080,
				pause: bool = False, loop: bool = False,
				fullscreen: bool = False, output: str = "output-"):
	__LoadOpencv2();

	destroyVideo = False;

	# Video input as filename: Load video
	if (type(video) == str):
		video = libOpencv2.VideoCapture(video);
		destroyVideo = True;
	
	# No video input: Ask for Load video
	if (video == None):
		from tkinter import filedialog;
		file = AskOpenFile([("Video files", "*.mp4 *.webm *.avi *.mov *.wmv *.flv"), ("All files", "*.*")]);
	
		if (not file):
			print("Quit PLayVideo: No file chosen!");
			return;

		video = libOpencv2.VideoCapture(file.name);
		file.close();
		destroyVideo = True;
	
	# Ivalid video: Print error and quit
	if (not IsVaildVideo(video, "PlayVideo")):
		return;

	# Reset video
	video.set(1, 0);

	# Get Video Information
	videoWidth = video.get(3);
	videoHeight = video.get(4);
	videoTotalFrames = video.get(7);

	videoFPS = video.get(5);
	videoDelay = int(1000 / videoFPS);

	# Callback function to keep window ratio
	def ResizeCallback(event, x, y, flags, param):
		libOpencv2 = param['libOpencv2'];
		windowName = param['windowName'];

		if event != libOpencv2.EVENT_MOUSEMOVE:
			# Get the new window size
			new_width = libOpencv2.getWindowImageRect(windowName)[2];
			new_height = int(new_width * param['ratio']);
			
			# Display the resized image
			libOpencv2.resizeWindow(windowName, (new_width, new_height));

	# Create Window
	if (videoWidth > maxWidth):
		videoWidth = maxWidth;
		videoHeight = videoHeight * (maxWidth / videoWidth);
	elif (videoWidth < maxWidth):
		videoWidth = videoWidth * (maxHeight / videoHeight);
		videoHeight = maxHeight;
	
	libOpencv2.namedWindow(windowName, (libOpencv2.WINDOW_FULLSCREEN if fullscreen else libOpencv2.WINDOW_NORMAL));
	libOpencv2.resizeWindow(windowName, int(videoWidth), int(videoHeight));
	libOpencv2.setMouseCallback(windowName, ResizeCallback, {'windowName': windowName, 'ratio': videoHeight / videoWidth, 'libOpencv2': libOpencv2});

	# Take Photo Variable
	outputIndex = 1;
	while (os.path.isfile(output + str(outputIndex) + ".png")):
		outputIndex += 1;

	# Play Video
	playing = not pause;
	frame: None;

	startTick = libOpencv2.getTickCount();
	endTick = 0;
	tickOfMS = libOpencv2.getTickFrequency() / 1000;

	while (True):
		try:
			if (playing):
				ret, frame = ShowVideoCurrentFrame(video, windowName);

				if (ret == False):
					if (loop == False):
						playing = False;
						continue;
					
					video.set(1, 0);
					ShowVideoCurrentFrame(video, windowName);

			# Delay
			endTick = libOpencv2.getTickCount();
			key = libOpencv2.waitKeyEx(int(videoDelay - min(videoDelay - 1, (endTick - startTick) / tickOfMS)));
			startTick = endTick;

			# Handle Event

			try:		# User closed window : Quit out
				libOpencv2.getWindowProperty(windowName, 0);
			except:
				print("Quit PlayVideo: Window chosed!");
				break;
			if (key == 27):			# ESC : Quit out
				print("Quit PlayVideo: ESC presed!");
				break;

			if (key == ord('t')):	# T : Take photo
				filename = output + str(outputIndex) + ".png";

				libOpencv2.imwrite(filename, frame);
				print("PlayVideo: Photo saved to " + filename);

				outputIndex += 1;
				continue;
			if (key == ord(' ')):	# SPACE : Switch playing
				playing = not playing;
				if (playing == True and video.get(1) == videoTotalFrames):
					video.set(1, 0);
				continue;
			if (key == ord('l')):
				loop = not loop;
				print("PlayVideo: Loop play is " + ("enable" if (loop) else "disable") + " now!");
				if (loop == True and playing == False):
					playing = True;
				continue;
			if (key == 0x7a0000):
				fullscreen = not fullscreen;
				libOpencv2.setWindowProperty(windowName, libOpencv2.WND_PROP_FULLSCREEN, (libOpencv2.WINDOW_FULLSCREEN if fullscreen else 0));
				continue;

			# Move offset
			offset = 0;

			if (key >= ord('0') and key <= ord('9')):
				offset = videoTotalFrames / 10 * (key - ord('0'));
			
			# 'A' : Move back 5 seconds
			elif (key == ord('a')):
				offset = video.get(1) - videoFPS * 5 - 1;
			
			# 'D' : Move front 5 seconds
			elif (key == ord('d')):
				offset = video.get(1) + videoFPS * 5;
			
			# ',' : Move back frame
			elif (key == ord(',')):
				offset = video.get(1) - 2;
			
			# '.' : Move front frame
			elif (key == ord('.')):
				offset = -1;
			else:
				continue;

			if (offset != -1):
				offset = round(max(0, min(offset, videoTotalFrames)));
				video.set(1, offset);

				if (offset != video.get(1)):
					print("ERROR: PlayVideo: Failed to move frame position (%d was expected but finally %d)" % (int(offset), int(video.get(1))));
			
			# Flush Frame after offset moved
			if (playing == False):
				ret, frame = ShowVideoCurrentFrame(video, windowName);
		except KeyboardInterrupt:
			print("Quit PlayVideo: CTRL+C interrupt");
			break;
	
	# Sure the window has closed
	try:
		libOpencv2.destroyWindow(windowName);
	except:
		pass;
	
	if (destroyVideo):
		video.release();


##### GIF Methods #####

def WriteGifFromFrames(frames: list, filename: str, duration: int, loop: int = 0):
	frames[0].save(filename, save_all=True, append_images=frames[1:], duration=duration, loop=loop);


def WriteGifFromVideo(video, filename: str, start: float = 0, end: float = -1, loop: int = 0):
	__LoadOpencv2();
	__LoadPIL_Image();

	if (not IsVaildVideo(video, "WriteGifFromVideo")):
		return;
	
	FPS = video.get(5);
	
	index = start * FPS;
	
	finallyFrame = 0;
	if (end == -1):
		finallyFrame = video.get(7);
	else:
		finallyFrame = end * FPS;
	
	
	video.set(1, index);
	frames = [];
	
	while (True):
		ret, frame = video.read();
	
		if (ret == False):
			break;
	
		frames.append(libPilImage.fromarray(libOpencv2.cvtColor(frame, libOpencv2.COLOR_BGR2RGB)));
		index += 1;
	
		if (index >= finallyFrame):
			break;
	
	WriteGifFromFrames(frames, filename, 1000 / FPS, loop = loop);



##### Attendence #####

class Attendance:
	class Row:
		def __init__(self, date, status, attendTime, lessonTime, room):
			self.date = date;
			self.status = status;
			self.attendTime = attendTime;
			self.lessonTime = lessonTime;
			self.room = room;
	
		def __repr__(self):
			return self.date + '\t' + self.status + '\t\t' + self.attendTime + '\t\t' + self.lessonTime + '\t' + self.room + '\n';
	
		__str__ = __repr__;
	
	
	def ValueTime(self, time: str):
		splited = time.split(":");
		value = 0;
		for part in splited:
			value *= 60;
			value += float(part);
		return value;
		
	def __init__(self, raw: str = None):
		self.rows = [];
	
		if (not raw):
			raise ValueError;
		
		if (raw.count('\n') == 0):
			raw = open(raw);
		
		if (type(raw) == _io.TextIOWrapper):
			file = raw;
			raw = file.read();
			file.close();
		
		for line in raw.splitlines():
			if (line.isspace()):
				continue;
	
			splited = line.split('\t');
			idx = 0;
			while (idx < len(splited)):
				if (not splited[idx]):
					splited.pop(idx);
				else:
					idx += 1;
			if (len(splited) < 5):
				continue;
	
			self.rows.append(self.Row(splited[0], splited[1], splited[2], splited[3], splited[4]));
    
	def __repr__(self):
		output = "\x1b[1mDate\t\t\tStatus\t\tAttend Time\tLesson Time\tRoom\x1b[0m\n";
		for row in self.rows:
			if (row.status == "Absent"):
				output += TERMCOLOR_RED + str(row) + TERMCOLOR_CLEAR;
			else:
				output += str(row);
		output += '\n';

		output += "Record Count: %d\n" % (len(self.rows));
		output += "Attend Time: %.2f hour\n" % (self.Attendance());
		output += "Miss Time: %.2f hour\n" % (self.Missed());
		return output;
	
	__str__ = __repr__;
	
	def Select(self, date = None, status = None, attendTime = None, lessonTime = None, room = None):
		result = Attendance();
	
		for row in self.rows:
			if (status and row.status != status):
				continue;
			if (lessonTime and row.lessonTime != lessonTime):
				continue;
	
			result.rows.append(row);
	
		return result;
	
	def Attendance(self, totalHour: int = 1):
		attendMintues = 0;
		for row in self.rows:
			if (row.status == "Absent"):
				continue;
	
			lessonTime_splited = row.lessonTime.split(" - ");
			lessonEnd = self.ValueTime(lessonTime_splited[1]);
	
			if (row.status == "Present"):
				attendMintues += lessonEnd - self.ValueTime(lessonTime_splited[0]);
				continue;
	
			attendMintues += lessonEnd - self.ValueTime(row.attendTime);
	
		return attendMintues / (totalHour * 60);
	
	def Missed(self, totalHour: int = 1):
		missedMintues = 0;
		for row in self.rows:
			if (row.status == "Present"):
				continue;
	
			lessonTime_splited = row.lessonTime.split(" - ");
			lessonStart = self.ValueTime(lessonTime_splited[0]);
	
			if (row.status == "Absent"):
				missedMintues += self.ValueTime(lessonTime_splited[1]) - lessonStart;
				continue;
	
			missedMintues += self.ValueTime(row.attendTime) - lessonStart;
	
		return missedMintues / (totalHour * 60);


##### Python Object #####

def CountStringShowLength(text: str) -> int:
	length: int = 0;
	for char in text:
		length += 1 + 1 - char.isascii();
	return length;


def DescriptObject(obj: any, language: str = "ja"):
	### 情報表示 ###
	objType = type(obj);
	print(TERMCOLOR_YELLOW + "クラス: %s.%s" % (
		objType.__module__,
		objType.__name__
	) + TERMCOLOR_CLEAR);

	### コメント表示 ###

	# コメントがない
	if (not obj.__doc__):
		print(TERMCOLOR_GRAY + "コメントがありません!" + TERMCOLOR_CLEAR);

	# 原文で表示
	elif (not language):
		print(obj.__doc__);
	
	# 訳文で表示
	else:
		__LoadGoogleTranslate();

		length = len(obj.__doc__);
		for i in range(length // 5000 + (1 if length % 5000 else 0)):
			content = libGoogleTranslator.translate(obj.__doc__[i * 5000  : i + 4999], dest = language);
			print(content.text);
	
	print();


def ListObjectMethods(obj: any, findname: str = None, details: bool = True, colors: bool = True):

	def AnalysisMethodType(obj: any, methodName: str, methodInfo: list):
		try:
			method = getattr(obj, methodName);
			methodClass = method.__class__;

			if (method == None):
				methodInfo[0] = METHOD_NONE;
				return;
		
			if (methodClass == bool):
				methodInfo[0] = METHOD_BOOL;
				methodInfo[2] = method;
				return;
		
			if (methodClass in [int, float]):
				methodInfo[0] = METHOD_NUMBER;
				methodInfo[2] = method;
				return;
		
			if (methodClass in [str, bytes]):
				methodInfo[0] = METHOD_STRING;
				methodInfo[2] = method;
				return;
		
			if (methodClass == type or methodClass.__name__ == "module"):
				methodInfo[0] = METHOD_CLASS;
				return;
		
			if (callable(method)):
				methodInfo[0] = METHOD_FUNCTION;
				return;
		
			methodInfo[0] = METHOD_STRUCTURE;
		except Exception as e:
			methodInfo[0] = METHOD_ERROR;
			methodInfo[2] = e;

	### Cleaning input ###
	if (findname):
		findname = findname.lower();

	### Collect method info ###
	firstResults = [];
	secondResults = [];
	thirdResults = [];
	longestNameLength = 0;
	
	for methodName in dir(obj):
		methodInfo = [METHOD_NORMAL, methodName, None];

		# Filter method if findname enabled
		if (findname):
			methodName_lowered = methodName.lower();
			if (methodName_lowered == findname):
				firstResults.append(methodInfo);
			
			elif (methodName_lowered.find(findname) == 0):
				secondResults.append(methodInfo);
			
			elif (methodName_lowered.find(findname) != -1):
				thirdResults.append(methodInfo);
		
			else:
				continue;
		else:
			firstResults.append(methodInfo);

		# Longest name length for print table
		longestNameLength = max(longestNameLength, len(methodName));

		# Collect method type and expand info if showdetails enabled
		if (details):
			AnalysisMethodType(obj, methodName, methodInfo);

	
	### Ready to print table ###

	termWidth = os.get_terminal_size()[0];
	
	longestNameLength = min(termWidth, longestNameLength + 1);
	rowLength	= termWidth // longestNameLength;
	indexLength	= termWidth // rowLength;
	
	firstResults.sort();
	secondResults.sort();
	thirdResults.sort();

	### Print method table ###

	index = 0;
	count = 0;

	for info in thirdResults + secondResults + firstResults:
		display = info[1];
		length = len(display);

		# Create expend display if possible
		
		if (info[2] != None):
			# Different display by class
			if (info[0] == METHOD_BOOL):
				extend = " (T)" if (info[2]) else " (F)";
			elif (info[0] == METHOD_ERROR):
				extend = " (" + info[2].__class__.__name__ + ")";
			else:
				extend = " (" + repr(info[2]) + ")";
			
			# use expand display if indexLength enough
			extendLength = CountStringShowLength(extend);
			if (length + extendLength < indexLength):
				display += extend;
				length += extendLength;
		
		# Print and count

		print("%s%s%s%s" % (
			METHODCOLOURS[info[0]] if (colors) else "",
			display,
			"\x1b[0m" if (colors and details) else "",
			" " * max(1, indexLength - length)
		), end="");

		index += 1;
		count += 1;

		# Next line if row full
		if (index >= rowLength):
			print();
			index = 0;
	if (index > 0):
		print();
	
	### Print number of method ###
	print("\nCount: " + str(count));


def IsObjectMultiValue(obj: any) -> bool:
	return type(obj) in [list, tuple, set];

def IsObjectCalculatable(obj: any) -> bool:
	return type(obj) in [int, float, bool];



##### Useful Methods #####

def UnpackValues(values: any) -> list:
	"Unpack multi array to 1d array (example: [[1, 2], [3, [4]]] -> [1, 2, 3, 4])"

	unpacked = [];

	for value in values:
		if (IsObjectMultiValue(value)):
			unpacked += UnpackValues(value);
			continue;

		unpacked.append(value);

	return unpacked;


def UnpackCalculatableValues(values: any, errorFuncName: str = False) -> list:
	"""Unpack multi array to 1d array by only calculateable number
	example: [[1, "hello world"], [print, [os]]] -> [1]
	
	values : array to unpack
	errorFuncName : Title to print error message (default: False)"""

	unpacked = [];

	for value in values:
		if (IsObjectMultiValue(value)):
			unpacked += UnpackCalculatableValues(value);
			continue;

		if (IsObjectCalculatable(value)):
			unpacked.append(value);
			continue;

		if (errorFuncName):
			print("ERROR: %s: %s not a calculatable value." % [errorFuncName, type(value).__name__]);

	return unpacked;


##### 統計学 #####

def Quartiles(*values) -> tuple[tuple[any, any], tuple[any, any], tuple[any, any]]:
	unpacked = UnpackValues(values);
	unpacked.sort();
	
	N = len(unpacked) + 1;
	
	index = N/4;
	first1 = unpacked[round(index) - 1];
	first2 = unpacked[round(index) - (index%1 != 0.5)];
	
	index = N/2;
	second1 = unpacked[round(index) - 1];
	second2 = unpacked[round(index) - (index%1 != 0.5)];
	
	index = N * 3/4;
	third1 = unpacked[round(index) - 1];
	third2 = unpacked[round(index) - (index%1 != 0.5)];
	
	def Combine(a, b):
		return ((a + b) / 2) if (IsObjectCalculatable(a) and IsObjectCalculatable(b)) else (a, b);
	
	return (Combine(first1, first2), Combine(second1, second2), Combine(third1, third2));





def Mean(*values) -> float:
	unpacked = UnpackCalculatableValues(values);
	return sum(unpacked) / len(unpacked);



def Mode(*values) -> tuple[any, int]:
	"return the most often value and often times at values"

	unpacked = UnpackValues(values);
	record = {};
	
	for value in unpacked:
		try:
			if (record.get(value)):
				record[value] += 1;
			else:
				record[value] = 1;
		except:
			pass
	
	mostOftenValue: any = None;
	mostOftenTimes: int = 0;
	
	for value, times in record.items():
		if (times > mostOftenTimes):
			mostOftenValue = value;
			mostOftenTimes = times;
	
	return (mostOftenValue, mostOftenTimes);


def Median(*values) -> tuple[any, any]:
	return Quartiles(values)[1];


def Midrange(*values) -> float:
	unpacked = UnpackCalculatableValues(values);
	return (max(unpacked) + min(unpacked)) / 2;



def FirstQuartile(*values) -> tuple[any, any]:
	return Quartiles(values)[0];

def SecondQuartile(*values) -> tuple[any, any]:
	return Quartiles(values)[1];

def ThirdQuartile(*values) -> tuple[any, any]:
	return Quartiles(values)[2];



def Midhinge(*values) -> tuple[any, any]:
	quartiles = Quartiles(values);
	return (quartiles[0] + quartiles[2]) / 2;



def MAD(*values) -> float:
	unpacked = UnpackCalculatableValues(values);
	mean = Mean(unpacked);
	
	return sum([abs(val - mean) for val in unpacked]) / len(unpacked);

def Variance(*values) -> float:
	unpacked = UnpackCalculatableValues(values);
	mean = Mean(unpacked);
	
	return sum([(val - mean)**2 for val in unpacked]) / len(unpacked);

def StandardDeviation(*values) -> float:
	return Variance(values) ** 0.5;

def VariationCoefficient(*values) -> float:
	return (StandardDeviation(values) / Mean(values)) * 100;

def SkewnessCoefficient(*values) -> float:
	return 3 * (Mean(values) - Median(values)) / StandardDeviation(values);





##### Time Display #####

def DisplayTime():
	while (true):
		print("\r" + time.ctime(), end = "");
	
		now = time.time();
		time.sleep(int(now) + 1 - now);



##### ライキン Method #####

def ROK_SplitSoldier(soldiers: list[int], capacities: list[int], preference: str = None):
	## コピーを作成 ##
	lessSoldiers = soldiers.copy();

	## パラメーター修正 ##
	if (type(preference) == str):
		preference = ord(preference);

		if (preference >= ord('A') or preference <= ord('Z')):
			preference -= ord('A');
		elif (preference == ord('a') or preference <= ord('z')):
			preference -= ord('a');
		else:
			print("ERROR: %s: Invalid preference '%s'!" % ("ROK_SplitSoldier", preference));
			return;
	
	if (preference and (preference < 0 or preference >= len(soldiers))):
		print("ERROR: %s: Preference soldier %s not exists!" % ("ROK_SplitSoldier", chr(preference + ord('A'))));
		return;

	## 統計 ##
	totalSoldier = sum(soldiers);
	totalCapacitie = sum(capacities);

	armyCount = len(capacities);

	## 推薦兵種の計算 ##
	preferenceCount: int = 0;

	if (preference):
		preferenceCount = min(soldiers[preference], totalCapacitie) / armyCount;

	## 兵数の数表示する ##
	print("Total soldiers: %d" % totalSoldier);
	print();

	## 各部隊の各兵数を計算し、表示する ##
	for armyNumber in range(armyCount):
		# 各部隊の計算で変動しているため、毎回計算する
		lessTotalSoldiers = sum(lessSoldiers);

		# 部隊の分配を計算する
		useSoldiers: list[int] = [];
		requestSoldier: int = capacities[armyNumber] - preferenceCount;
		
		for soldierType in range(len(lessSoldiers)):
			if (soldierType == preference):
				useSoldier: int = preferenceCount;
			else:
				useSoldier: int = requestSoldier * lessSoldiers[soldierType] / lessTotalSoldiers;
			
			useSoldier = min(useSoldier, lessSoldiers[soldierType]);
			
			useSoldiers.append(useSoldier);
			lessSoldiers[soldierType] -= useSoldier;
		
		# 部隊の分配を表示
		useSoldierCount: int = sum(useSoldiers);
		print("Army %d: Capacity %d  Actually %d (%.2f%%)" % (
			armyNumber + 1,
			capacities[armyNumber],
			useSoldierCount, useSoldierCount / totalSoldier * 100,
		));

		for soldierType in range(len(lessSoldiers)):
			print("\tSoldier %s: %d" % (chr(ord('A') + soldierType), useSoldiers[soldierType]));
		print();

	## 余った兵を表示する ##
	lessTotalSoldiers = sum(lessSoldiers);

	print("Less soldiers: %d (%.2f%%)" % (lessTotalSoldiers, lessTotalSoldiers / totalSoldier * 100));

	for soldierType in range(len(lessSoldiers)):
		print("\tSoldier %s: %d" % (chr(ord('A') + soldierType), lessSoldiers[soldierType]));
	
	print();



##### libYoutube #####

def ConvertToMP3(file: str, output: str) -> bool:
	libAudioSegment = __LoadPydub();
	
	try:
		audio = libAudioSegment.from_file(file);
		audio.export(output, format = "mp3");
	except:
		print();
		return False;

	return True;


def DownloadYoutubeMP3(url: str):
	# Load library
	libYoutube = __LoadlibYoutube();
	
	# Load libYoutube
	yt = libYoutube(url);
	
	# get streams
	streams = yt.streams.filter(abr = "160kbps");
	
	if (len(streams) < 1):
		print("ERROR: No suitable stream!");
		return;
	
	# Download
	filename = streams[0].download();
	
	# Convert file to MP3
	filename_splited = filename.rsplit(os.extsep, 1);
	output = filename_splited[0] + os.extsep + "mp3";
	
	if (filename_splited[1].lower() != "mp3"):
		ret = ConvertToMP3(filename, output);
		
		if (ret == False):
			print("MP3 Convert failed! file save to %s" % (output));
			return;
	
	os.remove(filename);
	print("MP3 save to %s" % (output));