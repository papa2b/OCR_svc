import csv
import spotipy

# ===============================
# 1️⃣ 방금 발급받은 액세스 토큰
# ===============================
ACCESS_TOKEN = "BQAr1atcVTbB-EkPxYkg..."  # 터미널에서 받은 토큰 전체 붙여넣기

# Spotipy 객체 생성 (토큰 직접 사용)
sp = spotipy.Spotify(auth=ACCESS_TOKEN)

# ===============================
# 2️⃣ 내 계정 ID 가져오기
# ===============================
user_id = sp.me()["id"]

# ===============================
# 3️⃣ 플레이리스트 생성
# ===============================
playlist_name = "평생을 당신의 마음에 들고자 노력하였습니다"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
playlist_id = playlist["id"]

# ===============================
# 4️⃣ CSV에서 곡명과 가수 읽기
# ===============================
with open("playlist_text.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        track_name = row["곡명"]
        artist_name = row["가수"]
        query = f"{track_name} {artist_name}"

        # Spotify에서 곡 검색
        results = sp.search(q=query, type="track", limit=1)
        tracks = results["tracks"]["items"]
        if tracks:
            track_id = tracks[0]["id"]
            sp.playlist_add_items(playlist_id, [track_id])
            print(f"✅ 추가됨: {track_name} - {artist_name}")
        else:
            print(f"⚠️ 찾을 수 없음: {track_name} - {artist_name}")

# ===============================
# 5️⃣ 완료 후 플레이리스트 URL 출력
# ===============================
print(f"\n🎉 플레이리스트 생성 완료: {playlist['external_urls']['spotify']}")
