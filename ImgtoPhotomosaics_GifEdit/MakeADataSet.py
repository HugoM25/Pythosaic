from PIL import Image
import os

def CreateImageSet():
    dimension = 50
    listoffiles = os.listdir("DataToUse/")
    number_files = len(listoffiles)
    print(number_files)
    datadim = GuessTwoInt(number_files)
    image_finale = Image.new("RGB", (dimension*datadim[0], dimension*datadim[1]), color = "black")
    rangexmax = datadim[0]
    rangex = 0
    rangey = 0
    for i in range(0,number_files) :
        try :
            img = Image.open("DataToUse/meme"+str(i) + ".png")
        except :
            img = Image.open("DataToUse/meme" + str(i) + ".jpg")

        img = img.resize((dimension,dimension), Image.ANTIALIAS)

        if rangex >= rangexmax :
            rangey += 1
            rangex = 0
        image_finale.paste(img, (dimension*rangex, dimension * rangey))
        rangex +=1
    image_finale.save("finalset.png")

def GuessTwoInt(number):
    num1 = 0
    num2 = 0
    for i in range(1,10) :
        if number % i == 0 :
            num1 = int(i)
            num2 = int(number/i)
    return num1, num2


if __name__ == "__main__" :
    CreateImageSet()
