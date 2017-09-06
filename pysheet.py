import sys
import os
import platform
from PIL import Image
import argparse
import time
import math
import re #for sorting file names

from pprint import pprint

print "------------------------\nLets try to make a sprite sheet\n------------------------"

#lets get some arguments

parser = argparse.ArgumentParser()

parser.add_argument("-s","--sequence", help="sequence to load in")
parser.add_argument("-o","--output", help="file name to save as")
parser.add_argument("-b","--begin", help="start frame", type=int)
parser.add_argument("-e","--end", help="end frame", type=int)

args = parser.parse_args()

print "Sequence: "+str(args.sequence)

if args.begin:
	print "Begin: "+str(args.begin)
if args.end:
	print "End: "+str(args.end)


#look in the folder
if(args.sequence==None):
	print "You should apply a directory to find a sequence to sprite sheet up"
	sys.exit()

path = str(args.sequence)
if(not os.path.isdir(path)):
	print "Supplied sequence path is bogus"
	sys.exit()

#get the parent directory for saving the sprite sheet
delimeter = "/"
if platform.system() == "Windows":
	delimeter = "\\"
dirsplit = path.split(delimeter)
dirsplit = dirsplit[:-1]
parentdir = delimeter.join(dirsplit)
print "Parent Directory: "+parentdir

outfile = "sprite_sheet"
if args.output:
	outfile = str(args.output)
savefile = parentdir+delimeter+outfile + ".png"

print "Sequence folder acceptable"
print "Filename: " + savefile

#look at getting the sequence files
#http://stackoverflow.com/a/168435
files = [ x[0] for x in sorted([(path+delimeter+fn, os.stat(path+delimeter+fn)) for fn in os.listdir(path)], key = lambda x: x[1].st_ctime)]
#pprint( files )
#https://stackoverflow.com/a/4836734
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

files = natural_sort(files)

autowidth = int(math.ceil(math.sqrt(len(files))))
fim = Image.open(files[0])
dimensions = fim.size

#figure out how big my new image is going to be
isize = (autowidth*dimensions[0],autowidth*dimensions[1])
# Create the new image. The background doesn't have to be white
white = (255,255,255,255)
black = (0,0,0,0);
print isize
#inew = Image.new('RGBA',isize,black)
#copy the image, basically makes a new image with the same mode, to avoid filthy errors
inew = Image.new(fim.mode,isize,black)
#inew.convert(fim.mode)
#print("----------NEW:"+inew.mode)
#print("----------FIR:"+fim.mode)


count = 0
# Insert each thumb:
for irow in range(autowidth):
    for icol in range(autowidth):
        
        left = irow*(dimensions[0])
        #right = left + dimensions[0]
        upper = icol*(dimensions[1])
        #lower = upper + dimensions[1]
        
        #bbox = (left,upper,right,lower)
        upperleft = (upper,left)
        #print("BBOX--------:"+str(left)+":"+str(right)+":"+str(upper)+":"+str(lower) )
        
        try:
            # Read in an image and resize appropriately
            #img = Image.open(fnames[count]).resize((photow,photoh))
            img = Image.open(files[count])
            #img.convert('RGBA')
            #print("----------CON:"+img.mode)
            print("FILENAME---------:"+files[count])
            print("UPPERLEFT--------:"+str(upper)+":"+str(left))
        except:
            break
        #inew.paste(img,bbox,img)
        inew.paste(img,upperleft)
        count += 1
if (isize[0]>4096):
    print("WE ARE LARGE, RESIZE TO 4096")
    inew = inew.resize((4096,4096),Image.BICUBIC)
inew.save(savefile)
inew.show()

#onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
