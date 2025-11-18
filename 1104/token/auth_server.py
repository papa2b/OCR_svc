from flask import Flask, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)

# 전역 OAuth 객체 (토큰 교환용)
sp_oauth = SpotifyOAuth(
    client_id="323f88c42f274cc7b2c95ada52976578",
    client_secret="34a628667ffa403b9d3871176bfe1325",
    redirect_uri="http://127.0.0.1:8808/callback",
    scope="playlist-modify-public"
)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    error = request.args.get("error")

    if error:
        print(f"❌ 인증 실패: {error}")
        return f"❌ 인증 실패: {error}"

    if not code:
        print("⚠️ code 파라미터 없음")
        return "⚠️ 인증 코드가 전달되지 않았습니다."

    # ✅ code를 access token으로 교환
    print(f"🎟️ 받은 code: {code}")
    token_info = sp_oauth.get_access_token(code)

    if token_info:
        access_token = token_info["access_token"]
        print(f"✅ 액세스 토큰 발급 완료! token: {access_token[:20]}...")  # 앞부분만 출력
        return "✅ Spotify 인증 성공! 터미널에서 토큰 확인 가능."
    else:
        print("❌ 액세스 토큰 발급 실패")
        return "❌ 액세스 토큰 발급에 실패했습니다."

if __name__ == "__main__":
    auth_url = sp_oauth.get_authorize_url()
    print("👇 아래 URL을 브라우저에서 열고 Spotify 로그인 + 허용을 눌러주세요 👇\n")
    print(auth_url)
    print("\n✅ Flask callback 서버가 실행 중입니다...\n")

    app.run(host="0.0.0.0", port=8808)
