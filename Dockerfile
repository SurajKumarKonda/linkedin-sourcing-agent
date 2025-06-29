FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"] 