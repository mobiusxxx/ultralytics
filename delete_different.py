'''
Author: xiafanli xiafanli@eccom.com.cn
Date: 2023-09-14 11:04:10
Description: F:\datasets\yndw\string insulator\img
'''
import os
import shutil

"""
    删除在第一个文件夹中但不在第二个文件夹中的文件
"""

# 定义两个文件夹的路径
folder1 = r"G:\datasets\张泽泉给运监中心要的数据（综合域）\第四批数据\吊臂下站人\images"
folder2 = r"G:\datasets\张泽泉给运监中心要的数据（综合域）\第四批数据\吊臂下站人\labels"

# 获取两个文件夹中的文件名
files_in_folder1 = list(os.path.splitext(file)[0] for file in os.listdir(folder1))
files_in_folder2 = list(os.path.splitext(file)[0] for file in os.listdir(folder2))

# 同名数量大于一的文件
same_name_files = [item for item in set(files_in_folder1) if files_in_folder1.count(item) > 1]

# 删除同名数量大于一的文件
for file in os.listdir(folder1):
    file_without_ext = os.path.splitext(file)[0]
    if file_without_ext in same_name_files:
        os.remove(os.path.join(folder1, file))
        print(f"Deleted {file}")
for file in os.listdir(folder2):
    file_without_ext = os.path.splitext(file)[0]
    if file_without_ext in same_name_files:
        os.remove(os.path.join(folder2, file))
        print(f"Deleted {file}")

files_in_folder1 = set(files_in_folder1)
files_in_folder2 = set(files_in_folder2)

# 找出两个文件夹中没有对应的文件
files_to_delete1 = files_in_folder1 - files_in_folder2
files_to_delete2 = files_in_folder2 - files_in_folder1
files_to_delete = files_to_delete1.union(files_to_delete2)


# 删除这些文件
for file in os.listdir(folder1):
    file_without_ext = os.path.splitext(file)[0]
    if file_without_ext in files_to_delete:
        os.remove(os.path.join(folder1, file))
        print(f"Deleted {file}")
for file in os.listdir(folder2):
    file_without_ext = os.path.splitext(file)[0]
    if file_without_ext in files_to_delete:
        os.remove(os.path.join(folder2, file))
        print(f"Deleted {file}")

# 保证两个文件夹中的文件名一致
files_in_folder1 = set(os.path.splitext(file)[0] for file in os.listdir(folder1))
files_in_folder2 = set(os.path.splitext(file)[0] for file in os.listdir(folder2))


assert files_in_folder1 == files_in_folder2, "The two folders should have the same files."