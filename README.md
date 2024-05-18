# pixel-rorschach

Generate a variety of 8-bit style rorschach-esque images

# Usage

`python3 rorschach.py -h` will let you see all of the options:

```sh
usage: rorshach [-h] [-s SIZE] [-x SCALE] [-m MODE] [-o OUT] [-u MAX_COLOR] [-l MIN_COLOR] [--rainbow] [--colorbgs] [--github]

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  set the length and width of the image in pixels (default: 16)
  -x SCALE, --scale SCALE
                        set the scale factor of the image. For each pixel of the image, it will make them that many times larger (default: 20)
  -m MODE, --mode MODE  set color mode (bw or 256) (default: bw)
  -o OUT, --out OUT     set the name of the output file (default: rorschach.ppm)
  -u MAX_COLOR, --max-color MAX_COLOR
                        set the upper color boundary (cannot be higher than 255) (default: 255)
  -l MIN_COLOR, --min-color MIN_COLOR
                        set the lower color boundary (default: 0)
  --rainbow             enable rainbow mode (color only) (default: False)
  --colorbgs            enable greater color variety in bg colors (color only) (default: False)
  --github              make a github-esque icon (ignores size and color settings) (default: False)
```