from PIL import Image, ImageDraw, ImageFont

from bitarray.util import zeros, gen_primes


def draw_bitarray(a, size, colors, mul=1):
    font = ImageFont.truetype("Vera.ttf", 0.36 * size)

    im = Image.new('RGB', (size * len(a) + 1, size + 1))
    dr = ImageDraw.Draw(im)
    for i, v in enumerate(a):
        dr.rectangle([(i * size, 0), ((i+1) * size, size)],
                     fill=colors[v],
                     outline="black")
        dr.text(((i + 0.5) * size, 0.5 * size),
                str(mul * i), anchor='mm',
                fill=colors[v + 2], font=font)
    return im

def lines(n, size):
    im = Image.new('RGB', (size * n + 1, 2 * size + 1), color="#fff")
    dr = ImageDraw.Draw(im)
    h = 2 * size
    for i in range(5):
        j = 6 * i + 1
        dr.line([((i + 0.5) * size, h), ((j + 0.5) * size, 0)],
                fill="#eee" if i in (0, 4) else '#fa7',
                width=5)
    return im

def dubner():
    primes = gen_primes(10_000)
    middles = (primes >> 1 & primes << 1)

    sqr = 50    # square size
    space = 20  # spacing
    size = (2 * space + 25 * sqr,
            3 * space + 17 * sqr)
    print(size)
    colors1 = ['#eee', '#369', '#000', '#fff']
    colors2 = ['#eee', '#fa7', '#000', '#000']
    colors3 = ['#eee', '#d66', '#000', '#fff']

    im = Image.new('RGB', size, color='#fff')
    im.paste(lines(25, sqr),
             (space, space + 3 * sqr))

    im.paste(draw_bitarray(primes[:25], sqr, colors1),
             (space, space))
    im.paste(draw_bitarray(primes[:23], sqr, colors1),
             (space + 2 * sqr, space + sqr))
    im.paste(draw_bitarray(middles[:24], sqr, colors2),
             (space + sqr, space + 2 * sqr))

    middles = middles[::6]
    im.paste(draw_bitarray(middles[:25], sqr, colors2, 6),
             (space, space + 5 * sqr))

    mark = zeros(len(middles))
    for i in middles.search(1):
        mark |= middles >> i
    print([6 * i for i in mark.search(0, 2)])
    for i, j in enumerate(middles.search(1, 0, 24)):
        im.paste(draw_bitarray(middles[:25 - j], sqr, colors1, 6),
                 (space + j * sqr, 2 * space + 6 * sqr + i * sqr))

    im.paste(draw_bitarray(mark[:25], sqr, colors1, 6),
             (space, 2 * space + 16 * sqr))

    im.save('image.png')


if __name__ == '__main__':
    dubner()
