<div align="center">

# AICTE TechSaksham Medical Diagnosis Project 

![License](https://img.shields.io/github/license/aka-0x4C3DD/aicte25-techSaksham-p4p2?style=flat-square)
![Issues](https://img.shields.io/github/issues/aka-0x4C3DD/aicte25-techSaksham-p4p2?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/aka-0x4C3DD/aicte25-techSaksham-p4p2?style=flat-square)
[![Code Size](https://img.shields.io/github/languages/code-size/aka-0x4C3DD/aicte25-techSaksham-p4p2.svg)]()
<img src="https://img.shields.io/badge/python-3.10-blue.svg">
<!--![GitHub stars](https://img.shields.io/github/stars/aka-0x4C3DD/aicte25-techSaksham-p4p2?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/aka-0x4C3DD/aicte25-techSaksham-p4p2?style=flat-square) -->


</div>

<div align="center">
  <i>A Flask web application for predicting medical conditions using machine learning models.</i>
<br> <br>

[📖 About](#-about) • 
[✨ Features](#-features)  • 
[🛠️ Technology Stack](#️-technology-stack)  • 
[📦 Prerequisites](#prerequisites)  • 
[📥 Installation](#installation)  • 
[🎮 Usage](#-usage) • 
[👥 Contributing](#-contributing) • 
[📄 License](#-license) • 
[🙏 Acknowledgements](#-acknowledgements)
<!-- [🚀 Getting Started](#-getting-started)  • -->

</div>

<div align="center">

## 📖 About

</div>

This project, developed as part of the AICTE TechSaksham program, provides a web application for predicting various medical conditions. It utilizes machine learning models trained on different datasets to predict the likelihood of diabetes, heart disease, hypothyroid, lung cancer, and Parkinson's disease. The application is built using Flask and incorporates best practices for model management, prediction service, and user interface.

<div align="center">

## ✨ Features

</div>

-   **Multiple Disease Prediction:** Predicts the likelihood of five different medical conditions:
    -   Diabetes (using Random Forest)
    -   Heart Disease (using TensorFlow)
    -   Hypothyroid (using Logistic Regression)
    -   Lung Cancer (using Random Forest)
    -   Parkinson's Disease (using TensorFlow)
-   **Web Interface:** User-friendly web interface for inputting data and receiving predictions.
-   **API Endpoint:** Provides an API endpoint (`/api/predict/<disease>`) for programmatic access to predictions.
-   **Model Management:** Efficiently loads and manages multiple machine learning models.
-   **Scalable Architecture:** Designed with a modular architecture for easy extension and maintenance.
-   **Data Validation:** Includes input validation to ensure data quality.
- **Dynamic Model Loading:** Loads models from a configurable directory.

<div align="center">

## 🛠️ Technology Stack

</div>
<div align="center">

   ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
   ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
   ![Scikit-learn](https://img.shields.io/badge/ScikitLearn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
   ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
   ![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
   ![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
   ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
   ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

</div>
<!-- 
<div align="center">

## 🚀 Getting Started

</div> 
-->

<div align="center">

## 📦 Prerequisites

</div>

-   Python 3.9+
-   pip

<div align="center">

## 📥 Installation

</div>

1.  Clone the repository:

    ```bash
    git clone https://github.com/aka-0x4C3DD/aicte25-techSaksham-p4p2.git
    ```

2.  Navigate to the project directory:

    ```bash
    cd aicte25-techSaksham-p4p2
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Run the application using the provided shell script (for Unix-like systems) or batch file (for Windows):

    ```bash
    # For Unix-like systems (macOS, Linux)
    ./run.sh

    # For Windows
    run.bat
    ```

    Or, run the Flask server directly:
    ```bash
    python codebase/server.py
    ```

The application will be accessible at `http://localhost:5000`.

<div align="center">

## 🎮 Usage

</div>

1.  Open a web browser and navigate to `http://localhost:5000`.
2.  Select the disease you want to predict from the available options.
3.  Fill in the required input fields on the prediction form.
4.  Click the "Predict" button to submit the form.
5.  The prediction result, along with the confidence level (if available), will be displayed on the results page.

You can also use the API endpoint `/api/predict/<disease>` to get predictions programmatically. Send a POST request with a JSON payload containing the required input data.

<div align="center">

## 👥 Contributing

</div>

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name`
3.  Commit your changes: `git commit -m "Add your commit message"`
4.  Push to the branch: `git push origin feature/your-feature-name`
5.  Open a pull request.

<div align="center">

## 📄 License

</div>

Distributed under the Unilicense License. See `LICENSE` for more information.

<!-- <div align="center">

 ## 📞 Contact

</div>

Project Link: [https://github.com/aka-0x4C3DD/aicte25-techSaksham-p4p2](https://github.com/aka-0x4C3DD/aicte25-techSaksham-p4p2) -->

<div align="center">

## 🙏 Acknowledgements

</div>

-   [AICTE](https://www.aicte-india.org/)
-   [TechSaksham Program](https://techsaksham.org/)

---

<div align="center">
    made with ❤️ by open source contributors
</div>
