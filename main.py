import os
from os import listdir
from PIL import Image as PImage
from tkinter import *


def from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def loadImage(path):
    imagesList = listdir(path)
    print(imagesList)

    imgname = ''

    for im in imagesList:
        if im.endswith('.png'):
            imgname = im
            break
        else:
            continue

    img = PImage.open(path + imgname)
    return img


class App:

    def __init__(self, master):
        self.simultanious_rows = 1

        frame = Frame(master)
        frame.pack()

        self.width = 1200
        self.height = 1200

        self.canvas = Canvas(frame, width=self.width, height=self.height)

        self.row_string = StringVar()

        self.row_label = Label(frame, textvariable=self.row_string)
        self.row_label.pack()

        self.canvas.pack()
        # self.canvas.create_rectangle(0, 0, 1920, 1080, fill="cornflowerblue")

        self.img = loadImage(os.getcwd() + '/')

        # rgb_img = img.convert('RGB')

        self.current_row = 0
        self.pixels = []
        self.consec_pixel_texts = []
        self.pixel_size = self.width / self.img.width

        self.display_row(0)

            # for y in range(img.height):
            #     r, g, b = img.getpixel((x, y))
            #     print(r, g, b)

        self.prev_button = Button(frame, text="Previous Row", fg="black", command=self.prev_row)
        self.prev_button.pack()
        self.next_button = Button(frame, text="Next Row", fg="black", command=self.next_row)
        self.next_button.pack()

        self.rows_slider = Scale(frame, from_=0, to=self.img.width, orient=HORIZONTAL)
        self.rows_slider.pack()

        master.bind('<Down>', self.next_row)
        master.bind('<Up>', self.prev_row)

    def next_row(self, _event=None):
        print('advancing row')
        if 0 <= self.current_row < self.img.height - 1:
            self.current_row += 1
        self.display_row(self.current_row)

    def prev_row(self, _event=None):
        if 0 < self.current_row <= self.img.height:
            self.current_row -= 1
        self.display_row(self.current_row)
        print('moving back one row')

    def display_row(self, row):

        self.row_string.set('current row: ' + str(row))
        #self.simultanious_rows = self.rows_slider.get()

        self.simultanious_rows = 2

        #if len(self.pixels) > self.img.width: # Remove one row
        for p in self.pixels:
            self.canvas.delete(p)
        self.pixels.clear()
        consec = 1
        prev_rgb = [0, 0]

        for t in self.consec_pixel_texts:
            self.canvas.delete(t)

        self.consec_pixel_texts.clear()

        for r in range(self.simultanious_rows):
            for x in range(self.img.width):
                rgb = self.img.getpixel((x, row + r))
                prev_row_rgb = (rgb[0] / 2, rgb[1] / 2, rgb[2] / 2)
                draw_color = rgb

                if r != 0:
                    draw_color = prev_row_rgb

                self.pixels.append(self.canvas.create_rectangle((x - 1) * self.pixel_size, (row + r) *
                                                                self.pixel_size, x * self.pixel_size, ((row + r) + 1)
                                                                * self.pixel_size, fill=from_rgb(draw_color)))

                if rgb == prev_rgb:
                    consec += 1
                elif r == 0 and x > 0:
                    self.consec_pixel_texts.append(self.canvas.create_text((x - 1 - consec / 2) * self.pixel_size,
                                                                           ((row + r) - 1) * self.pixel_size +
                                                                           (row + r) * (x < 2), text=str(consec),
                                                                           justify=CENTER))
                    consec = 1

                prev_rgb = rgb

            if r == 0:
                if (row + r) < 2:
                    self.consec_pixel_texts.append(self.canvas.create_text((self.img.width - 1 - consec / 2) * self.pixel_size,
                                                                           ((row + r) + 1) * 2 * self.pixel_size,
                                                                           text=str(consec), justify=CENTER))
                else:
                    self.consec_pixel_texts.append(self.canvas.create_text((self.img.width - 1 - consec / 2) * self.pixel_size,
                                                                           ((row + r) - 1) * self.pixel_size,
                                                                           text=str(consec), justify=CENTER))


root = Tk()
root.iconphoto(False, PhotoImage(file=os.getcwd() + '/communism.png'))
root.wm_title("MapMaker - By Cobeaquen")
app = App(root)
root.mainloop()
