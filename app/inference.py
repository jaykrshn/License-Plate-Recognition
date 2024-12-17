from fast_plate_ocr import ONNXPlateRecognizer # type: ignore
import cv2
from .yolo_inference import main
import os

def save_image(image, output_path):
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    is_written = cv2.imwrite(output_path, image)

    if is_written:
        print(f"Image successfully saved to {output_path}")
    else:
        print("Error: Could not save the image.")

def delete_image(output_path):

    try:
        os.remove(output_path)  # Deletes the file
        print(f"Image {output_path} has been deleted successfully.")
    except FileNotFoundError:
        print(f"Error: {output_path} not found.")
    except Exception as e:
        print(f"Error occurred while deleting the file: {e}")


def read_license_plate(image):

    image_path = "app/temp/predict_image.jpg"  # Output file path
    save_image(image,image_path)

    yolo_model= "app/trained_model/best.onnx"

    main(yolo_model,image_path)

    delete_image(image_path)

    m = ONNXPlateRecognizer('european-plates-mobile-vit-v2-model')
    print(m.run('app/temp/plate.jpg')[0])
    text=str(m.run('app/temp/plate.jpg')[0])

    return text

