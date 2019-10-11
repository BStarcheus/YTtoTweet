gcloud projects create yttotweet

gcloud config set project yttotweet

gcloud services enable youtube.googleapis.com
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable datastore.googleapis.com
gcloud services enable pubsub.googleapis.com


echo "Before running setup2.sh, setup billing in your GCP Console."
