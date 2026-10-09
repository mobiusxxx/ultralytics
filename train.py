'''
Author: xiafanli xiafanli@eccom.com.cn
Date: 2024-04-22 11:17:38
Description: 
'''
from ultralytics import YOLO

def main():
    # Load a model
    model = YOLO(r"F:\weights\yolov8\yolov8x-cls.pt")  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(data=r'H:\Standard calibration\datasets', epochs=100, imgsz=640)

if __name__ == '__main__':
    main()