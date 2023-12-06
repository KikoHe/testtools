import glob
import os,shutil

def remove_zip_files_and_directories(PicID):
    # 删除当前目录及子目录下所有包含PicID的.zip文件
    zip_files = glob.glob(f'**/*{PicID}*.zip', recursive=True)
    for zip_file in zip_files:
        try:
            os.remove(zip_file)
            print(f"已删除文件：{zip_file}")
        except OSError as e:
            print(f"无法删除文件 {zip_file}。原因：{e.strerror}")

    # 删除当前目录及子目录下所有名称中包含PicID的目录
    directories = glob.glob(f'**/*{PicID}*', recursive=True)
    for directory in directories:
        if os.path.isdir(directory):  # 确认这是一个目录
            try:
                shutil.rmtree(directory)
                print(f"已删除目录：{directory}")
            except OSError as e:
                print(f"无法删除目录 {directory}。原因：{e.strerror}")

# 调用函数
# remove_zip_files_in_current_directory()
