# Customer Support RAG System - Frontend

This is the frontend for the Customer Support RAG (Retrieval-Augmented Generation) system. It provides a user interface for ticket submission, viewing, and management.

## Features

- Ticket submission form
- Ticket list with filtering by status
- Ticket detail view with AI-generated responses
- Manual response capability for escalated tickets
- Knowledge base management interface

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Create a `.env` file in the frontend directory with your API URL (if different from default):
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

3. Run the development server:
   ```bash
   npm start
   ```

4. The application will be available at http://localhost:3000

## Pages

- **Home**: Submit tickets and view ticket list
- **Ticket Detail**: View ticket details and responses
- **Knowledge Base**: Manage historical tickets and company documentation

## Technologies Used

- React
- React Router
- Material UI
- Axios 