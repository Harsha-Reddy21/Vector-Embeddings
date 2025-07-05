import uuid
from datetime import datetime
from typing import Dict, List, Any

# In-memory database
tickets_db: Dict[str, Any] = {}
responses_db: Dict[str, Any] = {}

# Sample historical tickets
historical_tickets = [
    {
        "text": "My order hasn't arrived in 10 days", 
        "solution": "Your package is delayed due to weather conditions. We've contacted our shipping partner and they've confirmed it will arrive within the next 2-3 business days."
    },
    {
        "text": "Payment failed but amount was deducted", 
        "solution": "This is typically a temporary authorization hold. The charge should be reversed within 3-5 business days. If not, please contact your bank with reference #PAY-123."
    },
    {
        "text": "How do I return a product?", 
        "solution": "You can initiate a return through your account dashboard. Go to Orders > Select the item > Return. Print the return label and drop it off at any courier location."
    },
    {
        "text": "The product I received is damaged", 
        "solution": "We're sorry to hear that. Please take a photo of the damaged item and submit it through our returns portal. We'll process a replacement or refund within 24 hours."
    },
    {
        "text": "I can't log into my account", 
        "solution": "Try resetting your password using the 'Forgot Password' link. If that doesn't work, clear your browser cookies and cache, then try again. For persistent issues, contact support."
    }
]

# Sample company documentation
company_docs = [
    {
        "title": "Shipping Policy", 
        "content": "We ship within 5-7 business days using trusted courier partners. Express shipping (1-2 days) is available for an additional fee. International orders may take 10-14 business days. All orders include tracking information sent via email."
    },
    {
        "title": "Return Policy", 
        "content": "Returns are accepted within 30 days of purchase with original packaging. Refunds are processed within 5-7 business days after the returned item is received. For damaged items, please include photos when initiating the return."
    },
    {
        "title": "Payment Methods", 
        "content": "We accept all major credit cards, PayPal, and Apple Pay. Payment information is securely encrypted. For failed transactions, the authorization hold is typically released within 3-5 business days."
    },
    {
        "title": "Account Security", 
        "content": "We use industry-standard encryption to protect your data. Passwords are hashed and never stored in plain text. Enable two-factor authentication for additional security. If you suspect unauthorized access, contact support immediately."
    },
    {
        "title": "Product Warranty", 
        "content": "All electronic products include a 1-year manufacturer warranty covering defects. Warranty claims require proof of purchase and product serial number. Accidental damage is not covered under the standard warranty."
    }
]

def get_ticket(ticket_id: str):
    """Get a ticket by ID"""
    return tickets_db.get(ticket_id)

def get_all_tickets():
    """Get all tickets"""
    return list(tickets_db.values())

def create_ticket(ticket_data: dict):
    """Create a new ticket"""
    ticket_id = str(uuid.uuid4())
    ticket_data["id"] = ticket_id
    ticket_data["submitted_at"] = datetime.now().isoformat()
    tickets_db[ticket_id] = ticket_data
    return ticket_data

def update_ticket(ticket_id: str, ticket_data: dict):
    """Update an existing ticket"""
    if ticket_id in tickets_db:
        tickets_db[ticket_id].update(ticket_data)
        return tickets_db[ticket_id]
    return None

def save_response(response_data: dict):
    """Save a response to a ticket"""
    response_id = str(uuid.uuid4())
    response_data["id"] = response_id
    response_data["created_at"] = datetime.now().isoformat()
    responses_db[response_id] = response_data
    return response_data

def get_ticket_responses(ticket_id: str):
    """Get all responses for a ticket"""
    return [r for r in responses_db.values() if r["ticket_id"] == ticket_id]

def get_historical_tickets():
    """Get sample historical tickets"""
    return historical_tickets

def get_company_docs():
    """Get sample company documentation"""
    return company_docs 