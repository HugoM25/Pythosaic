class Element:
    def __init__(self, image, color, size):
        self.image = image
        self.color = color
        self.size = size

    def __str__(self):
        return "Element: " + str(self.color) + " " + str(self.size)

    def __repr__(self):
        return str(self)
