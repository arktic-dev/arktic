# apps.dstr.util

# django
from django.db import models

# util
import random
import string
import wave
import audioop
import os
import shutil
from subprocess import call

# vars
chars = string.ascii_uppercase + string.digits

# methods
def generate_id_token(app_name, obj_name):

  Obj = models.get_model(app_name, obj_name)

  def get_id_token():
    return random_string()

  id_token = get_id_token()
  while Obj.objects.filter(id_token=id_token).count()>0:
    id_token = get_id_token()

  return id_token

def random_string():
  return ''.join([random.choice(chars) for _ in range(8)]) #8 character string

### CONTROLS ###
sampleWidth = 2 # number of bytes in a frame.
  # for microsoft 16-bit PCM wav, this is 2.

def process_audio(input_path):
  # convert a-law wav file to microsoft pcm wav file
  temp = os.path.join(os.path.basename(input_path), 'temp', input_path)
  cmd = ['ffmpeg','-y','-i',input_path,'-f','wav',temp, '>/dev/null', '2>/dev/null']
  call(cmd)

  # get properties of the pcm wav file
  seconds, rmsValues = getWAVFileProperties(temp)

  # remove temporary audio file
  os.remove(temp)

  return (seconds, rmsValues)

def getWAVFileProperties(filePath):

  a = wave.open(filePath, 'r')
  nFrames = a.getnframes()
  framerate = a.getframerate()
  seconds = nFrames / float(framerate)

  # get rms value for each section of the audio
  framesPerSection = int(nFrames / float(settings.NUMBER_OF_AUDIO_FILE_BINS)) # note the truncation
  rmsValues = []
  count = 0
  for i in range(settings.NUMBER_OF_AUDIO_FILE_BINS-1):
    section = a.readframes(framesPerSection)
    count += framesPerSection
    r = audioop.rms(section, sampleWidth)
    rmsValues.append(r)

  # all the truncated time adds up.
  # we therefore read the last audio section to the end of the file,
  # rather than to an integer number of frames.
  last = nFrames - count
  section = a.readframes(last)
  r = audioop.rms(section, sampleWidth)
  rmsValues.append(r)

  return seconds, rmsValues
