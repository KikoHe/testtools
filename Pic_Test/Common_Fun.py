import glob
import os,shutil

current_directory = os.getcwd()

# 删除当前目录及子目录下所有包含PicID的.zip文件
def remove_zip_files_and_directories(PicID):
    zip_files = glob.glob(f'**/*{PicID}*.zip', recursive=True)
    for zip_file in zip_files:
        try:
            os.remove(zip_file)
            # print(f"已删除文件：{zip_file}")
        except OSError as e:
            print(f"无法删除文件 {zip_file}。原因：{e.strerror}")

    # 删除当前目录及子目录下所有名称中包含PicID的目录
    directories = glob.glob(f'**/*{PicID}*', recursive=True)
    for directory in directories:
        if os.path.isdir(directory):  # 确认这是一个目录
            try:
                shutil.rmtree(directory)
                # print(f"已删除目录：{directory}")
            except OSError as e:
                print(f"无法删除目录 {directory}。原因：{e.strerror}")

# 遍历文件夹中的所有文件和子文件夹，并删除
def delete_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            # 如果是文件，则删除
            os.remove(file_path)
        elif os.path.isdir(file_path):
            # 如果是子文件夹，则递归删除
            shutil.rmtree(file_path)

# folder_path = '/Users/ht/Desktop/PythonTools/Pic_Check/Pic/'  # 替换为您的文件夹路径
# delete_folder(folder_path)

