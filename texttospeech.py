import gtts
import playsound

text="heelo hiiii"
sound=gtts.gTTS(text,lang='en')
sound.save("hey.mp3")
playsound.playsound("hey.mp3")


