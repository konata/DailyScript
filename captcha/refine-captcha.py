# coding:utf-8
from __future__ import print_function
from PIL import Image
import pyocr
import operator

"""
	identify specific image
"""
def identify_image(img):
	tool = pyocr.get_available_tools()[0]
	digits = tool.image_to_string(img,builder=pyocr.tesseract.DigitBuilder())
	return digits


"""
	return pixel dimension arrays
"""
def read_image(image_path):
	image = Image.open(image_path)
	return (image,image.load())


"""
	find black dots
"""
def find_noise(pix,x,y):
	noise = [(h,v) for h in xrange(1,x-1) for v in xrange(1,y-1) if reduce(operator.add,pix[(h,v)],0) < 500] # black noise
	return noise


"""
	set value to the top and bottom color
"""
def blur_noise(pix,x,y):
	top = pix[(x,y+1)]
	bottom = pix[(x,y-1)]
	pix[(x,y)] = tuple([(top[i] + bottom[i]) / 2 for i in (0,1,2)])


"""
	save image
"""
def save_image(img,filename):
	img.save(filename,"JPEG")


def dump(x):
	print(x)


if __name__ == '__main__':
	(image,pix) = read_image('./captchaImage1')
	(x,y) = image.size
	# remove noise 3 times
	count = 2
	identified = False
	while count > 0 and not identified:
		res = identify_image(image)
		dump("Identify as : " + res)
		identified = len(res) == 4 and re.match(ur'^\d{4}$')
		count = count - 1
		black_dots = find_noise(pix,x,y)
		map(lambda x: blur_noise(pix,x[0],x[1]),black_dots)

	if not identified:
		dump("Failed Identify Image ") 







	





