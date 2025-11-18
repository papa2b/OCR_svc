import easyocr
import re
import cv2
from PIL import Image
import numpy as np
import csv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# ================= OCR 전처리 =================
# 이미지 읽기
img = cv2.imread("1112/ocr02.png")

# 그레이스케일 변환
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 글자 선명하게 확대
gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# 이진화
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# OpenCV -> PIL로 변환
preprocessed_img = Image.fromarray(thresh)
preprocessed_img.save("preprocessed.png")  # 확인용

# ================= EasyOCR 읽기 =================
reader = easyocr.Reader(['ko', 'en'])
results = reader.readtext("preprocessed.png", detail=0)

# OCR 결과 합치기
text = "\n".join(results)

# ================= 텍스트 후처리 =================
# 불필요한 특수문자 제거
text = text.replace('‒', '-').replace('•','').replace('|','')

lines = text.strip().split("\n")
songs = []

for line in lines:
    if "-" in line:
        parts = line.split("-")
        # 타임스탬프 제거: [00:13], 00:13 등 모두 제거
        song_name = re.sub(r"^[\[\d:.]+\]?\s*", "", parts[0]).strip()
        artist_name = parts[1].strip()
        songs.append((song_name, artist_name))

# ================= CSV 저장 =================
csv_file = "playlist_text01.csv"
with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["곡명", "가수"])
    writer.writerows(songs)

# ================= Spotify 플레이리스트 생성 =================
sp_oauth = SpotifyOAuth(
    client_id="323f88c42f274cc7b2c95ada52976578",
    client_secret="34a628667ffa403b9d3871176bfe1325",
    redirect_uri="http://127.0.0.1:8808/callback",
    scope="playlist-modify-public"
)

token_info = sp_oauth.get_cached_token()
if not token_info:
    exit()

sp = Spotify(auth=token_info["access_token"])
user_id = sp.me()["id"]

playlist_name = "평생을 당신의 마음에 들고자 노력하였습니다"
playlist = sp.user_playlist_create(user_id, name=playlist_name, public=True)
playlist_id = playlist["id"]

# ================= Spotify 곡 추가 =================
with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        track_name = row["곡명"].strip()
        artist_name = row["가수"].strip()
        query = f"{track_name} {artist_name}"

        try:
            results = sp.search(q=query, type="track", limit=1)
            tracks = results["tracks"]["items"]
            if tracks:
                track_id = tracks[0]["id"]
                sp.playlist_add_items(playlist_id, [track_id])
                print(f"✅ 추가됨: {track_name} - {artist_name}")
            else:
                print(f"⚠️ 찾을 수 없음: {track_name} - {artist_name}")
        except Exception as e:
            print(f"⚠️ Spotify 오류: {track_name} - {artist_name} -> {e}")

# ================= 완료 =================
print(f"\n🎉 플레이리스트 생성 완료: {playlist['external_urls']['spotify']}")
