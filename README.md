## SummaryBot - Slack Video Summarization App
SummaryBot is a Slack integration that leverages OpenAI's Whisper API to automatically generate accurate and concise summaries of video content shared within Slack channels. This tool is designed to enhance productivity and knowledge sharing by providing quick summaries of meetings, presentations, and any other video content. It's currently in an experimental stage and is not yet a fully featured product.

### Configuration
To run SummaryBot, you need to set the following environment variables:


| Name             | Description                                           | Required | Default |   |
|------------------|-------------------------------------------------------|----------|---------|---|
| OPENAI_API_KEY   | OpenAI API key                                        | yes      |         |   |
| SLACK_BOT_TOKEN  | Slack Bot User Oauth Token                            | yes      |         |   |
| SLACK_APP_TOKEN  | Slack Signing Secret                                  | yes      |         |   |

### Usage
Add SummaryBot to a Slack Channel:
Navigate to Slack Integrations.
Search for SummaryBot and select "Add to Channel" to integrate it into your desired channel.
Using SummaryBot:
Simply upload a video file to any channel where SummaryBot has been added.
SummaryBot will process the video and post a concise summary directly in the same channel.

### Persistence
SummaryBot utilizes a lightweight approach to manage data persistence required for processing and summarizing videos. The specifics of data handling and storage will depend on your configuration and deployment setup:

Local Storage: If running locally or on a single server, video processing data may be temporarily stored on disk.
Containerized Environments: For containerized deployments, ensure that storage is managed appropriately to persist necessary data across container lifecycles.

### Slack App Installation
To install SummaryBot into your Slack workspace, follow these manual setup steps:

1. Go to your Slack organization's admin area and navigate to Slack API.
2. Click "Create New App" and choose "From an app manifest".
3. Select the workspace where you wish to install SummaryBot.
4. Ensure the "YAML" tab is selected, then copy the contents of slack-summarybot-manifest.yaml from this repo into the text area and select create.
5. Generate an app token as per the instructions and export it to your required environment variable.
6. Under "Basic Information", install the app to your workspace.
7. Obtain the Bot User OAuth Token from the "OAuth & Permissions" tab and set it as an environment variable.

### Local Development
To run SummaryBot locally for development or testing:

You can run the app locally following these steps.
Create an `.env` file and define the environment variables described in the Configuration section below.
build docker image
```commandline
make build-local
```
run docker image
```commandline
make run-local
```


