# OCR로 이미지에서 텍스트 추출
#곡명과 가수 분리 -> Spotify 검색용 문자열 준비

#실제 서비스를 준비하기 전에 사진 한장을 가지고 Spotify 플레이리스트 연동 과정 완료까지 실행 테스트

import pytesseract
from PIL import Image

img = Image.open("1104/ocr01.png")
text = pytesseract.image_to_string(img, lang="kor+eng")

#print(text)
