# OCR로 이미지에서 텍스트 추출
# 전처리된 이미지를 불러와 글자 그대로 텍스트로 바꾼다
#곡명과 가수 분리 -> Spotify 검색용 문자열 준비

#실제 서비스를 준비하기 전에 사진 한장을 가지고 Spotify 플레이리스트 연동 과정 완료까지 실행 테스트

import pytesseract
from PIL import Image

img = Image.open("1104/ocr01.png")
text = pytesseract.image_to_string(img, lang="kor+eng")

print(text)

#def extract_text(image_path):
#    custom_config = r'--oem 3 --psm 6 -l kor+eng'
#    text = pytesseract.image_to_string(Image.open(image_path), config=custom_config)
#    return text

#if __name__ == "__main__":
#    text = extract_text("preprocessed.png")
#    print(text)