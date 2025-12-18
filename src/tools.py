from langchain_core.tools import tool

@tool
def write_email(to: str, subject: str, content: str) -> str:
    """
    Tool for composing and sending email responses.
    Args:
        to: Recipient email address
        subject: Email subject line
        content: Email body content
    Returns:
        str: Confirmation message of email sent
    """
    # In a real app, this would use Gmail API / SMTP
    print(f"--- TOOL USE: Sending email to {to} ---")
    print(f"Subject: {subject}")
    print(f"Content: {content}")
    return f"Email sent to {to}."

@tool
def check_calendar_availability(day: str) -> str:
    """
    Tool for checking calendar availability.
    Args:
        day: Day to check availability for (e.g., 'Monday', '2024-01-01')
    Returns:
        str: Available time slots
    """
    # Mock implementation
    print(f"--- TOOL USE: Checking calendar for {day} ---")
    return f"Available times on {day}: 9:00 AM, 2:00 PM, 4:00 PM"

# Export list for the agent
ACIONS_TOOLS = [write_email, check_calendar_availability]
