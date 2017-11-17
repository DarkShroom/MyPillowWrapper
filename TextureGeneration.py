'''
Image drawing example




to get a numpy array from an image use:

from PIL import Image
from numpy import array
img = Image.open("input.png")
arr = array(img)

And to get an image from a numpy array, use:

img = Image.fromarray(arr)
img.save("output.png")



'''
from __future__ import absolute_import, division, print_function
from PIL import Image, ImageDraw  # note this is pillow
import random
# from random import randint
import random
from distutils.dir_util import mkpath
from glob import glob
import os

import PIL

# import Orde

from collections import OrderedDict


def PreviewImage(PIL_image_class, scale=8):
    temp = PIL_image_class.copy()
    width, height = temp.size
    temp = temp.resize((width * scale, height * scale))
    temp.show()


def GenNoiseImage(filename):

    im = Image.new('RGB', (8, 8))  # new image

    draw = ImageDraw.Draw(im)  # a draw tool
    draw.line((0, 0) + im.size, fill=128)
    draw.line((0, im.size[1], im.size[0], 0), fill=128)
    del draw

    width, height = im.size

    for x in range(width):
        for y in range(height):
            cpixel = im.load()[x, y]
            print(cpixel)
            ranint_val = randint(0, 255)

            # cpixel = (randint(0,255),randint(0,255),randint(0,255))
            cpixel = (ranint_val, ranint_val, ranint_val)
            # cpixel = (300,1,1)
            im.putpixel((x, y), cpixel)

    # write to stdout
    im.save(filename)


# for n in range(16):
#     GenImage('NoiseGen{}.png'.format(n))


shades = [0, int(255 * 0.33), int(255 * 0.66), 255]


# for n in range(16):
#     GenImage('NoiseGen{}.png'.format(n))


def LoadImageTest():
    '''
    numpy manipulation 
    '''
    # https://stackoverflow.com/questions/14452824/how-can-i-save-an-image-with-pil

    import sys
    import numpy
    from PIL import Image

    img = Image.open('heart03.png').convert('L')

    im = numpy.array(img)
    fft_mag = numpy.abs(numpy.fft.fftshift(numpy.fft.fft2(im)))

    visual = numpy.log(fft_mag)
    visual = (visual - visual.min()) / (visual.max() - visual.min())

    result = Image.fromarray((visual * 255).astype(numpy.uint8))
    result.save('out.png')

# LoadImageTest()


def LoadImagePixelsTest(filename):

    # print('loading file: {}'.format(filename))
    i = Image.open(filename)
    pixels = i.load()

    color_count = {}

    width, height = i.size
    for y in range(height):
        for x in range(width):
            cur_pixel = pixels[x, y]

            if cur_pixel not in color_count:  # count pixels of colors
                color_count[cur_pixel] = 1
            else:
                color_count[cur_pixel] += 1

            colorize = (1, 0, 0, 1)  # colorize red
            # colorize = (2, 0, 0, 1) #colorize red

            cur_pixel = (
                cur_pixel[0] * colorize[0],
                cur_pixel[1] * colorize[1],
                cur_pixel[2] * colorize[2],
                cur_pixel[3] * colorize[3])

            pixels[x, y] = cur_pixel

    print ('color_count:', color_count)

    output_directory = 'generated'

    mkpath(output_directory)

    output_filename = '{}/{}.gen.png'.format(output_directory, filename)

    i.save(output_filename)

    PreviewImage(i)

    # # def

    # # resize image for preview
    # display_scale = 16
    # i = i.resize((width * display_scale, height * display_scale))
    # # i = i.resize ((width * display_scale, height * display_scale), Image.ANTIALIAS)
    # i.show()


# LoadImagePixelsTest('heart03.png')


def GetImageFormat(filename):
    try:
        img = Image.open(filename)
        return img.format
    except Exception as e:
        pass


def ListImageFormats():
    for filename in glob('*'):
        print (filename, GetImageFormat(filename))


class MyPILWrapper:
    '''
    my wrapper of custom functions
    '''

    def __init__(self, filename=None):
        if filename is not None:
            self.open(filename)

    def open(self, filename):
        # print('loading file: {}'.format(filename))
        self.img = Image.open(filename)

    def save(self, filename):
        # print('saving file: {}'.format(filename))

        print ('savive to ', filename)
        mkpath(os.path.dirname(filename))
        self.img.save(filename)

    def iterate_pixels(self):
        pixels = self.img.load()
        width, height = self.img.size
        self.color_count = {}  # save a color count
        for y in range(height):
            for x in range(width):
                cur_pixel = pixels[x, y]

                if cur_pixel not in self.color_count:  # count pixels of colors
                    self.color_count[cur_pixel] = 1
                else:
                    self.color_count[cur_pixel] += 1

        print('color_count', self.color_count)

    def color_count(self):
        pixels = self.img.load()
        width, height = self.img.size
        color_count = {}  # save a color count
        for y in range(height):
            for x in range(width):
                cur_pixel = pixels[x, y]

                if cur_pixel not in color_count:  # count pixels of colors
                    color_count[cur_pixel] = 1
                else:
                    color_count[cur_pixel] += 1
        return color_count

    def process_pixels(self, process_function):
        pixels = self.img.load()
        width, height = self.img.size
        for y in range(height):
            for x in range(width):
                pixels[x, y] = process_function(pixels[x, y])

    def colorize_pixel_funct(self, pixel, colorize_coefficient=(1, 0, 0, 1)):
        new_pixel = (
            pixel[0] * colorize_coefficient[0],
            pixel[1] * colorize_coefficient[1],
            pixel[2] * colorize_coefficient[2],
            pixel[3] * colorize_coefficient[3],
        )
        return new_pixel

        pass

    def colorize(self, colorize_coefficient=(1, 0, 0, 1)):
        '''
        multiplys the colors (1,0,0,1) would make white go red by dropping the green and blue
        '''
        pixels = self.img.load()
        width, height = self.img.size
        for y in range(height):
            for x in range(width):
                # pixels[x, y] = process_function(pixels[x,y])
                pixels[x, y] = self.colorize_pixel_funct(pixels[x, y], colorize_coefficient)

    def color_replace(self, old_color, new_color):
        '''
        replace all occurences of old color with new one

        color_replace((0,0,0,255),(0,0,0,0)) #all black to transparent

        '''
        pixels = self.img.load()
        width, height = self.img.size
        count = 0
        for y in range(height):
            for x in range(width):
                if pixels[x, y] == old_color:
                    pixels[x, y] = new_color
                    count += 1
        # print('{} pixels replaced'.format(count))

    def to_1bit(self):
        pixels = self.img.load()
        width, height = self.img.size
        count = 0
        for y in range(height):
            for x in range(width):
                if pixels[x, y] != (0, 0, 0, 255):
                    pixels[x, y] = (255, 255, 255, 255)
                    count += 1

    def scramble(self):

        pixels = self.img.load()
        width, height = self.img.size
        i = 0

        pixel_list = []

        for y in range(height):
            for x in range(width):
                # if pixels[x,y] == old_color:
                # pixels[x,y] = new_color
                i += 1
                pixel_list.append(pixels[x, y])  # serialize pixels

        random.shuffle(pixel_list)  # sheffle pixels

        i = 0
        for y in range(height):
            for x in range(width):
                pixels[x, y] = pixel_list[i]  # deserialize pixels
                i += 1


    def offset(self,x,y):
        self.img = PIL.ImageChops.offset(self.img,x,y)

    def show(self, scale=8):
        '''
        show image, but scale it (no blurring)
        '''
        temp = self.img.copy()
        width, height = temp.size
        temp = temp.resize((width * scale, height * scale))
        temp.show()


subdir = 'generated'
mkpath(subdir)


def SaveHeart03():

    filename = 'heart03.png'
    myPIL = MyPILWrapper()
    myPIL.open(filename)
    # myPIL.iterate_pixels()
    # myPIL.colorize()
    myPIL.color_replace((0, 0, 0, 255), (0, 0, 0, 0))
    myPIL.save('{}/{}.gen.png'.format(subdir, filename))
    myPIL.save(filename + '.processed.png')

    myPIL.show()


def ScramTest():

    filename = 'scramble01.png'
    myPIL = MyPILWrapper()
    myPIL.open(filename)

    # myPIL.scramble()
    # myPIL.iterate_pixels()
    # myPIL.colorize()
    # myPIL.color_replace((0,0,0,255),(0,0,0,0))
    # myPIL.save('{}/{}.gen.png'.format(subdir, filename))

    # myPIL.show()

    filename = 'scramble'

    for n in range(16):
        myPIL.scramble()
        filename_split = filename.split('.', 1)

        myPIL.save('{}/{}.gen{}.png'.format(subdir, filename_split[0], n))
        myPIL.save('{}/{}.gen{}.png'.format(subdir, filename_split[0], n))


# ScramTest()


def DecolorTest(filename='enemy01_color_frame01.png'):

    myPIL = MyPILWrapper()
    myPIL.open(filename)

    myPIL.to_bw()

    myPIL.show()

    # filename = 'scramble'

    # for n in range(16):
    #     myPIL.scramble()
    #     filename_split = filename.split('.',1)
    #


# for filename in glob('enemy01*'):
#     print (filename)
#     DecolorTest(filename)


class Color():
    '''
    test colour class
    '''
    red = 1.0
    green = 1.0
    blue = 1.0
    alpha = 1.0

    def set_from_color(self, color):
        self.red = color.red
        self.green = color.green
        self.blue = color.blue
        self.alpha = color.alpha

    def load_from_string(self, s):
        color = color_strings[s]
        self.set_from_color(color)

    def __init__(self, red=1.0, green=1.0, blue=1.0, alpha=1.0):

        sucess = False
        if not sucess:
            if type(red) == str:
                print ('ggg')
                self.load_from_string(red)
                sucess = True

        if not sucess:
            try:
                self.red = float(red)
                self.green = float(green)
                self.blue = float(blue)
                self.alpha = float(alpha)
                sucess = True
            except Exception as e:
                # print(type(e), e)
                pass

        if not sucess:
            try:  # try to convert iterate vals to floats
                self.red = float(red[0])
                self.green = float(red[1])
                self.blue = float(red[2])
                self.alpha = float(red[3])
                sucess = True
            except Exception as e:
                # print(type(e), e)
                pass

        if not sucess:
            # print('WARNING INVALID INPUT')
            pass

    def __add__(self, other):
        result = list(self)
        # other

    def __getitem__(self, index):
        if index == 0:
            return self.red
        elif index == 1:
            return self.green
        elif index == 2:
            return self.blue
        elif index == 3:
            return self.alpha

    # def __set__(self, val):
    #     pass

    def __iter__(self):
        for value in [self.red, self.green, self.blue, self.alpha]:  # this varied from sqlitedict
            yield value

    def pillow_color(self):
        return (
            int(self.red * 255),
            int(self.green * 255),
            int(self.blue * 255),
            int(self.alpha * 255)
        )

    def __repr__(self):
        s = ''
        s += 'Color('
        for val in self:
            s += str(val) + ','
        s = s[:-1]
        s += ')'
        return s


color_strings = OrderedDict()
color_strings['black'] = Color(1, 1, 1)
color_strings['white'] = Color(0, 0, 0)
color_strings['red'] = Color(1, 0, 0)
color_strings['green'] = Color(0, 1, 0)
color_strings['blue'] = Color(0, 0, 1)
color_strings['yellow'] = Color(1, 1, 0)
color_strings['cyan'] = Color(0, 1, 1)
color_strings['magenta'] = Color(1, 0, 1)
color_strings['grey50'] = Color(0.50, 0.50, 0.50)
color_strings['grey33'] = Color(0.33, 0.33, 0.33)
color_strings['grey66'] = Color(0.66, 0.66, 0.66)



def TestBatchColorize(filename='*.png'):

    subdir = 'colorize'
    mkpath(subdir)

    colors = {
        'red': (255, 0, 0, 255),
        'green': (0, 255, 0, 255),
        'blue': (0, 0, 255, 255),
        'yellow': (255, 255, 0, 255),
        'cyan': (0, 255, 255, 255),
        'magenta': (255, 0, 255, 255),

        'shade1': (255, 0, 255, 255),
    }

    glob_results = glob(filename)

    for filename in glob_results:
        # print(filename)
        myPIL = MyPILWrapper(filename)
        myPIL.colorize((1, 0, 0, 1))
        # myPIL.save('{}/{}.gen.png'.format(subdir, filename.split('.', 1)[0]))
        # myPIL.save('{}/{}'.format(subdir, filename))

        for color in colors:
            color_val = colors[color]
            color_val = (
                int(color_val[0] / 255),
                int(color_val[1] / 255),
                int(color_val[2] / 255),
                int(color_val[3] / 255),
            )
            myPIL = MyPILWrapper(filename)
            myPIL.colorize(color_val)
            # save_filename = '{}/{}_{}.gen.png'.format(subdir, filename.split('.', 1)[0], color)
            save_filename = '{}/{}/{}.gen.png'.format(subdir,color, filename.split('.', 1)[0])
            # mkpath(save_filename)
            # mkpath(save_filename)
            myPIL.save(save_filename)


TestBatchColorize()



def ColCountPalleteTests():

    myPIL = MyPILWrapper('bricks1.png')
    print(myPIL.color_count())


black = (0, 0, 0, 255)
transparent = (0, 0, 0, 0)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 255, 255)
yellow = (255, 255, 0, 255)
cyan = (0, 255, 255, 255)
magenta = (255, 0, 255, 255)


def convert_folder_black_to_trans(glob_pat = '*.png'):
    subdir = 'black_to_trans'
    mkpath(subdir)
    for filename in glob(glob_pat):
        # print('loading file {}'.format(filename))
        myPIL = MyPILWrapper(filename)
        myPIL.color_replace(black, transparent)
        save_filename = subdir + '/' + filename
        print('saving file "{}"...'.format(save_filename))
        myPIL.save(save_filename)

        # import PIL
        # myPIL.img = PIL.ImageChops.offset(myPIL.img,1,1)

        # # myPIL.img.offset(5,5)

        # myPIL.show()
        # break

# convert_folder_black_to_trans()


# def convert_folder_black_to_trans(glob_pat = '*.png'):
#     subdir = 'black_to_trans'
#     mkpath(subdir)
#     for filename in glob(glob_pat):
#         # print('loading file {}'.format(filename))
#         myPIL = MyPILWrapper(filename)
#         myPIL.color_replace(black, transparent)
#         save_filename = subdir + '/' + filename
#         print('saving file "{}"...'.format(save_filename))
#         myPIL.save(save_filename)

#         # import PIL
#         # myPIL.img = PIL.ImageChops.offset(myPIL.img,1,1)

#         # # myPIL.img.offset(5,5)

#         # myPIL.show()
#         # break

convert_folder_black_to_trans()


def animate_files( glob_pat = 'waterfall1.png'):
    subdir = 'animate_files'
    mkpath(subdir)
    for filename in glob(glob_pat):
        # print('loading file {}'.format(filename))
        

        filename_split = filename.split('.')
        print(filename_split)

        # save_filename = subdir + '/' + filename_split[0] + '_frame1' +

        for n in range(4):


           save_filename = '{}/{}_frame{}.{}'.format(subdir,filename_split[0],n+1,filename_split[1])
           print(save_filename)

           myPIL = MyPILWrapper(filename)
           myPIL.offset(0,n)
           myPIL.save(save_filename)


          

# animate_files()


def print_color_strings():

    code = ''

    basedir = 'print_color_strings'

    for s in color_strings:
        code += '{} = {}\n'.format(s,color_strings[s].pillow_color())

    code += 'color_list = ['
    for s in color_strings:
        code += '{}, '.format(s)
        pass
    code = code.strip(', ')
    code+=']'


    print (code)
    
print_color_strings()

black = (255, 255, 255, 255)
white = (0, 0, 0, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 255, 255)
yellow = (255, 255, 0, 255)
cyan = (0, 255, 255, 255)
magenta = (255, 0, 255, 255)
grey50 = (127, 127, 127, 255)
grey33 = (84, 84, 84, 255)
grey66 = (168, 168, 168, 255)
color_list = [black, white, red, green, blue, yellow, cyan, magenta, grey50, grey33, grey66]



