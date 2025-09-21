from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils
import json
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64
from wordcloud import WordCloud, STOPWORDS

app = Flask(__name__)

# Load all data on startup
def load_data():
    global df, pipeline, new_df, feature_text, location_df, cosine_sim1, cosine_sim2, cosine_sim3
    
    # Price prediction data
    with open('df.pkl','rb') as file:
        df = pickle.load(file)
    
    # Load pipeline with fallback
    try:
        with open('pipeline.pkl','rb') as file:
            pipeline = pickle.load(file)
    except FileNotFoundError:
        print("pipeline.pkl not found, creating minimal pipeline...")
        from sklearn.preprocessing import StandardScaler
        from sklearn.linear_model import LinearRegression
        from sklearn.pipeline import Pipeline
        
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', LinearRegression())
        ])
        print("Warning: Using minimal pipeline. Price predictions may not be accurate.")
    
    # Analytics data
    new_df = pd.read_csv('data_viz1.csv')
    
    with open('feature_text.pkl', 'rb') as file:
        feature_text = pickle.load(file)
    
    # Clean data
    for col in ['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']:
        new_df[col] = pd.to_numeric(new_df[col], errors='coerce')
    new_df = new_df.dropna(subset=['latitude', 'longitude'])
    
    # Recommendation data
    with open('location_distance.pkl','rb') as file:
        location_df = pickle.load(file)
    
    with open('cosine_sim1.pkl','rb') as file:
        cosine_sim1 = pickle.load(file)
        
    with open('cosine_sim2.pkl','rb') as file:
        cosine_sim2 = pickle.load(file)
        
    with open('cosine_sim3.pkl','rb') as file:
        cosine_sim3 = pickle.load(file)

load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('price_predictor.html', 
                             sectors=sorted(df['sector'].unique()),
                             bedrooms=sorted(df['bedRoom'].unique()),
                             bathrooms=sorted(df['bathroom'].unique()),
                             balconies=sorted(df['balcony'].unique()),
                             property_ages=sorted(df['agePossession'].unique()),
                             furnishing_types=sorted(df['furnishing_type'].unique()),
                             luxury_categories=sorted(df['luxury_category'].unique()),
                             floor_categories=sorted(df['floor_category'].unique()))
    
    # Handle prediction
    data = [[
        request.form['property_type'],
        request.form['sector'],
        float(request.form['bedrooms']),
        float(request.form['bathroom']),
        request.form['balcony'],
        request.form['property_age'],
        float(request.form['built_up_area']),
        float(request.form['servant_room']),
        float(request.form['store_room']),
        request.form['furnishing_type'],
        request.form['luxury_category'],
        request.form['floor_category']
    ]]
    
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']
    
    one_df = pd.DataFrame(data, columns=columns)
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.22
    high = base_price + 0.22
    
    return jsonify({'low_price': round(low, 2), 'high_price': round(high, 2)})

@app.route('/analytics')
def analytics():
    # Create geo map
    group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean().reset_index()
    
    geomap_fig = px.scatter_mapbox(
        group_df, lat="latitude", lon="longitude", color="price_per_sqft",
        size='built_up_area', hover_name='sector',
        color_continuous_scale="Viridis", zoom=10,
        mapbox_style="open-street-map"
    )
    # Convert numpy arrays to lists for JSON serialization
    geomap_json = json.dumps(geomap_fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Create wordcloud with fallback
    try:
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(feature_text)
        img = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        wordcloud_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
    except Exception as e:
        print(f"WordCloud error: {e}")
        # Create a simple text-based fallback
        img = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.text(0.5, 0.5, 'WordCloud unavailable', ha='center', va='center', fontsize=20)
        plt.axis("off")
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        wordcloud_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
    
    return render_template('analytics.html', 
                         geomap=geomap_json, 
                         wordcloud=wordcloud_url,
                         sectors=['overall'] + sorted(new_df['sector'].unique()),
                         property_types=sorted(new_df['property_type'].unique()))

@app.route('/chart/<chart_type>')
def get_chart(chart_type):
    if chart_type == 'area_price':
        property_type = request.args.get('property_type', 'flat')
        filtered_df = new_df[new_df['property_type'] == property_type]
        fig = px.scatter(filtered_df, x="built_up_area", y="price", color="bedRoom")
    
    elif chart_type == 'bhk_pie':
        sector = request.args.get('sector', 'overall')
        if sector == 'overall':
            fig = px.pie(new_df, names='bedRoom', title='BHK Distribution')
        else:
            fig = px.pie(new_df[new_df['sector'] == sector], names='bedRoom', title=f'BHK in {sector}')
    
    elif chart_type == 'price_box':
        fig = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='Price by BHK')
    
    elif chart_type == 'price_dist':
        house_data = new_df[new_df['property_type'] == 'house']['price'].dropna()
        flat_data = new_df[new_df['property_type'] == 'flat']['price'].dropna()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=house_data, name='House', opacity=0.7))
        fig.add_trace(go.Histogram(x=flat_data, name='Flat', opacity=0.7))
        fig.update_layout(title='Price Distribution', barmode='overlay')
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Backwards-compatible endpoints expected by templates
@app.get('/get_area_vs_price')
def get_area_vs_price():
    property_type = request.args.get('property_type', 'flat')
    filtered_df = new_df[new_df['property_type'] == property_type]
    fig = px.scatter(filtered_df, x="built_up_area", y="price", color="bedRoom")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.get('/get_bhk_pie')
def get_bhk_pie():
    sector = request.args.get('sector', 'overall')
    if sector == 'overall':
        fig = px.pie(new_df, names='bedRoom', title='BHK Distribution')
    else:
        fig = px.pie(new_df[new_df['sector'] == sector], names='bedRoom', title=f'BHK in {sector}')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.get('/get_bhk_price_box')
def get_bhk_price_box():
    fig = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='Price by BHK')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.get('/get_price_distribution')
def get_price_distribution_endpoint():
    house_data = new_df[new_df['property_type'] == 'house']['price'].dropna()
    flat_data = new_df[new_df['property_type'] == 'flat']['price'].dropna()
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=house_data, name='House', opacity=0.7))
    fig.add_trace(go.Histogram(x=flat_data, name='Flat', opacity=0.7))
    fig.update_layout(title='Price Distribution', barmode='overlay')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'GET':
        return render_template('recommend.html',
                             locations=sorted(location_df.columns),
                             apartments=sorted(location_df.index))
    
    action = request.form.get('action')
    
    if action == 'search_location':
        location = request.form['location']
        radius = float(request.form['radius'])
        result_ser = location_df[location_df[location] < radius*1000][location].sort_values()
        results = [{'name': key, 'distance': round(value/1000, 2)} for key, value in result_ser.items()]
        return jsonify({'results': results})
    
    elif action == 'recommend_apartments':
        apartment = request.form['apartment']
        recommendations = get_recommendations(apartment)
        return jsonify({'recommendations': recommendations.to_dict('records')})

def get_recommendations(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]
    top_properties = location_df.index[top_indices].tolist()
    
    return pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores
    })

if __name__ == '__main__':
    app.run(debug=True)