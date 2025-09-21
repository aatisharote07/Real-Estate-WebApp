# Real Estate App - Full Version

This folder contains the complete version of the Real Estate App with all original pickle files and data.

## Contents:
- `app.py` - Original Flask application with full functionality
- `templates/` - HTML templates
- `*.pkl` - All pickle files including the large pipeline.pkl (146MB)
- `data_viz1.csv` - Analytics data
- `requirements.txt` - Python dependencies
- `Readme.md` - Original README

## Usage:
This version is designed for local development or deployment on platforms that support large files (like AWS, Google Cloud, or Heroku with large dynos).

## To run locally:
```bash
pip install -r requirements.txt
python app.py
```

## Note:
This version cannot be deployed to Vercel due to the 250MB serverless function size limit. The main project folder contains a Vercel-optimized version with sample data.
