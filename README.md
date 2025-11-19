# Automated-feature-generation-selection-and-prediction-Model
The Automated Feature Generation and Selection Model uses the Bot-IoT dataset to improve intrusion detection by automating key steps of feature engineering.
  
A fully automated ML pipeline for training, evaluating, and deploying a prediction model on the UNSW (UNSW_2018_IoT_Botnet_Final_10_B.csv)dataset.

This project includes:
- Automated dataset download using a secure GitHub Actions secret  
- Automated training pipeline (RandomForestClassifier)  
- Automated testing  
- Model packaging with joblib  
- Flask API for real-time predictions  
- Docker image build with Gunicorn  
  
# Project Features
1. Automated ML Training  
- Cleans dataset  
- Encodes categorical fields (e.g., `proto`)  
- Removes high-cardinality fields like IP addresses  
- Selects stable numerical features  
- Trains a Random Forest model  
- Saves trained model & encoders → `models/model.joblib`

2. CI/CD with GitHub Actions  
Pipeline automatically:
1. Downloads dataset from a secure Google Drive link  
2. Trains the model  
3. Runs tests (`pytest`)  
4. Builds a Docker image  
  
5. REST API using Flask  
- Endpoint: `/predict`  
- Accepts JSON input for the model  
- Returns prediction (`0 = benign`, `1 = attack`)  
- Returns confidence score (probability)

6. Dockerized Deployment  
- Production server runs via Gunicorn  
- Ready for deployment to **Render**, **Railway**, **Azure WebApps**, **AWS ECS**, etc.





