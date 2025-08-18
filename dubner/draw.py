from PIL import Image, ImageDraw, ImageFont

from bitarray.util import zeros, gen_primes


def draw_bitarray(a, size, colors=None, font=None, imap=lambda i: i):
    if colors is None:
        colors = ['#eee', '#369', '#000', '#fff']
    if font is None:
        font = ImageFont.truetype("Vera.ttf", 0.36 * size)

    im = Image.new('RGB', (size * len(a) + 1, size + 1))
    dr = ImageDraw.Draw(im)
    for i, v in enumerate(a):
        dr.rectangle([(i * size, 0), ((i+1) * size, size)],
                     fill=colors[v],
                     outline="black")
        if font:
            dr.text(((i + 0.15) * size, 0.3 * size),
                    str(imap(i)),
                    fill=colors[v + 2], font=font)
    return im

def dubner():
    twins = gen_primes(10_000, odd=True)
    twins &= twins << 1
    middles = twins[2::3] >> 1
    mark = zeros(len(middles))
    for i in middles.search(1):
        mark |= middles >> i
    print([6 * i for i in mark.search(0, 2)])

    sqr = 50    # square size
    space = 20  # spacing
    imap = lambda i: 6 * i
    size = (2 * space + 25 * sqr,
            4 * space + 12 * sqr)
    print(size)
    im = Image.new('RGB', size, color='#fff')
    colors = ['#eee', '#fa7', '#000', '#000']
    im.paste(draw_bitarray(middles[:25], sqr, colors, imap=imap),
             (space, space))

    for i, j in enumerate(middles.search(1, 0, 24)):
        im.paste(draw_bitarray(middles[:25 - j], sqr, None, imap=imap),
                 (space + j * sqr, 2 * space + sqr + i * sqr))

    im.paste(draw_bitarray(mark[:25], sqr, None, imap=imap),
             (space, 3 * space + 11 * sqr))

    im.save('image.png')


if __name__ == '__main__':
    dubner()
