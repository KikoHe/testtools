###通过PDF资源的路径，来检查资源是否为正常的PDF资源
import fitz,argparse

### 除了直接引用的库外，还需要安装PyMuPDF、frontend
def extract_paths_from_pdf(file_path):
    paths = []
    try:
        with fitz.open(file_path) as pdf:
            for page in pdf:
                shapes = page.get_drawings()
                for shape in shapes:
                    if shape["type"] == "f" or "s":  # 类型为f/s表示路径对象
                        paths.append(shape)
        # 打印路径数量和示例路径
        if len(paths) > 0:
            print(f"Number of Paths: {len(paths)}")
            print(f"Valid PDF")
        else:
            print(f"Number of Paths: {len(paths)}")
            print(f"Invalid PDF")
    except Exception as e:
        print(f"Not PDF")
    # return paths

# # 调用函数并获取 PDF_Check 的路径
# file_path = '/Users/ht/Desktop/AutoTesttools/pythonProject/PDF_Check/8986a334022ec0d9cbdee48290ffecc2.pdf'
# pdf_paths = extract_paths_from_pdf(file_path)

parser = argparse.ArgumentParser(description='检查图片格式是否PDF')
parser.add_argument('file', type=str, help='检测文件路径')

args = parser.parse_args()

# 获取文件路径参数
resource_path = args.file
# 检查文件格式
extract_paths_from_pdf(resource_path)
