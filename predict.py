'''
Author: xiafanli xiafanli@eccom.com.cn
Date: 2024-10-17 17:07:52
Description: 
'''

import warnings
warnings.filterwarnings('ignore')
from ultralytics import RTDETR

if __name__ == '__main__':
    model = RTDETR('runs/train/r18_r2_0.65/r18-pretrained-blip_0.7_0.65/weights/best.pt')
    model.predict('dataset/od_dataset/images/test', 
                project='runs/predict/r18_r2_0.65',
                name='r18-pretrained-blip_0.7_0.65',
                save=True, imgsz=640)