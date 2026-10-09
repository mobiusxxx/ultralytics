'''
Author: xiafanli xiafanli@eccom.com.cn
Date: 2024-05-11 15:44:43
Description: 
'''
from ultralytics import YOLO
# Load a model
model = YOLO(r"F:\weights\yndw\falldown_20240527.pt")  # load an official model
model.export(format='onnx')