from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import discord
from discord.ext import commands

load_dotenv()


"""
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
*                                                                   *
*                           *** TO-DO ***                           *
*                                                                   *
*    - Add Discord features                                         *
*    - Allow users to pick an artist and play their top n songs     *
*    - Pick specific songs based on title                           *
*        - Return top 5 results from song name search               *
*            - Allow them to respond with 1-5 to pick the songs     *
*           - The menu will show song name & artist                 *
*    - Maybe play a playlist so they don't have to chose songs      *
*      when one ends?                                               *
*                                                                   *
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
"""


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
bot_token = os.getenv("BOT_TOKEN")

# print(client_id, client_secret) - DEBUG

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)


# Bot Development


def getToken():  # Gets & Encodes Spotify Token
    authString = client_id + ":" + client_secret
    authBytes = authString.encode("utf-8")
    authBase64 = str(base64.b64encode(authBytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + authBase64,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    jsonResult = json.loads(result.content)
    token = jsonResult["access_token"]
    return token


def getAuthHeader(token):
    return {"Authorization": "Bearer " + token}


def searchForArtist(token, artistName):
    url = "https://api.spotify.com/v1/search"
    headers = getAuthHeader(token)
    query = f"?q={artistName}&type=artist&limit=1"

    queryURL = url + query
    result = get(queryURL, headers=headers)

    jsonResult = json.loads(result.content)["artists"]["items"]

    if len(jsonResult) == 0:
        print("Artist not found!")
        return None

    return jsonResult[0]


@bot.command()
async def search_artist_songs(ctx, *, artist_name):
    token = getToken()  # Get Spotify token

    artist_data = searchForArtist(token, artist_name)  # Use the token

    if artist_data is None:
        await ctx.send("Artist not found!")
        return

    artist_id = artist_data["id"]
    top_tracks_url = (
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    )

    headers = getAuthHeader(token)  # Pass the token
    top_tracks_response = get(top_tracks_url, headers=headers)  # Use get method
    top_tracks_data = top_tracks_response.json()["tracks"][:5]

    track_options = []
    for idx, track in enumerate(top_tracks_data, start=1):
        track_options.append(f"{idx}. {track['name']}")

    response = f"Top 5 tracks for {artist_name}:\n"
    response += "\n".join(track_options)
    response += "\n\nPlease select a track by typing its number."

    await ctx.send(response)

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        user_input = await bot.wait_for("message", check=check, timeout=30)
        choice = int(user_input.content)

        if 1 <= choice <= 5:
            selected_track = top_tracks_data[choice - 1]
            track_name = selected_track["name"]
            track_uri = selected_track["uri"]

            await ctx.send(f"Now playing: {track_name}")
            await ctx.send(
                f"Listen to the track: https://open.spotify.com/track/{track_uri.split(':')[2]}"
            )
        else:
            await ctx.send("Invalid choice. Please select a number between 1 and 5.")
    except ValueError:
        await ctx.send("Invalid input. Please enter a number.")


# token = getToken()
# result = searchForArtist(token, "Drake")
# artistID = result["id"]
# print(token) - DEBUG
# print(result["name"])


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


## RUNS BOT DO NOT DELETE
bot.run(bot_token)
