gcloud services enable cloudscheduler.googleapis.com

gcloud app create

gcloud pubsub topics create checkYT

gcloud pubsub subscriptions create checkYT-sub --topic checkYT

gcloud scheduler jobs create pubsub checkYT --schedule="0 */4 * * *" --topic=checkYT --message-body="Checking YT"

gcloud functions deploy checkYT --runtime python37 --trigger-topic checkYT
