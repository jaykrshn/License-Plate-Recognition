import onnxruntime as ort
import cv2
import numpy as np
import time

def preprocess_image(image_path, input_shape):
    """
    Preprocess the input image to match the model's input requirements.
    :param image_path: Path to the input image.
    :param input_shape: Tuple of (height, width) expected by the model.
    :return: Preprocessed image tensor and original image for visualization.
    """
    original_image = cv2.imread(image_path)
    if original_image is None:
        raise FileNotFoundError(f"Image file '{image_path}' not found.")

    # Resize image to match model's expected input size
    resized_image = cv2.resize(original_image, (input_shape[1], input_shape[0]))

    # Convert to RGB
    rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

    # Normalize (0-255) -> (0.0-1.0)
    normalized_image = rgb_image / 255.0

    # HWC to CHW format for ONNX input
    input_tensor = np.transpose(normalized_image, (2, 0, 1)).astype(np.float32)

    # Add batch dimension (1, C, H, W)
    input_tensor = np.expand_dims(input_tensor, axis=0)
    
    return input_tensor, original_image

def postprocess(outputs, input_shape, orig_shape):
    """
    Postprocess the model outputs to extract the bounding box with the highest confidence score.
    :param outputs: Raw outputs from the model (1, 5, N).
    :param input_shape: Tuple of (height, width) used for input resizing.
    :param orig_shape: Original image shape (H, W).
    :return: Bounding box with the highest confidence and its score.
    """
    # Extract the output array
    predictions = outputs[0]  # Shape: (1, 5, 2100)
    
    # Remove the batch dimension: (5, 2100)
    predictions = np.squeeze(predictions, axis=0)

    # Find the index of the highest confidence score
    confidences = predictions[4, :]  # Confidence scores are in the 5th row
    max_index = np.argmax(confidences)  # Index of the highest confidence

    # Extract the bounding box and confidence score
    x, y, w, h, confidence = predictions[:, max_index]

    # Scale bounding box back to original image dimensions
    x = int((x / input_shape[1]) * orig_shape[1])
    y = int((y / input_shape[0]) * orig_shape[0])
    w = int((w / input_shape[1]) * orig_shape[1])
    h = int((h / input_shape[0]) * orig_shape[0])

    # Convert to top-left corner format
    x1 = x - w // 2
    y1 = y - h // 2
    x2 = x1 + w
    y2 = y1 + h

    box = [x1, y1, x2, y2]

    return box, confidence

# def visualize_results(image, box, score):
#     """
#     Draw bounding boxes and scores on the original image.
#     :param image: Original image.
#     :param box: Bounding boxes (bbox) detected.
#     :param score: Confidence score of the bbox.
#     """
#     x1, y1, x2, y2 = box
    
#     # Draw the bounding box
#     cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    
#     # Display the confidence score near the bounding box
#     score_text = f"Score: {score:.2f}"
#     cv2.putText(image, score_text, (x1, y1 - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)
    
#     # Show the image with bounding boxes and score
#     cv2.imshow("Detection Results", image)
#     key = cv2.waitKey(0)
#     if key == 27:  # 27 is the ASCII code for the 'Esc' key
#         cv2.destroyAllWindows()

def save_cropped_image(image, box, save_path):
    """
    Crop the detected object from the image and save it as a separate file.
    :param image: Original image.
    :param box: Bounding box coordinates [x1, y1, x2, y2].
    :param save_path: Path to save the cropped image.
    """
    x1, y1, x2, y2 = box
    
    # Crop the image using the bounding box coordinates
    cropped_image = image[y1:y2, x1:x2]
    
    # Save the cropped image
    cv2.imwrite(save_path, cropped_image)
    print(f"Cropped image saved to {save_path}.")


def main(model_path,image_path):
    # Set providers (CUDA or CPU)
    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']

    print(f"Loading model from {model_path}...")
    ort_session = ort.InferenceSession(model_path, providers=providers)

    # Model input shape (assume dynamic input shape)
    input_shape = ort_session.get_inputs()[0].shape[2:4]  # (height, width)
    print(f"Model expects input shape: {input_shape}")

    # Preprocess the input image
    input_tensor, original_image = preprocess_image(image_path, input_shape)
    print("Image preprocessed successfully.")

    # Perform inference
    print("Running inference...")
    start_time = time.time()
    outputs = ort_session.run(None, {ort_session.get_inputs()[0].name: input_tensor})
    end_time = time.time()
    print(f"Inference completed in {end_time - start_time:.2f} seconds.")

    print(len(outputs))
    print(type(outputs[0]))
    print(outputs[0].shape)
    print(type(outputs))

    # Postprocess the results
    box, score = postprocess(outputs, input_shape, original_image.shape[:2])
    print(f"Detected box {box} with confidence {score}.")

    # # Visualize results
    # visualize_results(original_image, box, score)

    save_path = "temp/plate.jpg"  # Save with a timestamp
    save_cropped_image(original_image, box, save_path)

if __name__ == "__main__":

    print('---')
