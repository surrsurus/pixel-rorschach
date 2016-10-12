#! /usr/bin/env python3.5

import random, argparse

def format_colors(r, g, b):
    ''' Format color ints into strings with buffer spaces for formatted ppm output '''
    # Since the largest color number possible is 255, that means all numbers
    # are going to be from 1 - 3 characters

    # Therefore we can define a lambda that adds missing spaces for until
    # the string hits a length of 3
    format_color = lambda col: ' ' * (3 - len(col)) + col

    # Then we can just return the 3 values as a tuple
    return (format_color(str(r)), format_color(str(g)), format_color(str(b)))


def random_colors(lower, uppper):
    ''' Randomly generate colors based on a minimum and maximum
    and format them for ppm output '''

    # Return 3 colors as tuple
    return (random.randint(lower, uppper),
            random.randint(lower, uppper),
            random.randint(lower, uppper))

def save_image(image, p_type='P1', colors=''):
    ''' Create a ppm data based on data from create_ppm_data '''
    # Open a file and estalbish the proper identifiers for the ppm format
    f = open(image.filename, 'w+')
    f.write('{}\n'.format(p_type))

    # size * scale is the actual dimensions of the image
    f.write('{} {}\n'.format(image.size * image.scale, image.size * image.scale))

    # Append colors if availible
    if colors:
        f.write('{}\n'.format(colors))

    # Write the data to the file
    for y in image.ppm_data:
        for x in y:
            f.write(str(x) + '  ')
        f.write('\n')

    f.close()

class Image():
    ''' Image class to hold all data about the PPM image to output '''
    def __init__(self, size, scale, min_color, max_color, mode, filename):
        self.size = size
        self.scale = scale

        self.min_color = min_color
        self.max_color = max_color

        # Check colors
        self.check_colors()

        self.mode = mode
        self.filename = filename

        # Image data
        self.ppm_data = [[0 for x in range(int((size / 2)))]
                            for y in range(size)]

    def check_colors(self):
        ''' Make sure colors do not go over the specified limits '''

        if self.min_color > self.max_color:
            self.min_color = 0
            print('min_color cannot be larger than max_color. \
                Reducing to 0 as a fallback')

        if self.min_color < 0:
            self.min_color = 0
            print('min_color cannot be larger than max_color. \
                Increasing to 0 as a fallback')


        if self.max_color > 255:
            self.max_color = 255
            print('max_color cannot go beyond 255. \
                Reducing to 255 as a fallback.')

        if self.max_color < 0:
            self.max_color = 1
            print('max_color cannot go below 0. \
                Increasing to 1 as a fallback.')

class Rorshach():
    """ Methods for creating pixel rorshach-like images
        with certain parameters """
    def __init__(self, image, rainbow=False, colored_bgs=False):

        self.image = image

        # Optional
        self.rainbow = rainbow
        self.colored_bgs = colored_bgs

    def colorize_ppm(self):
        ''' Modify ppm data to support colors '''

        # Generate fg colors with colored backgrounds (Optional)
        if self.colored_bgs:
            # Generate rgb colors with a high color value for fg
            r, g, b = random_colors(self.image.max_color-50, self.image.max_color)
            # create bg colors by muting the current colors
            mute = random.randint(25, 75)
            rbg, gbg, bbg = (r-mute, g-mute, b-mute)
        else:
            # Generate fg colors
            r, g, b = random_colors(self.image.min_color, self.image.max_color-50)
            # Keep the bg at a high value to create gray to white colors
            # Then keep one color and set the others to it
            rbg, gbg, bbg = random_colors(self.image.max_color-50, self.image.max_color)
            # Randomly choose one color to keep, cull the rest
            if random.randint(1, 3) == 1:
                gbg, bbg = rbg, rbg     # 'Red' got picked
            elif random.randint(1, 2) == 2:
                bbg, rbg = gbg, gbg # 'Blue' got picked
            else:
                rbg, gbg = bbg, bbg # 'Green' got picked

        # Format bg and fg
        r, g, b = format_colors(r, g, b)
        rbg, gbg, bbg = format_colors(rbg, gbg, bbg)

        # For each element, change it to the appropriate color
        for i, y in enumerate(self.image.ppm_data):
            for j, _ in enumerate(y):
                # 1 created from random image generator is the fg...
                if y[j] == 1:
                    y[j] = '{} {} {}'.format(r, g, b)
                    # New random color each time for rainbow mode
                    if self.rainbow:
                        r, g, b = random_colors(self.image.min_color, self.image.max_color-50)
                        r, g, b = format_colors(r, g, b)
                # ...Otherwise it's a bg tile
                else:
                    y[j] = '{} {} {}'.format(rbg, gbg, bbg)

            self.image.ppm_data[i] = y

    def make_image(self):
        ''' Wrapper for making images based on color mode '''

        self.random_pattern()

        if self.image.mode == '256' or self.rainbow or self.colored_bgs:
            self.colorize_ppm()
            self.scale_pattern()
            save_image(self.image, p_type='P3', colors=self.image.max_color)
        elif self.image.mode == 'bw':
            self.scale_pattern()
            save_image(self.image)

    def random_pattern(self):
        ''' Return a 2d list of size x size dimensions
        this will form the basis of the rorshach image '''

        # Set random data
        for i, y in enumerate(self.image.ppm_data):
            for j, _ in enumerate(y):
                y[j] = random.randint(0, 1)

            # Create rorshach symmetry
            # Add a middle column if the size is not even
            if self.image.size % 2 != 0:
                self.image.ppm_data[i] = (y + [random.randint(0, 1)] +
                                    list(reversed(y)))
            else:
                self.image.ppm_data[i] = (y + list(reversed(y)))

    def scale_pattern(self):
        ''' Scale lists by a certain factor '''
        scaled_pattern = []

        for y in self.image.ppm_data:
            # For each row, we create `scale` ammount more of them
            for _ in range(self.image.scale):
                for x in y:
                    _arr = []

                    # For each item in the row, we create `scale` ammount more of them
                    for _ in range(self.image.scale):
                        _arr.append(x)

                    scaled_pattern.append(_arr)

        self.image.ppm_data = scaled_pattern

def parse_args():
    ''' Return an image based on the arguments from arg_parse '''

    # Argparser for command line arguments
    # This parser takes the program name and displays default values
    parser = argparse.ArgumentParser(
        prog='rorshach',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    settings_flags = [
        ['-s', '--size', int, 16,
            'set the length and width of the image in pixels'],
        ['-x', '--scale', int, 20,
            'set the scale factor of the image. For each pixel of the image, it will make them that many times larger'],
        ['-m', '--mode', str, 'bw',
            'set color mode (bw or 256)'],
        ['-o', '--out', str, 'rorschach.ppm',
            'set the name of the output file'],
        ['-u', '--max-color', int, 255,
            'set the upper color boundary (cannot be higher than 255)'],
        ['-l', '--min-color', int, 0,
            'set the lower color boundary']
    ]

    action_flags = [
        ['--rainbow', 'store_true',
            'enable rainbow mode (color only)'],
        ['--colorbgs', 'store_true',
            'enable greater color variety in bg colors (color only)'],
        ['--github', 'store_true',
            'make a github-esque icon (ignores size and color settings)']
    ]

    for flag in settings_flags:
        parser.add_argument(flag[0], flag[1], type=flag[2], default=flag[3],
            help=flag[4])

    for flag in action_flags:
        parser.add_argument(flag[0], action=flag[1], help=flag[2])

    args = parser.parse_args()

    if args.github:
        image = Image(5, args.scale, 50, 255, '256', args.out)
        rorschach = Rorshach(image, args.rainbow, True)
    else:
        image = Image(args.size, args.scale,
                             args.min_color, args.max_color,
                             args.mode, args.out)
        rorschach = Rorshach(image, args.rainbow, args.colorbgs)

    rorschach.make_image()

if __name__ == "__main__":
    parse_args()
