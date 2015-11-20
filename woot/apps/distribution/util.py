# apps.distribution.util

# django
from django.apps import apps
from django.conf import settings

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

  Obj = apps.get_model(app_label=app_name, model_name=obj_name)

  def get_id_token():
    return random_string()

  id_token = get_id_token()
  while Obj.objects.filter(id_token=id_token).count()>0:
    id_token = get_id_token()

  return id_token

def random_string():
  return ''.join([random.choice(chars) for _ in range(8)]) #8 character string

### CONTROLS ###
def process_audio(input_path):
  # convert a-law wav file to microsoft pcm wav file
  temp_path = os.path.join(os.path.dirname(input_path), 'temp')
  if not os.path.exists(temp_path):
    os.makedirs(temp_path)

  temp = os.path.join(temp_path, os.path.basename(input_path))

  cmd = '../bin/ffmpeg -y -i {} -f wav {} 2> /dev/null'.format(input_path, temp)
  call(cmd, shell=True)

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
    r = audioop.rms(section, settings.AUDIO_SAMPLE_WIDTH)
    rmsValues.append(r)

  # all the truncated time adds up.
  # we therefore read the last audio section to the end of the file,
  # rather than to an integer number of frames.
  last = nFrames - count
  section = a.readframes(last)
  r = audioop.rms(section, settings.AUDIO_SAMPLE_WIDTH)
  rmsValues.append(r)

  return seconds, rmsValues
