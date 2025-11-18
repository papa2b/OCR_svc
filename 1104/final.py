import csv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# ===============================
# 1️⃣ Spotify OAuth 설정
# ===============================
sp_oauth = SpotifyOAuth(
    client_id="323f88c42f274cc7b2c95ada52976578",          # 본인 앱 Client ID
    client_secret="34a628667ffa403b9d3871176bfe1325",  # 본인 앱 Client Secret
    redirect_uri="http://127.0.0.1:8808/callback",
    scope="playlist-modify-public"
)

# 캐시된 토큰 가져오기 (없으면 auth_server.py 실행 후 발급)
token_info = sp_oauth.get_cached_token()
if not token_info:
    print("❌ 토큰 없음 또는 만료됨. auth_server.py 실행 후 새 토큰 발급 필요")
    exit()

# Spotipy 객체 생성
sp = Spotify(auth=token_info["access_token"])

# ===============================
# 2️⃣ 내 계정 ID 가져오기
# ===============================
user_id = sp.me()["id"]
print("✅ 사용자 ID:", user_id)

# ===============================
# 3️⃣ 플레이리스트 생성
# ===============================
playlist_name = "평생을 당신의 마음에 들고자 노력하였습니다"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
playlist_id = playlist["id"]
print(f"✅ 플레이리스트 생성: {playlist['external_urls']['spotify']}")

# ===============================
# 4️⃣ CSV에서 곡명과 가수 읽고 검색/추가
# ===============================
with open("1104/playlist_text.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        track_name = row["곡명"].strip()
        artist_name = row["가수"].strip()
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
