#api.spotify_tools.base

#A python file containing constants and pseudo-constants needed for interacting with the Spotify API.
import engine.signal as signal
CLIENT_ID_HREF = "../public/spotify_client_id.txt"
CLIENT_SECRET_HREF = "../secrets/spotify_client_secret.txt"

# idObj = signal.ValueLoader(CLIENT_ID_HREF)
# secretObj = signal.ValueLoader(CLIENT_SECRET_HREF)

# client_id = getattr(idObj, "content")
# client_secret = getattr(secretObj, "content")

client_id = signal.ValueLoader(CLIENT_ID_HREF)
client_secret = signal.ValueLoader(CLIENT_SECRET_HREF)

redirect_uri = "http://127.0.0.1"

authorise_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"