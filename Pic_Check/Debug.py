from PIL import Image
import cairosvg

# 读取矢量资源文件（例如SVG）
with open('/Users/ht/Desktop/PythonTools/Pic_Check/Pic/65e559a4a0a5acce482dae18/65e559a4a0a5acce482dae18_vector.svg', 'rb') as f:
    svg_data = f.read()

# 使用cairosvg将SVG转换为位图
png_data = cairosvg.svg2png(bytestring=svg_data)

# 将位图数据保存为PNG文件
with open('output_bitmap.png', 'wb') as f:
    f.write(png_data)
