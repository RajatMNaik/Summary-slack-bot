#include .env


build-local:
	docker build -t slack-summary-bot:latest .


run-local-docker:
	docker run -d --platform linux/amd64 --name="slack-summary-bot" \
	-e SLACK_BOT_TOKEN=${SLACK_BOT_TOKEN} \
	-e SLACK_APP_TOKEN=${SLACK_APP_TOKEN} \
	-e OPENAI_API_KEY=${OPENAI_API_KEY} \
	slack-summary-bot


clean:
	docker stop slack-summary-bot
	docker rm slack-summary-bot


