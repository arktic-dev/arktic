# util
import random
import string
import wave
import audioop
import os
import shutil
from subprocess import call

input_path = 'data/20150729163126x12425.wav'

def process_audio(input_path):
  # convert a-law wav file to microsoft pcm wav file
  temp_path = os.path.join(os.path.dirname(input_path), 'temp')
  if not os.path.exists(temp_path):
    os.mkdir(temp_path)

  temp = os.path.join(temp_path, os.path.basename(input_path))

  cmd = 'ffmpeg -y -i {} -f wav {} 2> /dev/null'.format(input_path, temp)
  call(cmd, shell=True)

  # get properties of the pcm wav file
  seconds, rmsValues = getWAVFileProperties(temp)
  # seconds, rmsValues = getWAVFileProperties(input_path)

  # remove temporary audio file
  os.remove(temp)

  return (seconds, rmsValues)

def getWAVFileProperties(filePath):

  a = wave.open(filePath, 'r')
  nFrames = a.getnframes()
  framerate = a.getframerate()
  seconds = nFrames / float(framerate)

  # get rms value for each section of the audio
  framesPerSection = int(nFrames / float(100)) # note the truncation
  rmsValues = []
  count = 0
  for i in range(100-1):
    section = a.readframes(framesPerSection)
    count += framesPerSection
    r = audioop.rms(section, 2)
    rmsValues.append(r)

  # all the truncated time adds up.
  # we therefore read the last audio section to the end of the file,
  # rather than to an integer number of frames.
  last = nFrames - count
  section = a.readframes(last)
  r = audioop.rms(section, 2)
  rmsValues.append(r)

  return seconds, rmsValues

(s,n) = process_audio(input_path)
print(s,n)
