from PIL import Image
import CreateDataSet


def RescaleImage(img) :
    maxwidth = 50
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
        for i in range(len(listeEmoji)) :
            diff = 0
            diff += abs(rgb[0] - int(listeEmoji[i][2]))
            diff += abs(rgb[1] - int(listeEmoji[i][3]))
            diff += abs(rgb[2] - int(listeEmoji[i][4]))

            if diff < mindiff :
                x = int(listeEmoji[i][0])
                y = int(listeEmoji[i][1])
                mindiff = diff
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

def CreateAnImage(listOfEmojis, img, dimensions):
    wi,he = RescaleImage(img).size
    image_finale = Image.new("RGB", (wi * round(dimensions[0]), he * round(dimensions[1])), color = "black")
    rangex = 0
    rangey = 0
    for i in range(0,len(listOfEmojis)) :
        if rangex >= wi :
            rangey +=1
            rangex = 0
        image_finale.paste(CreateDataSet.GiveImageOfOneElement(listOfEmojis[i][1], listOfEmojis[i][0], im, dimensions), (rangex * round(dimensions[0]), rangey * round(dimensions[1])), CreateDataSet.GiveImageOfOneElement(listOfEmojis[i][1], listOfEmojis[i][0], im, dimensions))
        rangex += 1
    image_finale.save("finalImg.png")
    image_finale.show()



if __name__ == "__main__" :
    datasetname = input("The name of your dataset ( with the extension )")
    im = Image.open(datasetname).convert("RGBA")
    filetoconvert = input("The file to be converted:")
    img = Image.open(filetoconvert)
    listeEmoji = LisListeFromFile(datasetname[:-4] + "List.txt")[0]
    dimensions = LisListeFromFile(datasetname[:-4] + "List.txt")[1]
    pixlist = ImagToPixel(RescaleImage(img))

    CreateAnImage(CalcThebestEmoji(pixlist, listeEmoji), img, dimensions)
