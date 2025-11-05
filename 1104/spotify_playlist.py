import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="323f88c42f274cc7b2c95ada52976578",
    client_secret="34a628667ffa403b9d3871176bfe1325",
    redirect_uri="https://61.109.239.120:8888/callback",
    scope="playlist-modify-public"
))

user_id = sp.me()["id"]

playlist_name = "평생을 당신의 마음에 들고자 노력하였습니다"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
playlist_id = playlist["id"]

# CSV 파일에서 곡명, 가수 읽기
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
            print(f"추가됨: {track_name} - {artist_name}")
        else:
            print(f"찾을 수 없음: {track_name} - {artist_name}")

print(f"\n🎵 플레이리스트 생성 완료: {playlist['external_urls']['spotify']}")
