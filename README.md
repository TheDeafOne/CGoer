# About CGoer
At Grove City College, we're required to either go to chapel or "make up" missed chapels by watching a recorded chapel and write an essay about it. \
I don't want to go to chapel, but I also don't want to watch a bunch of videos and write a bunch of essays. To avoid this I've created a bot called CGoer which takes the following process:
* grabs live stream link from the user (GCC uses livestream.com to keep records on chapels)
* downloads m3u8 files via reverse engineered API calls
* converts the video to mp3 and transcribes it
* uses chatGPT to summarize the transcription from the perspective of a student listening
* outputs the summary


