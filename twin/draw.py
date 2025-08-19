from PIL import Image, ImageDraw, ImageFont

from bitarray.util import gen_primes


def draw_bitarray(a, size, imap=lambda i: i):
    colors = ['#eee', '#369', '#000', '#fff']
    font = ImageFont.truetype("Vera.ttf", 0.36 * size)

    im = Image.new('RGB', (size * len(a) + 1, size + 1))
    dr = ImageDraw.Draw(im)
    for i, v in enumerate(a):
        dr.rectangle([(i * size, 0), ((i+1) * size, size)],
                     fill='#e44' if i == 2 == imap(2) else colors[v],
                     outline="#000")
        dr.text(((i + 0.15) * size, 0.3 * size),
                str(imap(i)),
                fill=colors[v + 2], font=font)
    return im

def polygons(n, size):
    im = Image.new('RGB', (size * n + 1, 2 * size + 1), color="#fff")
    dr = ImageDraw.Draw(im)
    h = 2 * size
    for i in range(n // 2):
        j = 2 * i + 1
        dr.polygon([(i * size, h), (j * size, 0),
                    ((j + 1) * size, 0), ((i + 1) * size, h)],
                   fill="#acf")
    return im

def twins():
    n = 25
    sqr = 50    # square size
    border = 20
    map_odd = lambda i: 2 * i + 1
    size = (2 * border + n * sqr,
            2 * border + 6 * sqr)
    print(size)
    im = Image.new('RGB', size, color='#fff')
    im.paste(polygons(n, sqr),
             (border, border + sqr))

    im.paste(draw_bitarray(gen_primes(n), sqr),
             (border, border))

    primes = gen_primes(n, odd=True)
    im.paste(draw_bitarray(primes, sqr, imap=map_odd),
             (border, border + 3 * sqr))

    twins = primes.copy()
    twins &= twins << 1
    im.paste(draw_bitarray(twins, sqr, imap=map_odd),
             (border, border + 4 * sqr))
    twins |= twins >> 1
    im.paste(draw_bitarray(twins, sqr, imap=map_odd),
             (border, border + 5 * sqr))

    im.save('image.png')

if __name__ == '__main__':
    twins()
