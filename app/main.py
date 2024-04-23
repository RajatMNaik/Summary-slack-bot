import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from moviepy.editor import AudioFileClip
import openai
import requests
import threading
from tempfile import NamedTemporaryFile
from healthcheck import http_server

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN'] 
OPENAI_API_KEY  = os.environ['OPENAI_API_KEY'] 

app = App(token=os.getenv("SLACK_BOT_TOKEN"))
openai.api_key = os.getenv('OPENAI_API_KEY')

def download_file_from_slack(url, headers):
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
            for chunk in r.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            return tmp_file.name

def convert_and_split_mp4(audio_file_path, segment_length=15):
    audio_clip = AudioFileClip(audio_file_path)
    duration = audio_clip.duration
    segments = []

    for start in range(0, int(duration), segment_length):
        end = min(start + segment_length, int(duration))
        segment_path = f"{audio_file_path}_{start}_{end}.wav"
        audio_clip.subclip(start, end).write_audiofile(segment_path, codec='pcm_s16le')
        segments.append(segment_path)

    audio_clip.close()
    return segments

def transcribe_and_summarize(audio_file_path):
    segments = convert_and_split_mp4(audio_file_path)
    full_transcript = ""

    for segment in segments:
        with open(segment, "rb") as audio_file:
            transcript_response = openai.Audio.transcribe(model="whisper-1", file=audio_file, response_format="text")
            transcript = transcript_response.get("text", "") if isinstance(transcript_response, dict) else transcript_response
            full_transcript += transcript + " "
        os.remove(segment)

    summary_response = openai.ChatCompletion.create(
    model="gpt-4-0125-preview",
    messages=[
        {
            "role": "system",
            "content": ("For this task, assume the role of a professional meeting summarizer with extensive experience at leading Tech companies like Meta, OpenAI, and Google. "
                        "You have transcribed meetings for leaders across various functions such as Marketing, Product, Engineering, Legal, and Strategy. "
                        "You are renowned for your communication and writing skills, having mastered techniques from books like 'Crucial Conversations' by Kerry Patterson, 'Simply Said' by Jay Sullivan, 'Words That Work' by Dr. Frank Luntz, 'The Fine Art of Small Talk' by Debra Fine, and 'Communication Skills Training' by Ian Tuhovsky. "
                        "Your task is to analyze a provided meeting transcript transcribed through OpenAI’s Whisper API, write a summary that clearly outlines the key discussions and create a to-do list based on the transcript. "
                        "The summary should be formatted as plain text without the use of markdown syntax like asterisks or hash symbols for headings and bold text. Ensure there is a clear space between each section for readability. "
                        "Summarize the meeting and next steps in a general way without allocating names.")
        },
        {
            "role": "user",
            "content": "Please summarize this transcript and highlight the key takeaways and next steps, without allocating names."
        },
        {
            "role": "assistant",
            "content": f"Transcript:\n{full_transcript}"
        }
    ],

    max_tokens=1000,
    temperature=0.5
)
    return summary_response['choices'][0]['message']['content']


@app.event("file_shared")
def handle_file_shared(event, say, logger, client):
    file_id = event['file']['id']
    try:
        
        result = client.files_info(file=file_id)
        file_info = result['file']
        if file_info['mimetype'].startswith('video/'):
            
            url = file_info['url_private']
            headers = {'Authorization': f'Bearer {os.getenv("SLACK_BOT_TOKEN")}'}
            video_path = download_file_from_slack(url, headers)

            
            summary = transcribe_and_summarize(video_path)

           
            os.remove(video_path)

            
            channel_id = file_info['channels'][0] if file_info['channels'] else file_info['groups'][0] if file_info['groups'] else file_info['ims'][0]
            client.chat_postMessage(channel=channel_id, text=summary)
        
    except Exception as e:
        logger.error(f"Error processing shared file: {e}")
def start_slack_app():
    SocketModeHandler(app, SLACK_APP_TOKEN).start()

if __name__ == "__main__":

    # we need to provide a liveness endpoint for Kubernetes,
    # so we start a simple HTTP server in a separate thread from the Slack app
    http_server_port = 3000
    http_server_port = 3000
    http_server_thread = threading.Thread(target=http_server, args=(http_server_port,))
    slack_app_thread = threading.Thread(target=start_slack_app)

    # Start both threads concurrently
    slack_app_thread.start()
    http_server_thread.start()

    # Wait for both threads to finish
    http_server_thread.join()
    slack_app_thread.join()
