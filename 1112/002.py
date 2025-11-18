#OCR 정확도 문제. 'pytesseract'가 화면 글자 자체를 잘못 인식함. 이미지 전처리 전에 모델 자체를
#바꾸어 보았습니다. 

import easyocr  # pytesseract 대신
import re
from PIL import Image
import csv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# ================= OCR =================
reader = easyocr.Reader(['ko', 'en'])
results = reader.readtext('1112/ocr02.png')

# easyocr 결과에서 텍스트만 추출하고 줄바꿈
text = "\n".join([res[1] for res in results])

lines = text.strip().split("\n")
songs = []

for line in lines:
    if "-" in line:
        parts = line.split("-")
        # 00:13 타임스탬프 제거
        song_name = re.sub(r"^\[?\d{2}:\d{2}\]?\s*", "", parts[0]).strip()
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

with open(csv_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        track_name = row["곡명"].strip()
        artist_name = row["가수"].strip()
        query = f"{track_name} {artist_name}"

        results = sp.search(q=query, type="track", limit=1)
        tracks = results["tracks"]["items"]

        if tracks:
            track_id = tracks[0]["id"]
            sp.playlist_add_items(playlist_id, [track_id])
            print(f"✅ 추가됨: {track_name} - {artist_name}")
        else:
            print(f"⚠️ 찾을 수 없음: {track_name} - {artist_name}")

# ===============================
print(f"\n🎉 플레이리스트 생성 완료: {playlist['external_urls']['spotify']}")
