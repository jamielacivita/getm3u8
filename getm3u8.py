from sys import argv
from subprocess import call
import httplib2
from bitstring import ConstBitStream

class manifestRequest:
	inputURL = ""
	outputURL = ""
	parentURL = ""
	childURL = ""
	baseURL = ""
	manifestURL = ""
	outFile = ""

	def downloadfile(self, URL):
		h = httplib2.Http("Cache")
		resp, content = h.request(URL, "GET")
		return content

	def getPostion(self, bitStream, searchString, offset):
		found = bitStream.find(searchString, start=offset, bytealigned=True)
		return bitStream.pos + 8

	def getString(self, bitStream, start, end):
		bitStream.pos = start
		readLength = (end - start) - 8
		hexSlice = bitStream.read(readLength).hex
		out = bytearray.fromhex(hexSlice).decode()
		return out

	def getinputURL(self):
		return self.inputURL


	def setParentManifestURL(self):
		#download the master file
		bs = ConstBitStream(self.downloadfile(self.inputURL))
		#isolate the parent manifest
		#search for html5player.setVideoHLS
		playerPos = self.getPostion(bs, b'html5player.setVideoHLS', 0)

		#fromPlayerPos navigate to the first tic.
		startTic = self.getPostion(bs, '0x27', playerPos)
		
		#fromFirstTic find second tic.
		endTic = self.getPostion(bs, '0x27', startTic)

		#isolate relative string store and return.
		self.parentURL = self.getString(bs, startTic, endTic)
		#return self.parentURL
		return 0

	def setChildManifestURL(self):
		#download the child file
		bs = ConstBitStream(self.downloadfile(self.parentURL))
		#isolate the parent manifest
		#search for NAME key
		namePos = self.getPostion(bs, b'NAME', 0)
		#fromName navigate to the first newline.
		startNew = self.getPostion(bs, b'\n', namePos)
		#fromFirstTic find second tic.
		endNew = self.getPostion(bs, b'\n', startNew)
		#isolate relative string store and return.
		self.childURL = self.getString(bs, startNew, endNew)
		#return self.childURL
		return 0


	def setManifestURL(self):
		self.baseURL = self.parentURL.rsplit('/',1)[0]
		self.manifestURL = self.baseURL + "/" + self.childURL
		#return self.manifestURL
		return 0

	def getManifestURL(self):
		return self.manifestURL

	def __init__(self, outFile, URL):
		self.outFile = outFile
		self.inputURL = URL
		self.setParentManifestURL()
		self.setChildManifestURL()
		self.setManifestURL()
		self.setManifestURL()
 
	def getBaseURL(self):
		return self.baseURL

	def getOutFile(self):
		return self.outFile

class parseManifest():

	manifestURL = ""
	fileList = []

	#download the manifest into a bitstream
	def downloadfile(self, URL):
		h = httplib2.Http("Cache")
		resp, content = h.request(URL, "GET")
		return content

	def getPostion(self, bitStream, searchString, offset):
		found = bitStream.find(searchString, start=offset, bytealigned=True)
		return bitStream.pos + 8

	def getString(self, bitStream, start, end):
		bitStream.pos = start
		readLength = (end - start) - 8
		hexSlice = bitStream.read(readLength).hex
		out = bytearray.fromhex(hexSlice).decode()
		return out

	def isHash(self, bs, position):
		bs.pos = position
		char = bs.read(8)
		return (char.hex == '23')

	def nextNewLine(self, bs, position):
		bs.pos = position
		found = bs.find(b'\n', start=position)
		return bs.pos

	def __init__(self, URL):
		self.manifestURL = URL
		bs = ConstBitStream(self.downloadfile(self.manifestURL))
		#print(bs)

		#read first character
		#is it a hash?
		if (self.isHash(bs,0)):
			#print("is hash")
			#print("next new line is at")
			#print(self.nextNewLine(bs,0))
			#print("dist: %i" % self.distFromEnd(bs))
			#print(self.getLine(bs,0))
			#print(self.getLine(bs,64))
			self.getLines(bs,0,"files")
		else:
			print("not hash")

	def distFromEnd(self, bs):
		length = bs.len
		return length - bs.pos

	def getLine(self, bs, position):
		bs.pos = position
		line = bs.readto(b'\n', bytealigned=True)
		return (line, bs.pos)
		
	def getLines(self, bs, position, mode):
		while (position < bs.len):
			line = self.getLine(bs,position)

			if ((mode=="files") and (self.isHash(line[0],0))):
				pass
			else:
				#print(line) <---<<< returns a tuple (useful for debugging)
				#print(line[0]) <---<<< returns a hex string
				hexSlice = line[0].hex 
				#print(str(bytearray.fromhex(hexSlice).decode()))
				fileName = bytearray.fromhex(hexSlice).decode().strip()
				#print(fileName)
				self.fileList.append(fileName)
	

			position = line[1]
		return self.fileList

	def getFileList(self):
		return self.fileList

class CreateTSfile():

	baseURL = ""
	fileList = []
	URLList = []
	
	def downloadfile(self, URL):                 
		h = httplib2.Http("Cache")                 
		resp, content = h.request(URL, "GET")                 
		return content

	def getFileList(self):
		return self.fileList

	def setFileList(self, fileList):
		self.fileList = fileList

	def getBaseURL(self):
		return self.baseURL

	def setBaseURL(self, baseURL):
		self.baseURL = baseURL

	def setURLList(self):
		for n in self.fileList:
			self.URLList.append(self.baseURL + "/" + n)

	def getURLList(self):
		return self.URLList


	def createFile(self, outFile="test.ts"):
		f = open(outFile, "bw+")
		for fileURL in self.URLList:
			c = self.downloadfile(fileURL)
			f.write(c)
		f.close()



		


man = manifestRequest(argv[1], argv[2])
pm = parseManifest(man.getManifestURL())
ct = CreateTSfile()
bu = man.getBaseURL()


ct.setBaseURL(man.getBaseURL())
ct.setFileList(pm.getFileList())
ct.setURLList()
#print(ct.getURLList())
#for n in ct.getURLList():
#	print(n)
ct.createFile(man.getOutFile())





















