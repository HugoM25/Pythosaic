from PIL import Image

def GiveImageOfOneElement(x, y, im, dimensions) :
    width , height = im.size
    emoji_img = im.crop((x * dimensions[0], y * dimensions[1], x * dimensions[0] + dimensions[0],y * dimensions[1] + dimensions[1]))
    return emoji_img

def CalcColor(img) :
    r, g, b = 0,0,0
    newimg = img.resize((1,1), Image.ANTIALIAS)
    colorpixel = newimg.getpixel((0,0))
    r = colorpixel[0]
    g = colorpixel[1]
    b = colorpixel[2]
    return (r, g, b)



if __name__ == '__main__' :
    datasetname = input("Your grid name (with the extension):")
    im = Image.open(datasetname)
    dim = input("give the number of images per row and column in the form : 1 1")
    dim = dim.split()
    width , height = im.size
    dimensions = (int(width/ int(dim[0])), int(height/ int(dim[1])))
    ListeEmoji = []
    for j in range(0,24) :
        for i in range(0,30):
            ListMini = []
            ListMini.append((i,j))
            ListMini.append(CalcColor(GiveImageOfOneElement(i,j, im, dimensions)))
            ListeEmoji.append(ListMini)
    with open(datasetname[:-4] + "List.txt", "w") as file :
        for i in range(0,len(ListeEmoji)) :
            data_dispo = ""
            data_dispo = str(ListeEmoji[i][0][1]) + " " + str(ListeEmoji[i][0][0])
            data_dispo += "   " + str(ListeEmoji[i][1][0]) +" "+ str(ListeEmoji[i][1][1]) + " "+  str(ListeEmoji[i][1][2]) + "\n"
            file.write(data_dispo)
        file.write("# " + str(dimensions[0]) + " " + str(dimensions[1]))
