
# Diabetes Prediction Web App 🩺💻

## Project Overview 🌟

This project is a comprehensive diabetes prediction web application that uses a logistic regression model to differentiate between diabetic and non-diabetic patients. Additionally, it integrates Google's Gemini model to review patient data and diagnoses, allowing users to chat with an AI doctor and generate detailed reports. 🤖📊

## Features 🛠️

1. **Patient Data Input**: Users can input patient data, and the AI doctor will review and provide feedback. 🏥💬
2. **Data Validation**: If the patient parameters are absurd, the AI doctor will suggest the correct ranges. ✅🔍
3. **AI Doctor Chat**: Users can chat with the AI doctor for insights and reviews. 🩺🗨️
4. **Generate Report**: Users can generate a report that includes patient data, diagnosis, and the AI doctor's review. 📈📝
5. **Stop Typing**: A stop button allows users to halt the AI doctor's typing if it becomes too lengthy. ⏹️
6. **Future Enhancements**:
    - User login functionality. 🔐
    - Photo upload for more detailed reports. 📸

## Project Structure 📂

```
Diabetes_project/
├── AI_Service/
│   └── doctor_response.py
├── Backend/
│   ├── app.py
├── modules/
│   ├── Digits.py
│   ├── numbersValidation.py
│   └── range_check.py   
├── Frontend/
│   ├── static/
│   │   ├── style.css
│   │   ├── script.js
│   │   └── few images files
│   └── templates/
│       └── index.html
├── models/
│   └── LogR_model.pkl
├── requirements.txt
```

## Setup Instructions ⚙️

### Prerequisites 🛠️

- Python 3.8+ 🐍
- Flask 🏗️
- scikit-learn 📚
- Google Cloud Platform (GCP) account ☁️
- Google AI Studio API key 🔑

### Installation 📝

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Diabetes_project.git
    cd Diabetes_project
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your Google AI Studio API key:
    - Go to GCP and create a project.
    - Create an API key from Google AI Studio for integrating AI into the project.
    - Save the API key in a `.env` file in the root directory of your project:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

### Running the Application 🚀

1. Start the Flask server:
    ```bash
    python Backend/app.py
    ```

2. Open your browser and navigate to `http://localhost:5000` to view the web app. 🌐

## Usage 🖥️

1. **Input Patient Data**: Enter the patient's parameters on the left side of the UI. 📝
2. **AI Doctor Chat**: Interact with the AI doctor on the right side for reviews and insights. 💬
3. **Generate Report**: Click the 'Generate Report' button to get a detailed report of the patient's data, diagnosis, and AI doctor's review. 📑

## Models and Data 📊

- The diabetes prediction model is trained using a logistic regression algorithm. 📈
- The dataset used for training the model is from Kaggle. 🏆

## Frontend 🎨

- The frontend is built with HTML, CSS, and JavaScript. 🌐
- The UI is designed to be user-friendly with a clear distinction between patient data input and AI doctor chat sections. 🖥️

## Backend 🔧

- The backend is powered by Flask. ⚙️
- The logistic regression model (`LogR_model.pkl`) is used for prediction. 🧠
- The AI service integrates the Google Gemini model for reviewing patient data and diagnosis. 🤖

## Future Enhancements 🔮

- Implement user login functionality. 🔐
- Allow users to upload photos for more detailed reports. 📸

## Contributing 🌟

1. Fork the repository. 🍴
2. Create a new branch (`git checkout -b feature/your-feature`). 🌿
3. Make your changes. ✍️
4. Commit your changes (`git commit -m 'Add some feature'`). 💾
5. Push to the branch (`git push origin feature/your-feature`). 🚀
6. Open a pull request. 🔄

## License 📜

This project is licensed under the MIT License. See the `LICENSE` file for more details. 📜

## Demo 🎥


https://github.com/user-attachments/assets/7134075f-1b1e-45d7-bed0-60be6c0e3791

