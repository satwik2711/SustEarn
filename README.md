
# README

## Project Overview

This project is a Django-based web application that calculates the environmental footprint of products using Life-Cycle Assessment (LCA) methods. It provides endpoints for fetching life cycle stages, calculating weighted average emissions, optimizing emissions, and fetching direct emissions.

## Features

1. **Get Life Cycle Stages**: Fetch the main life cycle stages of a product based on its description.
2. **Calculate Footprint**: Calculate the weighted average emission and optimized emission using the Clean Tech Mart algorithm.
3. **Get Emission**: Fetch the direct emission data for a product using NLP prompt engineering.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x
- Django 3.x or later
- An active Google API key for using Google Generative AI
- Virtualenv (optional but recommended)

## Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and Activate a Virtual Environment (Optional)**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add your Google API key:
   
   ```env
   GOOGLE_API_KEY=your_google_api_key
   ```



## Running the Server

To start the development server, run:

```sh
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`.

## API Endpoints

### Get Life Cycle Stages

**URL:** `api/lcs`

**Method:** `POST`

**Request Payload:**

```json
{
    "name": "Product Name",
    "description": "Product Description"
}
```

**Response:**

```json
{
    "life_cycle_stages": "Stage 1, Stage 2, Stage 3"
}
```

### Calculate Footprint

**URL:** `api/calculate/`

**Method:** `POST`

**Request Payload:**

```json
{
    "name": "Product Name",
    "life_cycle_stages": ["Stage 1", "Stage 2", "Stage 3"],
    "weights": {
        "Stage 1": 0.3,
        "Stage 2": 0.4,
        "Stage 3": 0.3
    }
}
```

**Response:**

```json
{
    "weighted_average_emission": 123.45,
    "optimized_emission": 110.00
}
```

### Get Emission

**URL:** `api/emission/`

**Method:** `POST`

**Request Payload:**

```json
{
    "name": "Product Name"
}
```

**Response:**

```json
{
    "emission": 150.75
}
```



## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Google Generative AI Documentation](https://cloud.google.com/generative-ai)
- [Python Virtual Environment Documentation](https://docs.python.org/3/tutorial/venv.html)

