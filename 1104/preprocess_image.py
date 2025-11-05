# 우선 이미지 전처리로 이미지 품질 향상을 해야 한다.
# OpenCV로 글자 선명도 개선, 노이즈 제거

import cv2
import numpy as np

def preprocess_image(input_path, output_path="preprocessed.png"):
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    denoised = cv2.medianBlur(thresh, 3)
    cv2.imwrite(output_path, denoised)
    print(f"전처리 완료: {output_path}")

if __name__ == "__main__":
    preprocess_image("/home/ubuntu/ocr_svc/1104/ocr01.png")