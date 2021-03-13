# Modern_Show_Version

Cisco IOS-XE Show Version Command Reimagined as a pyATS job that creates CSV / MD / HTML; sends #chatbot messages; and generates MP3 using Google Cloud TTS #voice

## Simply a better way to run the show version command on IOS-XE Devices

Install pyATS

```console
pip install pyats[full]
```

Update the testbed file to reflect your devices. The example uses a 3850

Ensure SSH connectivity and run the pyATS job

```console
pyats run job Modern_Show_Version_job.py --testbed-file ../testbed/3850.yaml
```

### #chatbots and #voicebots

#### WebEx #chatbot

Follow these guides to setup your bot

Cisco WebEx REST API Basics

<https://developer.webex.com/docs/api/basics>

Cisco WebEx Webhooks

<https://developer.webex.com/docs/api/guides/webhooks>

Practically Speaking; Login to the WebEx Developer Portal with your Cisco DevNet or CCO Account

<https://developer.webex.com/my-apps>

Create an Application

Then test the application using the following portals in your browser

First get the list of WebEx Teams you are a part of

<https://developer.webex.com/docs/api/v1/teams>

Then get the Rooms that in these Teams

<https://developer.webex.com/docs/api/v1/rooms>

Finally you can explore the messages in that room, including how to POST a message

<https://developer.webex.com/docs/api/v1/messages>

To see all current messages you can also use

<https://developer.webex.com/docs/api/v1/messages/list-messages>

Make sure you modify the following lines of code

In the Python

webex_response = requests.post('https://webexapis.com/v1/messages', data=output_from_parsed_webex_template, headers={"Content-Type":"application/json", "Authorization": "Bearer {{ your bearer token here }} "})

Replace the {{ your bearer token here }} with your API token from the Bot or your account

In the Jinja2 template also update your roomId

{
  "roomId": "{{ your room ID here }}",
  "text": "This is being sent from pyATS..."
}

#### Discord #chatbot

Follow this guide to setup your bot

Setup a Discord Application and create a Webhook

<https://discord.com/developers/applications>

Replace the Webhook in this line of code with your Discord Webhook

discord_response = requests.post('<https://discord.com/api/webhooks/>{{ your webhook here }}', data=output_from_parsed_discord_template, headers={"Content-Type":"application/json"})

Discord Developer Portal

<https://discord.com/developers/docs/intro>

Discord Webhook Reference

<https://discord.com/developers/docs/resources/webhook>

#### Slack #chatbot

Follow this guide to setup your Slackbot

First configure your Slack App

<https://api.slack.com/apps?new_app=1>

Follow the Slack Webhook guide

<https://api.slack.com/messaging/webhooks>

In the Python update the following line

slack_response = requests.post('<https://hooks.slack.com/services/>{{ your webhook here }}', data=output_from_parsed_slack_template, headers={"Content-Type":"application/json"})

Replacing {{ your webhook here }} with your Slackbot Webhook

#### Google Cloud Text-to-Speech (TTS) #voicebot

Follow the brief introduction guide to the TTS service

<https://cloud.google.com/text-to-speech>

Go to your Google Cloud Console and configure the service.

<https://console.cloud.google.com/>

For this to work you need to setup what is called a Service Account under the API Credentials sub-menu.

<https://cloud.google.com/iam/docs/creating-managing-service-account-keys>

<https://cloud.google.com/iam/docs/service-accounts?_ga=2.180954017.-780071125.1615085699>

Generate a key under your service account which will automatically down a JSON file.

You need to save this JSON file somewhere on the host running the Python and set the following environment variable

```console
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```

##### Output Files

Review your output files. You should have 3 files in the output folder:

Text files:
show_version_csv.csv
show_version_md.md
show_version_html.html

Audio files - generated from a real 3850 using a fictitious hostname and serial number (everything else is real information):
show_version_google_tts_eng.mp3
show_version_google_tts_fr.mp3
show_version_google_tts_greek.mp3