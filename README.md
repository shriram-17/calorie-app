# Recipe Recommendation System

## Overview
This project is a **Recipe Recommendation System** that allows users to:
- Generate new recipes based on their preferences.
- Find exact matches for specific recipes.
- Get recommendations for similar recipes.
- Analyze ingredients for allergens and substitutions.
- Estimate calorie content and get nutritional insights.

The system is built using the following technologies:
- **Frontend**: Next.js
- **API**: GraphQL (Strawberry)
- **Backend**: FastAPI
- **Multi-Agent System**: LangChain/CrewAI
- **Message Broker**: Kafka
- **Vector Storage**: Supabase
- **Image URL Storage**: PostgreSQL
- **Image Storage**: Firebase

---

## Workflow

### 1. **User Input**
- The user provides a query (e.g., "Create a recipe with chicken and garlic" or "Find recipes with chicken and garlic").
- The query is sent to the **GraphQL API**.

### 2. **GraphQL API**
- Validates the query and forwards it to the **backend**.
- Determines the type of query:
  - **Exact Match**: User wants a specific recipe.
  - **Recommendation**: User wants similar recipes.
  - **Synthetic Recipe**: User wants a new recipe generated.

### 3. **Backend Processing**
- The backend receives the query and publishes it to the appropriate **Kafka topic**:
  - `exact-match-requests`: For exact match queries.
  - `recommendation-requests`: For recommendation queries.
  - `synthetic-recipe-requests`: For synthetic recipe generation.

### 4. **Kafka Consumers**
- **Exact Match Consumer**:
  - Listens to the `exact-match-requests` topic.
  - Uses the **Info Retrieval Agent** to find the **top-1 recipe** using **RRF (Reciprocal Rank Fusion)**.
  - Publishes the result to the `exact-match-results` topic.
- **Recommendation Consumer**:
  - Listens to the `recommendation-requests` topic.
  - Uses the **Recommendation Agent** to find the **top-K recipes** using **RRF**.
  - Publishes the result to the `recommendation-results` topic.
- **Synthetic Recipe Consumer**:
  - Listens to the `synthetic-recipe-requests` topic.
  - Uses the **Synthetic Recipe Agent** to generate multiple new recipes.
  - Publishes the result to the `synthetic-recipe-results` topic.

### 5. **Result Processing**
- The backend subscribes to the Kafka result topics:
  - `exact-match-results`: Retrieves the top-1 recipe.
  - `recommendation-results`: Retrieves the top-K recipes.
  - `synthetic-recipe-results`: Retrieves the generated recipes.
- Processes the results and sends them back to the **GraphQL API**.

### 6. **GraphQL API Response**
- The GraphQL API returns the results to the **frontend**:
  - **Exact Match**: Returns the top-1 recipe.
  - **Recommendation**: Returns the top-K recipes.
  - **Synthetic Recipe**: Returns the generated recipes.

### 7. **Frontend Display**
- The frontend receives the results and displays them to the user:
  - **Exact Match**: Displays the top-1 recipe.
  - **Recommendation**: Displays the top-K recipes.
  - **Synthetic Recipe**: Displays the generated recipes.

---

## Architecture

### 1. **Frontend (Next.js)**
- Provides a user-friendly interface for browsing recipes, viewing nutritional information, and tracking calorie intake.
- Communicates with the backend via **GraphQL API**.

### 2. **GraphQL API (Strawberry)**
- Acts as the interface between the frontend and backend.
- Handles queries and mutations for recipes, calorie analysis, and user data.

### 3. **Backend (FastAPI)**
- Processes requests from the GraphQL API.
- Publishes tasks to Kafka topics for asynchronous processing.
- Subscribes to Kafka result topics to retrieve processed results.

### 4. **Kafka**
- Handles asynchronous task processing:
  - `exact-match-requests`: For exact match queries.
  - `recommendation-requests`: For recommendation queries.
  - `synthetic-recipe-requests`: For synthetic recipe generation.
  - `exact-match-results`: For exact match results.
  - `recommendation-results`: For recommendation results.
  - `synthetic-recipe-results`: For synthetic recipe results.

### 5. **Agents**
- **Synthetic Recipe Agent**: Generates multiple new recipes based on user input.
- **Info Retrieval Agent**: Returns the **top-1 recipe** for exact match queries.
- **Recommendation Agent**: Returns the **top-K recipes** for recommendation queries.
- **Ingredient Checker Agent**: Analyzes ingredients for allergens, substitutions, and hard-to-find items.
- **Calorie Agent**: Estimates calorie content and provides nutritional insights.
- **Insights Agent**: Provides cultural and health-related insights about recipes.

### 6. **Data Storage**
- **Supabase**:
  - Stores recipe embeddings for semantic search.
  - Supports vector similarity search for recommendations.
- **PostgreSQL**:
  - Stores recipe details (title, ingredients, instructions).
  - Stores image URLs (linked to Firebase).
- **Firebase**:
  - Stores recipe images.

---

## Setup Instructions

### Prerequisites
- Node.js (for Next.js)
- Python 3.8+ (for FastAPI and LangChain/CrewAI)
- Docker (for Kafka and PostgreSQL)
- Firebase account (for image storage)
- Supabase account (for vector storage)

### 1. **Frontend (Next.js)**
1. Clone the frontend repository:
   ```bash
   git clone https://github.com/your-username/calorie-app-frontend.git
   cd calorie-app-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. The frontend will be available at `http://localhost:3000`.

### 2. **GraphQL API (Strawberry)**
1. Clone the API repository:
   ```bash
   git clone https://github.com/your-username/calorie-app-api.git
   cd calorie-app-api
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the GraphQL server:
   ```bash
   python main.py
   ```
4. The GraphQL API will be available at `http://localhost:8000/graphql`.

### 3. **Backend (FastAPI)**
1. Clone the backend repository:
   ```bash
   git clone https://github.com/your-username/calorie-app-backend.git
   cd calorie-app-backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
4. The backend will be available at `http://localhost:8001`.

### 4. **Kafka**
1. Start Kafka using Docker:
   ```bash
   docker-compose up -d
   ```
2. Configure Kafka topics in the backend (see `backend/kafka.py`).

### 5. **Supabase**
1. Create a Supabase project and enable the Vector extension.
2. Configure Supabase credentials in the backend (see `backend/supabase.py`).

### 6. **PostgreSQL**
1. Start PostgreSQL using Docker:
   ```bash
   docker-compose up -d
   ```
2. Configure PostgreSQL credentials in the backend (see `backend/database.py`).

### 7. **Firebase**
1. Create a Firebase project and enable Firebase Storage.
2. Configure Firebase credentials in the backend (see `backend/firebase.py`).

---

## Environment Variables
Create a `.env` file in each component with the following variables:

### Frontend (Next.js)
```env
NEXT_PUBLIC_GRAPHQL_API=http://localhost:8000/graphql
```

### GraphQL API (Strawberry)
```env
BACKEND_URL=http://localhost:8001
```

### Backend (FastAPI)
```env
KAFKA_BROKER=localhost:9092
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
POSTGRES_URL=postgresql://user:password@localhost:5432/calorie_app
FIREBASE_CREDENTIALS=path/to/firebase/credentials.json
```

---

## Contributing
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README provides a comprehensive blueprint for your **Recipe Recommendation System**. Let me know if you need further assistance! 🚀
