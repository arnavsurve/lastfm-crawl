# LastFM - Crawl

This is a wrapper for the LastFM API serving JSON to provide a customizable way to embed LastFM data into an application. Written in Python using Flask, contained in Docker, hosted on AWS Lambda.

## Usage

### Docker

To run the application locally or deploy on a server, you can use Docker. The following command will build the image and run the container:

```bash
docker build -t lastfm-crawl .
docker run -p 5000:5000 lastfm-crawl
```

### Environment Variables

The following environment variables are required and should be set in `config.json`:

```json
{
    "lastfm_api_key": "LASTFM_API_KEY",
    "lastfm_api_secret": "LASTFM_API_SECRET",
    "password": "Last.fm USER PASSWORD"
}
```

`config.json` is gitignored by default and should be created in the root directory of the project.

The last.fm username is hardcoded in the `app.py` file. Please change it to your own username corresponding to the password in config.json.

### API

The API has the following endpoints:

- `/` - Returns a confirmation message indicating the server is running.
- `/recent-tracks` - Returns the most recent tracks listened to by the user. Takes a parameter `username` which is the username of the target LastFM user to query. An optional parameter `number` can be passed to define the number of tracks returned, by default returns the most recent 10 tracks.
- `/top-tracks` - Returns the top tracks listened to by the user. Takes a parameter `username` which is the username of the target LastFM user to query. An optional parameter `number` can be passed to define the number of tracks returned, by default returns the top 10 tracks.
