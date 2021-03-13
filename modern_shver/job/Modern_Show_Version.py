# ----------------
# Copywrite
# ----------------
# Written by John Capobianco, March 2021 
# Copyright (c) 2021 John Capobianco

# ----------------
# Python
# ----------------
import sys
import time
import logging
import json
import requests
import base64
from google.cloud import texttospeech

# ----------------
# Jinja2
# ----------------
from jinja2 import Environment, FileSystemLoader
template_dir = '../templates'
env = Environment(loader=FileSystemLoader(template_dir))

# ----------------
# Import pyATS and the pyATS Library
# ----------------
from genie.testbed import load
from pyats.log.utils import banner

# Get logger for script
log = logging.getLogger(__name__)

# ----------------
# Template sources
# ----------------
csv_template = env.get_template('show_version_csv.j2')
md_template = env.get_template('show_version_md.j2')
html_template = env.get_template('show_version_html.j2')
discord_template = env.get_template('show_version_discord.j2')
webex_template = env.get_template('show_version_webex.j2')
slack_template = env.get_template('show_version_slack.j2')
google_tts_eng_template = env.get_template('show_version_google_tts_english.j2')
google_tts_fr_template = env.get_template('show_version_google_tts_fr.j2')
google_tts_greek_template = env.get_template('show_version_google_tts_greek.j2')

# ----------------
# Enable logger
# ----------------
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')
log = logging.getLogger(__name__)

# ----------------
# Load the testbed
# ----------------
log.info(banner("Loading testbed"))
testbed = load('../testbed/3850.yaml')
log.info("\nPASS: Successfully loaded testbed '{}'\n".format(testbed.name))

# --------------------------
# Connect to device 3850
# --------------------------
log.info(banner("Connect to device '3850'"))
device = testbed.devices['3850']
device.connect(via='cli')
log.info("\nPASS: Successfully connected to device '3850'\n")

# ---------------------------------------
# Execute parser to show version
# ---------------------------------------
log.info(banner("Executing parser to get show version and create documentation..."))
parsed_show_version = device.parse("show version")

# ---------------------------------------
# Template Results
# ---------------------------------------
output_from_parsed_csv_template = csv_template.render(to_parse_version=parsed_show_version['version'])
output_from_parsed_md_template = md_template.render(to_parse_version=parsed_show_version['version'])
output_from_parsed_html_template = html_template.render(to_parse_version=parsed_show_version['version'])
output_from_parsed_discord_template = discord_template.render(to_parse_version=parsed_show_version['version'])
output_from_parsed_webex_template = webex_template.render(to_parse_version=parsed_show_version['version'])
output_from_parsed_slack_template = slack_template.render(to_parse_version=parsed_show_version['version'])
output_from_parsed_google_tts_eng_template = google_tts_eng_template.render(to_parse_version=parsed_show_version['version'])
output_from_parsed_google_tts_fr_template = google_tts_fr_template.render(to_parse_version=parsed_show_version['version'])
output_from_parsed_google_tts_greek_template = google_tts_greek_template.render(to_parse_version=parsed_show_version['version'])

# ---------------------------------------
# Create Files
# ---------------------------------------
with open("../output/show_version_csv.csv", "w") as fh:
    fh.write(output_from_parsed_csv_template)

with open("../output/show_version_md.md", "w") as fh:
    fh.write(output_from_parsed_md_template)

with open("../output/show_version_html.html", "w") as fh:
    fh.write(output_from_parsed_html_template)

# ---------------------------------------
# #chatbots 
# ---------------------------------------
discord_response = requests.post('https://discord.com/api/webhooks/{{ your webhook here }}', data=output_from_parsed_discord_template, headers={"Content-Type":"application/json"})
print('The POST to Discord had a response code of ' + str(discord_response.status_code) + 'due to' + discord_response.reason)

webex_response = requests.post('https://webexapis.com/v1/messages', data=output_from_parsed_webex_template, headers={"Content-Type":"application/json", "Authorization": "Bearer {{ your bearer token here }} "})
print('The POST to WebEx had a response code of ' + str(webex_response.status_code) + 'due to' + webex_response.reason)

slack_response = requests.post('https://hooks.slack.com/services/{{ your webhook here }}', data=output_from_parsed_slack_template, headers={"Content-Type":"application/json"})
print('The POST to Slack had a response code of ' + str(slack_response.status_code) + 'due to' + slack_response.reason)

# ---------------------------------------
# #voicebots
# ---------------------------------------

# ----------------
# Instantiates a client
# ----------------
client = texttospeech.TextToSpeechClient()

# ----------------
# Set the text input to be synthesized
# ----------------
google_voice_english_synthesis_input = texttospeech.SynthesisInput(text=output_from_parsed_google_tts_eng_template)
google_voice_french_synthesis_input = texttospeech.SynthesisInput(text=output_from_parsed_google_tts_fr_template)
google_voice_greek_synthesis_input = texttospeech.SynthesisInput(text=output_from_parsed_google_tts_greek_template)


# ----------------
# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
# ----------------
eng_voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

fr_voice = texttospeech.VoiceSelectionParams(
    language_code="fr-CA", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

greek_voice = texttospeech.VoiceSelectionParams(
    language_code="el-GR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# ----------------
# Select the type of audio file you want returned
# ----------------
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# ----------------
# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
# ----------------
eng_response = client.synthesize_speech(
    input=google_voice_english_synthesis_input, voice=eng_voice, audio_config=audio_config
)

fr_response = client.synthesize_speech(
    input=google_voice_french_synthesis_input, voice=fr_voice, audio_config=audio_config
)

greek_response = client.synthesize_speech(
    input=google_voice_greek_synthesis_input, voice=greek_voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("../output/show_version_google_tts_eng.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(eng_response.audio_content)

with open("../output/show_version_google_tts_fr.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(fr_response.audio_content)

with open("../output/show_version_google_tts_greek.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(greek_response.audio_content)    