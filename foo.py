





import httplib2

URLA = "http://hls-hw.xvideos-cdn.com/videos/hls/26/b9/41/26b941d61b20e29f14adda31d9f2ad2c-1/hls-480p0.ts?e=1522517112&l=0&h=79f663e48fdd609ca4b5f97f03505268"
URLB = "http://hls-hw.xvideos-cdn.com/videos/hls/26/b9/41/26b941d61b20e29f14adda31d9f2ad2c-1/hls-480p1.ts?e=1522517112&l=0&h=79f663e48fdd609ca4b5f97f03505268"

def downloadfile(URL):                 
	h = httplib2.Http("Cache")                 
	resp, content = h.request(URL, "GET")                 
	return content

#create the file for writing
f = open("test.ts", "bw+")
c = downloadfile(URLA)
f.write(c)
c = downloadfile(URLB)
f.write(c)
f.close()



