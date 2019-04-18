```
docker build --tag stormbot .
docker run --device /dev/snd -e AUDIODEV=hw:1,0 -v /var/cache/stormbot/:/var/cache/stormbot/ -v ~/Music:/app/Music/ stormbot --jid $jid $room --plugins stormbot_fortune.fortune,stormbot_music.music,stormbot_quote.quote,stormbot_quizz.quizz,stormbot_say.say --music-player play --music-path Music/ --music-default $music_default
```