#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: zhangyanwei  
# @Creat Time : 2024/5/4 15:07
# @File: save_result.py  
# @Project: dataset_format_converter
import os.path
import xml.etree.ElementTree as ET
import cv2
import numpy as np
from ultralytics import YOLO

def parse_voc(label_file):
    """
    解析voc标注文件格式，返回字典对象
    :param label_file:
    :return:dict
    """
    assert label_file.endswith('.xml'), f'file_path must be xml format'
    et = ET.parse(label_file)
    root = et.getroot()

    def get_child(item):
        ret_dict = {}
        for child in item:
            if len(child):
                if child.tag == 'object':
                    if child.tag not in ret_dict.keys():
                        ret_dict[child.tag] = []
                    ret_dict[child.tag].append(get_child(child))
                else:
                    ret_dict[child.tag] = get_child(child)
            else:
                ret_dict[child.tag] = child.text
        return ret_dict

    ret_parse = get_child(root)
    return ret_parse


def plot_images_with_voc_anno(img_dir, anno_dir, save_dir=None):
    """
    :param img_dir:原始图像目录
    :param anno_dir:标注图像目录
    :param save_dir:绘制图像存储目录
    :return: None
    """
    support_img_fmts = ['.jpg', '.png', '.bmp', '.jpeg']

    image_files = os.listdir(img_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    def plot_one_image(img_file, anno_file):
        voc_anno_dict = parse_voc(anno_file)
        image = cv2.imdecode(np.fromfile(img_file, dtype=np.uint8), flags=cv2.IMREAD_COLOR)

        if voc_anno_dict.get('object', None):
            for item in voc_anno_dict['object']:
                xmin = int(item['bndbox']['xmin'])
                xmax = int(item['bndbox']['xmax'])
                ymin = int(item['bndbox']['ymin'])
                ymax = int(item['bndbox']['ymax'])
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=(0, 0, 255), thickness=3, lineType=cv2.LINE_AA)
        return image

    for file_name in image_files:
        name, suffix = os.path.splitext(file_name)
        if suffix.lower() in support_img_fmts:
            anno_file_path = os.path.join(anno_dir, f'{name}.xml')
            img_file_path = os.path.join(img_dir, file_name)
            # 如果标注文件不存在，跳过
            if not os.path.exists(anno_file_path):
                continue
            ploted = plot_one_image(img_file_path, anno_file_path)
            cv2.imencode(suffix.lower(), ploted)[1].tofile(os.path.join(save_dir, file_name))

def plot_images_with_yolo_anno(img_dir, anno_dir, save_dir=None):
    """
    :param img_dir:原始图像目录
    :param anno_dir:标注图像目录
    :param save_dir:绘制图像存储目录
    :return: None
    """
    support_img_fmts = ['.jpg', '.png', '.bmp', '.jpeg']

    image_files = os.listdir(img_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    def plot_one_image(img_file, anno_file):
        image = cv2.imdecode(np.fromfile(img_file, dtype=np.uint8), flags=cv2.IMREAD_COLOR)
        h, w = image.shape[:2]
    
        with open(anno_file, 'r') as f:
            annos = f.readlines()

        for anno in annos:
            parts = anno.strip().split()
            class_id, x_center, y_center, width, height = map(float, parts)
            class_id = int(class_id)

            x_center *= w
            y_center *= h
            width *= w
            height *= h

            x1 = int(x_center - width / 2)
            y1 = int(y_center - height / 2)
            x2 = int(x_center + width / 2)
            y2 = int(y_center + height / 2)

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # 在框上标注类别
            cv2.putText(image, str(class_id), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

        return image


    for file_name in image_files:
        name, suffix = os.path.splitext(file_name)
        if suffix.lower() in support_img_fmts:
            anno_file_path = os.path.join(anno_dir, f'{name}.txt')
            img_file_path = os.path.join(img_dir, file_name)
            # 如果标注文件不存在，跳过
            if not os.path.exists(anno_file_path):
                continue
            ploted = plot_one_image(img_file_path, anno_file_path)
            cv2.imencode(suffix.lower(), ploted)[1].tofile(os.path.join(save_dir, file_name))


def save_results_2_voc_format(results, img_shape, img_filename, result_dir, data_source='test_images'):
    """
    将识别结果保存到voc格式的xml文件中
    :param results:list,识别结果列表, 形如：[[xmin,ymin,xmax,ymax,conf,cls_name],...]
    :param img_shape:tuple 或 list, 图像shape,[height,width,channel]
    :param result_dir:str, 识别结果文件保存路径
    :param img_filename:str, 图像文件,如： "aaa.jpg"
    :param source:str, 数据来源，格式为数字或英文字母组成的字符串，如：jueyuanzi
    :return: str, 结果保存文件地址
    """
    root = ET.Element('annotation')
    folder = ET.SubElement(root, 'folder')
    folder.text = data_source

    filename = ET.SubElement(root, 'filename')
    filename.text = img_filename

    path = ET.SubElement(root, 'path')
    path.text = 'Unknown'

    source = ET.SubElement(root, 'source')
    database = ET.SubElement(source, 'database')
    database.text = data_source

    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    width.text = str(img_shape[1])
    height = ET.SubElement(size, 'height')
    height.text = str(img_shape[0])
    depth = ET.SubElement(size, 'depth')
    depth.text = str(img_shape[2])

    segmented = ET.SubElement(root, 'segmented')
    segmented.text = '0'

    for result in results:
        xmin, ymin, xmax, ymax, conf, cls_name = result
        object = ET.SubElement(root, 'object')

        name = ET.SubElement(object, 'name')
        name.text = cls_name

        pose = ET.SubElement(object, 'pose')
        pose.text = 'Unspecified'

        truncated = ET.SubElement(object, 'truncated')
        truncated.text = '0'

        difficult = ET.SubElement(object, 'difficult')
        difficult.text = '0'

        bndbox = ET.SubElement(object, 'bndbox')
        xmin_item = ET.SubElement(bndbox, 'xmin')
        xmin_item.text = str(int(xmin))
        ymin_item = ET.SubElement(bndbox, 'ymin')
        ymin_item.text = str(int(ymin))
        xmax_item = ET.SubElement(bndbox, 'xmax')
        xmax_item.text = str(int(xmax))
        ymax_item = ET.SubElement(bndbox, 'ymax')
        ymax_item.text = str(int(ymax))

    tree = ET.ElementTree(root)
    output_file_name, _ = os.path.splitext(img_filename)
    output_file = os.path.join(result_dir, f'{output_file_name}.xml')
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

    return output_file


if __name__ == '__main__':

    ## 识别结果保存为voc文件格式
    # results = [[1516, 1258, 1616, 1383, 0.56, '40080003'], [1516, 1258, 1616, 1383, 0.56, '40080003']]
    # image_shape = [3078, 5472, 3]
    # image_file = 'test_voc.jpg'
    # model = YOLO(r"F:\weights\yndw\jueyuanzi_20240506.pt")  # load a pretrained model (recommended for training)
    root_path = r'G:\datasets\综合数据赛道数据\第四批数据_20240527\跨越围栏'
    image_dir = os.path.join(root_path, 'images')
    result_dir = os.path.join(root_path, 'xmls')
    output_dir = os.path.join(root_path, 'output')
    import time
    start = time.time()
    # # 遍历文件夹下所有图片
    # image_files = os.listdir(image_dir)
    # for image_file in image_files:
    #     image_path = os.path.join(image_dir, image_file)
    #     image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), flags=cv2.IMREAD_COLOR)
    #     preds = model.predict(source=image,iou=0.5,conf = 0.4)
    #     results = preds[0].boxes.data
    #     image_shape = image.shape
    #     # 识别结果为空时，跳过
    #     if len(results) == 0:
    #         continue
    #     result_path = save_results_2_voc_format(results, image_shape, image_file, result_dir=result_dir,
    #                                             data_source='jueyuanzi')
    #     print(f'results saved to {result_path}')

    # print(f'cost time:{time.time()-start}')

    ##  检查识别结果（VOC格式），保存绘制图片到output_dir
    plot_images_with_voc_anno(img_dir=image_dir, anno_dir=result_dir, save_dir=output_dir)
    # plot_images_with_yolo_anno(img_dir=image_dir, anno_dir=result_dir, save_dir=output_dir)
