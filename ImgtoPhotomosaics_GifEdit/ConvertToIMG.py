from PIL import Image
import CreateDataSet
from math import sqrt


def RescaleImage(img) :
    maxwidth = 70
    wpercent = (maxwidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((maxwidth,hsize), Image.ANTIALIAS)
    return img

def ImagToPixel(img) :
    wi,he = img.size
    listePix = []
    for j in range(0,he) :
        for i in range(0,wi) :
            listePix.append(img.getpixel((i,j)))
    return listePix

def CalcThebestEmoji(Pixlist, listEmoji) :
    ListOfEmoji = []
    sensi = 150
    for rgb in Pixlist :
        try :
            if rgb[3] <= sensi :
                rgb = (255,255,255, 255)
        except :
            pass

        mindiff = 1000
        MinList = []
        x = 0
        y = 0
        for i in range(len(listEmoji)) :
            diff = 0
            diff += abs(int(rgb[0]) - int(listEmoji[i][2]))
            diff += abs(int(rgb[1]) - int(listEmoji[i][3]))
            diff += abs(int(rgb[2]) - int(listEmoji[i][4]))

            if diff < mindiff :
                x = int(listEmoji[i][0])
                y = int(listEmoji[i][1])
                mindiff = diff
        MinList.append(x)
        MinList.append(y)
        ListOfEmoji.append(MinList)
    return ListOfEmoji

def CalcThebestEmoji2(Pixlist, listEmoji):
    ListOfEmoji = []
    sensi = 150
    for rgb in Pixlist :
        try :
            if rgb[3] <= sensi :
                rgb = (255,255,255, 255)
        except :
            pass

        mindistance = 1000
        MinList = []
        x = 0
        y = 0
        for i in range(len(listEmoji)) :
            dist = 0
            dist = sqrt((rgb[0] - int(listEmoji[i][2]))**2 + (rgb[1] -int(listEmoji[i][3]))**2  + (rgb[2] -int( listEmoji[i][4]))**2)

            if dist < mindistance :
                x = int(listEmoji[i][0])
                y = int(listEmoji[i][1])
                mindistance = dist
        MinList.append(x)
        MinList.append(y)
        ListOfEmoji.append(MinList)
    return ListOfEmoji


def LisListeFromFile(filename) :
    with open(filename, "r") as file :
        lines = file.readlines()
        listEmoji = []
        for line in lines :
            if line[0] != "#" :
                dataline = line.split()
                listEmoji.append(dataline)
            else :
                dataline = line.split()
                dimensions =  (int(dataline[1]), int(dataline[2]))


        return listEmoji , dimensions

def CreateAnImage(listOfEmojis, img, dimensions,im):
    wi,he = RescaleImage(im).size
    image_finale = Image.new("RGB", (wi * round(dimensions[0]), he * round(dimensions[1])), color = "black")
    rangex = 0
    rangey = 0
    for i in range(0,len(listOfEmojis)) :
        if rangex >= wi :
            rangey +=1
            rangex = 0
        image_finale.paste(CreateDataSet.GiveImageOfOneElement(listOfEmojis[i][1], listOfEmojis[i][0], img, dimensions), (rangex * round(dimensions[0]), rangey * round(dimensions[1])), CreateDataSet.GiveImageOfOneElement(listOfEmojis[i][1], listOfEmojis[i][0], img, dimensions))
        rangex += 1
    return image_finale

def ConverttheIMG(datasetname, im, img):
    listeEmoji = LisListeFromFile(datasetname[:-4] + "List.txt")[0]
    dimensions = LisListeFromFile(datasetname[:-4] + "List.txt")[1]
    pixlist = ImagToPixel(RescaleImage(img))
    image_finale = CreateAnImage(CalcThebestEmoji2(pixlist, listeEmoji), im, dimensions, img)
    return image_finale

if __name__ == "__main__" :
    datasetname = input("The name of your dataset ( with the extension )")
    im = Image.open(datasetname).convert("RGBA")
    filetoconvert = input("The file to be converted:")
    img = Image.open(filetoconvert)
    image_finale = ConverttheIMG(datasetname, im, img)
    image_finale.save("finalImg.png")
    image_finale.show()
