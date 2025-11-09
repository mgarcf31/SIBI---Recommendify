# app/auth.py
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SCOPES = "user-top-read user-read-recently-played playlist-read-private"

def _oauth(uid: str) -> SpotifyOAuth:
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI", "https://localhost:8000/auth/callback"),
        scope=SCOPES,
        cache_path=f".cache-{uid}",
        show_dialog=True
    )

def get_authorize_url(uid: str) -> str:
    return _oauth(uid).get_authorize_url(state=uid)

def handle_callback(state: str, code: str):
    return _oauth(state).get_access_token(code, check_cache=False)

def sp_client(uid: str) -> spotipy.Spotify:
    so = _oauth(uid)
    token_info = so.get_cached_token()
    if not token_info:
        raise RuntimeError("No hay token. Abre /login/{uid} primero.")
    if so.is_token_expired(token_info):
        token_info = so.refresh_access_token(token_info["refresh_token"])
    return spotipy.Spotify(auth=token_info["access_token"])
