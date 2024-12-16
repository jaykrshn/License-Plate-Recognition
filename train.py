from ultralytics import YOLO

if __name__== '__main__':
    #load model
    model=YOLO("yolo11s.pt")

    #train model
    train_result = model.train(
        data="/home/jayakrishnan/Documents/Projects/License-Plate-Recognition/dataset/data.yaml",
        epochs=8,
        imgsz=300,
        device=0
    )

    # Export the model to ONNX format
    model.export(format="onnx")  # creates 'yolo11n.onnx'
