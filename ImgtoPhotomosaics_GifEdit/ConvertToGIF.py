import ConvertToIMG
import CreateDataSet
import os
from PIL import Image
import shutil
from collections import *
import ConvertToIMG

def ExtractingFrames(thegif):
    outfolder = "extractedFrames"
    infolder = "doneFrames"
    try :
        shutil.rmtree(outfolder +"/")
        shutil.rmtree(infolder +"/")
    except :
        pass
    os.makedirs(outfolder + "/")
    os.makedirs(infolder + "/")
    frame = Image.open(thegif)
    nframes = 0
    while frame :
        frame.save("%s/%s-%s.png" % (outfolder, os.path.basename(thegif), nframes), "PNG")
        nframes += 1
        try :
            frame.seek(nframes)
        except EOFError:
            break;
    return True

def Concatenate(nameofGif):
    folderwithIMG = "doneFrames"
    outfolder = "extractedFrames"
    imageList = []
    listoffiles = os.listdir( folderwithIMG+ "/")
    number_files = len(listoffiles)

    for i in range(0, number_files):
        im = Image.open("%s/%s-%s.png" % (folderwithIMG, os.path.basename(nameofGif), i)).convert("RGBA")
        imageList.append(im)
    imageList[0].save("gifFinal.gif", save_all=True, append_images = imageList[1:], duration=100, loop = 10)


if __name__ == "__main__" :

    datasetname = input("The name of your dataset ( with the extension )")
    im = Image.open(datasetname).convert("RGBA")
    nameofGif = input("The name of the gif file :")
    outfolder = "extractedFrames"
    ExtractingFrames(nameofGif)
    listoffiles = os.listdir( outfolder+ "/")
    number_files = len(listoffiles)
    for i in range(0, number_files) :
        image_finale = ConvertToIMG.ConverttheIMG(datasetname, im,Image.open("%s/%s-%s.png" % ("extractedFrames", os.path.basename(nameofGif), i)).convert("RGBA"))
        image_finale.save("%s/%s-%s.png" % ("doneFrames", os.path.basename(nameofGif), i))
    Concatenate(nameofGif)
