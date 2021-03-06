from inc_noesis import *

PAL_COUNT_OFFSET = 3
PAL_0_TRANSPARENT = True
OLDER_VERSION = False #necessary for some files (NTROG7.IMG, STUFF.IMG, others)

def registerNoesisTypes():
	handle = noesis.register("NBA Jam Source IMG", ".img")
	noesis.setHandlerTypeCheck(handle, imgCheckType)
	noesis.setHandlerLoadRGBA(handle, imgLoadRGBA)
	#noesis.logPopup()
	return 1

class ImgImage:
	def __init__(self, bs):
		self.name = bs.readBytes(16)
		self.x = bs.readShort()
		self.y = bs.readShort()
		self.u0 = 0 if OLDER_VERSION else bs.readShort()
		self.w = bs.readShort()
		self.h = bs.readShort()
		self.palIndex = (bs.readShort() & 4095) - PAL_COUNT_OFFSET
		self.dataOffset = bs.readInt()
		bs.readBytes(12 if OLDER_VERSION else 18) #unused/unknown
		
class ImgPal:
	def __init__(self, bs):
		self.name = bs.readBytes(12)
		self.colorCount = bs.readUShort()
		self.dataOffset = bs.readInt()
		bs.readBytes(8) #unused/unknown

class ImgFile:
	def __init__(self, bs):
		self.bs = bs
		
	def parseInfo(self):
		bs = self.bs
		try:
			dataSize = len(bs.getBuffer())
			imageCount = bs.readUShort()
			palCount = bs.readUShort() - PAL_COUNT_OFFSET
			dirOffset = bs.readInt()
			u1 = bs.readUShort()
			uCount0 = bs.readUShort()
			uCount1 = bs.readUShort()
			u2 = bs.readUShort()
			u3 = bs.readUShort()
			if imageCount == 0 or palCount == 0 or dirOffset <= 0 or dirOffset >= dataSize:
				return 0
			images = []
			pals = []
			bs.seek(dirOffset, NOESEEK_ABS)
			for imageIndex in range(imageCount):
				image = ImgImage(bs)
				if image.dataOffset < 0 or image.dataOffset >= dataSize:
					return 0
				images.append(image)
			for palIndex in range(palCount):
				pal = ImgPal(bs)
				if pal.dataOffset < 0 or pal.dataOffset >= dataSize:
					return 0
				pals.append(pal)
			self.images = images
			self.pals = pals
		except:
			return 0
		return 1
		
	def loadTextures(self, texList):
		bs = self.bs
		palDatas = []
		for pal in self.pals:
			palBuffer = bytearray(256 * 4)
			bs.seek(pal.dataOffset, NOESEEK_ABS)
			data = bs.readBytes(pal.colorCount * 2)
			palBuffer[:pal.colorCount * 4] = rapi.imageDecodeRaw(data, pal.colorCount, 1, "b5g5r5p1")
			if PAL_0_TRANSPARENT:
				palBuffer[3] = 0
			palDatas.append(palBuffer)
			
		for image in self.images:
			name = noeStrFromBytes(image.name.split(b"\0")[0])
			padW = (image.w + 3) & ~3
			bs.seek(image.dataOffset, NOESEEK_ABS)
			data = bs.readBytes(padW * image.h)
			palData = palDatas[image.palIndex]
			rgba = rapi.imageDecodeRawPal(data, palData, padW, image.h, 8, "r8g8b8a8")
			print(name, "-", image.x, image.y, "/", image.w, image.h, "-", image.u0, image.palIndex, "@", image.dataOffset)			
			texList.append(NoeTexture(name, padW, image.h, rgba, noesis.NOESISTEX_RGBA32))			

def imgCheckType(data):
	img = ImgFile(NoeBitStream(data))
	if not img.parseInfo():
		return 0
	return 1

def imgLoadRGBA(data, texList):
	rapi.parseInstanceOptions("-texnorepfn")
	img = ImgFile(NoeBitStream(data))
	img.parseInfo()
	img.loadTextures(texList)
	return 1
