from sys import argv
from subprocess import call
import httplib2
from bitstring import ConstBitStream

class manifestRequest:
	inputURL = ""
	outputURL = ""

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

man = manifestRequest()
man.inputURL = argv[1]
print(man.getinputURL())




#get the position of the player
bs = ConstBitStream(downloadfile(URL))
#bs = ConstBitStream(filename='test.txt')
ss = b'html5player.setVideoHLS'
os = 0
playerPosition = getPostion(bs, ss, os)

#starting from the player, get the position of the first tic.
ss = '0x27'
os = playerPosition
startTic = getPostion(bs, ss, os)

#starting from the first tic, get position of second tic.
ss = '0x27'
os = startTic+8
endTic = getPostion(bs, ss, os)

htmlString = getString(bs, startTic, endTic)
print(htmlString)


#Get the manifest file
bs = ConstBitStream(downloadfile(htmlString))
print(bs)

#starting from the position 0, find the NAME tag.
ss = b'NAME'
os = 0
namePos = getPostion(bs, ss, os)


#starting from the NAME, find the first newline tag.
ss = b'\n'
os = namePos
newline = getPostion(bs, ss, os)


#starting from the newline, find the next newline tag.
ss = b'\n'
os = newline+8
endline = getPostion(bs, ss, os)


htmlString = getString(bs, newline, endline)
print(htmlString)


#searchString = b'html5player.setVideoHLS'
#found = s.find(searchString, bytealigned=True)
#print("position of html5player.setVideoHLS is: %i" % s.pos)

#print("Current position: %i " % s.pos)

#searchString = '0x27'
#found = s.find(searchString, start = s.pos+1, bytealigned=True)
#print("position of start tic: %i" % s.pos)

#print("Current position: %i " % s.pos)
#startTic = s.pos

#searchString = '0x27'
#found = s.find(searchString, start = s.pos+1, bytealigned=True)
#print("position of end tic: %i" % s.pos)

#print("Current position: %i " % s.pos)
#endTic = s.pos

#readLength = endTic - startTic - 16
#s.pos = startTic + 8
#out = s.read(readLength).hex
#print(out)




