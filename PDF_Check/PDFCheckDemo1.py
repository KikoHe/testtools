import PyPDF2,os
def check_resource_pdf(resource_path):
    try:
        with open(resource_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)

            # 检查PDF文件的页数
            num_pages = len(pdf_reader.pages)

            if num_pages > 0:
                print(f"The resource at {resource_path} is in PDF_Check format.")
            else:
                print(f"The resource at {resource_path} is not in PDF_Check format.")

            # 检查PDF文件的标题属性
            title = pdf_reader.metadata.get('/Title')

            if title:
                print(f"The resource at {resource_path} is a valid PDF_Check with title: {title}")
            else:
                print(f"The resource at {resource_path} is a valid PDF_Check without a title.")

    except Exception as e:
        print(f"Error occurred while checking the resource: {str(e)}")


def check_pdf_extension(file_path):
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)  # 读取文件头部的前四个字节

            if header == b'%PDF_Check':
                print(f"The file at {file_path} is a valid PDF_Check.")
            else:
                print(f"The file at {file_path} is not a valid PDF_Check.")

    except Exception as e:
        print(f"Error occurred while checking the file: {str(e)}")



def count_pdf_resources(directory_path):
    pdf_count = 0

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_count += 1
    if pdf_count > 3:
        print("The number of PDF_Check resources exceeds 3.")
    else:
        print("The number of PDF_Check resources does not exceed 3.")

def count_pdf_layers_and_paths(file_path):
    layers_count = 0
    paths_count = 0

    with open(file_path, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)

        # 获取 PDF_Check 文件中的页面总数
        num_pages = pdf.numPages

        for page_num in range(num_pages):
            page = pdf.getPage(page_num)

            # 获取页面中的图层数量
            if '/OCProperties' in page:
                ocg_dict = page['/OCProperties'].getObject()
                layers_count += len(ocg_dict['/OCGs'])

            # 获取页面中的路径数量
            if '/Contents' in page:
                contents = page['/Contents'].getObject()
                if isinstance(contents, PyPDF2.generic.ArrayObject):
                    for obj in contents:
                        if isinstance(obj, PyPDF2.pdf.ContentStream):
                            paths_count += obj.operations.count('re')

    return layers_count, paths_count


# 调用函数并获取图层和路径数量
file_path = 'path/to/file.pdf'
layers_count, paths_count = count_pdf_layers_and_paths(file_path)
print(f"Number of Layers: {layers_count}")
print(f"Number of Paths: {paths_count}")

import argparse
parser = argparse.ArgumentParser(description='检查图片格式是否PDF')
parser.add_argument('file', type=str, help='检测文件路径')

args = parser.parse_args()

# 获取文件路径参数
resource_path = args.file
# 检查文件格式
count_pdf_resources(resource_path)