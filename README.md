# Simple URL Shortener

A simple URL Shortener backend built using Python Flask and SQLite.

## Features

- Accepts long URLs
- Generates a unique short code
- Stores URLs in SQLite database
- Redirects short URLs to the original URL
- REST API endpoint for creating short URLs

## Technologies Used

- Python
- Flask
- SQLite
- REST API

## API Endpoint

### Create Short URL

**POST** `/shorten`

Request:

```json
{
  "url": "https://www.google.com"
}
