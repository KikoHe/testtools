import PyPDF2
def count_pdf_layers_and_paths(file_path):
    layers_count = 0
    paths_count = 0

    with open(file_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)

        # 获取 PDF_Check 文件中的页面总数
        num_pages = len(pdf.pages)

        for page_num in range(num_pages):
            page = pdf.pages[page_num]

            # 获取页面中的图层数量
            if '/OCProperties' in page:
                ocg_dict = page['/OCProperties'].get_object()
                layers_count += len(ocg_dict['/OCGs'])

            # 获取页面中的路径数量
            if '/Contents' in page:
                contents = page['/Contents'].get_object()
                if isinstance(contents, PyPDF2.generic.ArrayObject):
                    for obj in contents:
                        if isinstance(obj, PyPDF2.generic.IndirectObject):
                            stream = obj.get_object()
                            if isinstance(stream, PyPDF2.generic.ContentStream):
                                paths_count += stream.operations.count('re')

    return num_pages,layers_count, paths_count


# 调用函数并获取图层和路径数量
file_path = '/pythonProject/PDF_Check/8986a334022ec0d9cbdee48290ffecc2.pdf'
num_pages,layers_count, paths_count = count_pdf_layers_and_paths(file_path)
print(f"Number of Pages: {num_pages}")
print(f"Number of Layers: {layers_count}")
print(f"Number of Paths: {paths_count}")
