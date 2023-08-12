# spotify-bot

## What I was Hoping For

When setting this up, I was hoping to mimic other music bots that are regularly used in Disocrd. Unfortunately, the the
Spotify API does not allow that. I was disappointed that the bot only sends a preview of a song in chat, whereas other bots
will join a voice channel and play the full song. 

## How it works

The bot will listen for a specific command & user input. Once the command is made, it will request the artists top 5 songs from 
Spotify and allow the user to chose from their top 5 most popular. The user will be prompted to enter 1-5, and based on this entry, 
the bot will then send a preview of the song in chat. 

## Commands

!search_artist_songs 
