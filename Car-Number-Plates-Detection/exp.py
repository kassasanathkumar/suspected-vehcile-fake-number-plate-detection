import cv2
import easyocr
import pandas as pd
import os

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Path to the directory containing plate images
plate_directory = "C:/Users/kassa/OneDrive/Desktop/EDT PROJECT/pythonProject1/Car-Number-Plates-Detection/plates"

# Prepare results list
results = []

# Process each image in the plates directory
for filename in os.listdir(plate_directory):
    if filename.startswith("scaned_img_") and filename.endswith(".jpg"):
        # Construct the full path to the image
        image_path = os.path.join(plate_directory, filename)

        # Read the image
        img = cv2.imread(image_path)
        if img is None:
            continue

        # Convert the image to grayscale (optional, can help with some OCR tasks)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Perform OCR on the image
        ocr_result = reader.readtext(img_gray)

        # Extract text and check if OCR detected something
        plate_text = ""
        for (bbox, text, prob) in ocr_result:
            plate_text += text + " "

        # Print recognized plate text and append to results
        if plate_text.strip():
            print(f"Recognized Plate from {filename}: {plate_text}")
            results.append({"Image": filename, "Text": plate_text.strip(), "Status": "Real"})
        else:
            print(f"Recognition failed for {filename}.")
            results.append({"Image": filename, "Text": "Recognition failed", "Status": "Fake"})

# Save results to an Excel file
df = pd.DataFrame(results)
df.to_excel("plates_recognition_results.xlsx", index=False)

print("Processing completed. Results saved to plates_recognition_results.xlsx.")
