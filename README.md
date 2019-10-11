# YTtoTweet
Automatically Tweet when your YouTube channel gets new uploads.


## How it works

Every 4 hours (or less if you change the scheduler timing), the service will run and check if there was a new upload since its last run.

For each new upload it will Tweet for you in the order that the videos were published.

Note: When running for the first time, it only checks for uploads in the last 24 hours.


## Requirements

To run this service you must have:

1. A Google Cloud Account

2. Google Cloud SDK
    - [Installed](https://cloud.google.com/sdk/docs/quickstarts)
    - Initialized with:   
    `gcloud init`

3. A Twitter Developer Account

## Setup

- Run setup1.sh  
`sh setup1.sh`

- Setup billing for the new project in the GCP Console

- [Get a YouTube Data API Developer Key](https://developers.google.com/youtube/registering_an_application#console_public_api_keys)

- [Get a Twitter API Consumer Key, Consumer Secret, Access Token Key, and Access Token Secret](https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens)

- Insert your Keys into the correct variables at the top of main.py

- [Get your YouTube Channel ID](https://support.google.com/youtube/answer/3250431?hl=en) and insert it into the correct variable at the top of main.py

- Run setup2.sh  
`sh setup2.sh`

The service is deployed! If you upload a new video, you'll get an automated Tweet in at most 4 hours (or less if you change the scheduler timing).
