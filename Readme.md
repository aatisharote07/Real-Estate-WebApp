# Real Estate Analytics   App

A modern, responsive Flask web application for real estate analytics in Gurgaon with price prediction, market analysis, and property recommendations.

## Features

- **Price Predictor**: ML-powered property price estimation
- **Analytics Dashboard**: Interactive charts and maps for market insights
- **Property Recommendations**: Location-based search and similarity recommendations
 

## Setup Instructions

### 1. Create Project Structure

Create the following folder structure:

```
real-estate-flask-app/
│
├── app.py
├── requirements.txt
├── README.md
│
└── templates/
    ├── base.html
    ├── index.html
    ├── predict.html
    ├── analytics.html
    └── recommend.html
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Your Data Files

Ensure you have the following files in their original paths (as used in your Streamlit app):

- `C:\Users\Admin\OneDrive\Documents\Real Estate Analytics Web App\real-estate-app\pages\df.pkl`
- `C:\Users\Admin\OneDrive\Documents\Real Estate Analytics Web App\real-estate-app\pages\pipeline.pkl`
 
 
- `C:\Users\Admin\OneDrive\Documents\Real Estate Analytics Web App\real-estate-app\datasets\cosine_sim1.pkl`
- `C:\Users\Admin\OneDrive\Documents\Real Estate Analytics Web App\real-estate-app\datasets\cosine_sim2.pkl`
- `C:\Users\Admin\OneDrive\Documents\Real Estate Analytics Web App\real-estate-app\datasets\cosine_sim3.pkl`

### 4. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Application Pages

### 1. Home (`/`)
- Welcome page with feature overview
- Navigation to different sections

### 2. Price Predictor (`/predict`)
- Interactive form for property details
- Real-time price prediction using ML model
- Responsive design with form validation

### 3. Analytics Dashboard (`/analytics`)
- Interactive geo-map of price per sqft by sector
- Features wordcloud
- Area vs price scatter plots
- BHK distribution pie charts
- Price distribution histograms
- Dynamic filtering and real-time updates

### 4. Recommendations (`/recommend`)
- Location-based property search within radius
- Similarity-based property recommendations
- Interactive forms with AJAX responses

## Key Improvements Over Streamlit

- **Better Performance**: Cached data loading and optimized queries
- **Modern UI**: Custom CSS with gradients, shadows, and animations
- **Responsive Design**: Works perfectly on mobile and desktop
- **Interactive Elements**: AJAX forms, loading spinners, smooth transitions
- **Professional Layout**: Card-based design with consistent styling
 

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Plotly.js for interactive visualizations
- **ML Libraries**: scikit-learn, pandas, numpy
- **Visualization**: matplotlib, seaborn, wordcloud

## Browser Compatibility

- Chrome (recommended)
- Safari
- Brave

## Notes

- All file paths are kept exactly as they were in your original Streamlit app
- The app loads all models and data on startup for better performance
- Interactive charts update dynamically without page refresh
 
