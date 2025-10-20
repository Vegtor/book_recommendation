# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend files
COPY recommend_api.py book_recommend_sql.py book_recommend_goodreads.py database_manager.py ./

# Expose port for FastAPI
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "recommend_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]