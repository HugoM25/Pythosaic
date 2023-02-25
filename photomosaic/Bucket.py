class Bucket:
    def __init__(self, elements=[]):
        self.elements = elements
        self.average_color = self.calculate_average_color()

    def calculate_average_color(self):

        if len(self.elements) == 0:
            return (0, 0, 0)

        average_color = [0, 0, 0]
        for element in self.elements:
            average_color[0] += element.color[0]
            average_color[1] += element.color[1]
            average_color[2] += element.color[2]

        average_color[0] /= len(self.elements)
        average_color[1] /= len(self.elements)
        average_color[2] /= len(self.elements)

        return average_color

    def add_element(self, element):
        self.elements.append(element)
        # Need to update average color
        self.average_color = self.calculate_average_color()
