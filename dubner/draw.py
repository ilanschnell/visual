from PIL import Image, ImageDraw, ImageFont

from bitarray.util import zeros, gen_primes


def draw_bitarray(a, size, colors, imap=lambda i: 6 * i):
    font = ImageFont.truetype("Vera.ttf", 0.36 * size)

    im = Image.new('RGB', (size * len(a) + 1, size + 1))
    dr = ImageDraw.Draw(im)
    for i, v in enumerate(a):
        dr.rectangle([(i * size, 0), ((i+1) * size, size)],
                     fill=colors[v],
                     outline="black")
        dr.text(((i + 0.5) * size, 0.5 * size),
                str(imap(i)), anchor='mm',
                fill=colors[v + 2], font=font)
    return im

def polygons(n, size):
    im = Image.new('RGB', (size * n + 1, 2 * size + 1), color="#fff")
    dr = ImageDraw.Draw(im)
    h = 2 * size
    for i in range(5):
        j = 6 * i
        dr.polygon([(i * size, h), (j * size, 0),
                    ((j + 1) * size, 0), ((i + 1) * size, h)],
                   fill="#eee" if i in (0, 4) else '#fa7')
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
    im.paste(polygons(25, sqr),
             (space, space + 3 * sqr))

    im.paste(draw_bitarray(primes[:24], sqr, colors1, lambda i: i),
             (space + sqr, space))
    im.paste(draw_bitarray((primes << 1)[:25], sqr, colors1, lambda i: i + 1),
             (space, space + sqr))
    im.paste(draw_bitarray(middles[:25], sqr, colors2, lambda i: i),
             (space, space + 2 * sqr))

    middles = middles[::6]
    im.paste(draw_bitarray(middles[:25], sqr, colors2),
             (space, space + 5 * sqr))

    mark = zeros(len(middles))
    for i in middles.search(1):
        mark |= middles >> i
    print([6 * i for i in mark.search(0, 2)])
    for i, j in enumerate(middles.search(1, 0, 24)):
        im.paste(draw_bitarray(middles[:25 - j], sqr, colors1),
                 (space + j * sqr, 2 * space + 6 * sqr + i * sqr))

    im.paste(draw_bitarray(mark[:25], sqr, colors3),
             (space, 2 * space + 16 * sqr))

    im.save('image.png')


if __name__ == '__main__':
    dubner()
