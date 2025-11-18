from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

sp_oauth = SpotifyOAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://127.0.0.1:8808/callback",
    scope="playlist-modify-public"
)

token_info = sp_oauth.get_cached_token()
if not token_info:
    print("❌ 토큰 없음 또는 만료됨")
    exit()

sp = Spotify(auth=token_info["access_token"])
user_id = sp.me()["id"]
print("✅ 사용자 ID:", user_id)

