# -*- coding: utf-8 -*-

from PIL import Image
import colorsys
import sys
'''提取图标色值'''

def extract(f):
    image = f if isinstance(f, Image.Image) else Image.open(f)
    if image.mode not in ('RGB', 'RGBA', 'RGBa'):
        image = image.convert('RGB')

    (h, s, l) = avg_hsl(image)


def avg_hsl(image):
    width, height = image.size
    pixels = image.load()
    count = 0
    total_r = 0
    total_g = 0
    total_b = 0
    for y in range(round(height)):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            total_r += r
            total_g += g
            total_b += b
            count += 1
    r = total_r / count
    g = total_g / count
    b = total_b / count

    # hexstr = hex((r << 16) + (g << 8) + b)

    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

    h_n = h
    s_n = round(0.6 * s + 0.4, 5)
    l_n = round(0.7 * l + 0.3, 5)

    r_n, g_n, b_n = colorsys.hls_to_rgb(h_n, l_n, s_n)
    r_n, g_n, b_n = round(255 * r_n), round(255 * g_n), round(255 * b_n)

    hexstr_n = hex((r_n << 16) + (g_n << 8) + (b_n))

    print("RGB(Old):", r, g, b)
    print("HSL(Old):", round(h * 360), round(s * 100), round(l * 100))
    # print("HEX(Old):", hexstr.replace('0x', '#').upper())
    print("RGB(New):", r_n, g_n, b_n)
    print("HSL(New):", round(h_n * 360), round(s_n * 100), round(l_n * 100))
    print("HEX(New):", hexstr_n.replace('0x', '#').upper())

    return (h, s, l)


if __name__ == '__main__':
    extract(sys.argv[1])