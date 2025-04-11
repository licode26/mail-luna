import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import datetime

# Set page configuration
st.set_page_config(
    page_title="Feedback Form",
    page_icon="📝",
    layout="centered"
)

# App title and description
st.title("📝 We Value Your Feedback!")
st.write("Help us improve by sharing your experience with our product/service.")

# Create a function to validate email
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

# Function to send email
def send_feedback_email(name, email, rating, product_used, duration, feedback_text, suggestions, specific_ratings, nps, contact_permission):
    try:
        # Configure these settings with your email provider details
        SMTP_SERVER = "smtp.gmail.com"  # For Gmail - change to your provider's SMTP server if different
        SMTP_PORT = 587  # Common port for TLS
        SENDER_EMAIL = "farm.luna.123@gmail.com"  # Replace with your actual email
        SENDER_PASSWORD = "yvwa krnf vcer jhzi"  # Replace with your app password or email password
        RECIPIENT_EMAIL = "farm.luna.123@gmail.com"  # Replace with where you want to receive feedback (can be same as sender)

        # Create a multipart message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = f"New Feedback Submission - Rating: {rating}/5"

        # Current date and time
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Construct the email body
        email_body = f"""
        New feedback received on {current_time}:
        
        From: {name if name else 'Anonymous'} ({email})
        Overall Rating: {rating}/5
        Product/Service Used: {product_used}
        Duration of Use: {duration}
        
        Feedback:
        {feedback_text}
        
        Suggestions for Improvement:
        {suggestions if suggestions else 'None provided'}
        
        Specific Ratings:
        - Ease of Use: {specific_ratings['ease_of_use']}
        - Customer Service: {specific_ratings['customer_service']}
        - Value for Money: {specific_ratings['value_for_money']}
        - Features & Functionality: {specific_ratings['features']}
        
        Net Promoter Score: {nps}/10
        
        Contact Permission: {'Yes' if contact_permission else 'No'}
        """
        
        msg.attach(MIMEText(email_body, "plain"))
        
        # Connect to server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

# Feedback form
with st.form("feedback_form"):
    # Personal information
    st.subheader("About You")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name (Optional)", placeholder="John Doe")
    
    with col2:
        email = st.text_input("Email Address", placeholder="john.doe@example.com")
    
    # Product/service information
    st.subheader("Product/Service Information")
    
    product_used = st.selectbox("What product/service are you providing feedback about?", [
        "Select an option",
        "Mobile App",
        "Website",
        "Customer Service",
        "Product A",
        "Product B",
        "Other"
    ])
    
    duration = st.selectbox("How long have you been using our product/service?", [
        "Less than a month",
        "1-6 months",
        "6-12 months",
        "1-2 years",
        "More than 2 years"
    ])
    
    # Rating and feedback
    st.subheader("Your Feedback")
    
    rating = st.slider("Overall Rating", min_value=1, max_value=5, value=3, help="1 = Very Unsatisfied, 5 = Very Satisfied")
    
    # Show different emoji based on rating
    if rating == 1:
        st.write("😞")
    elif rating == 2:
        st.write("🙁")
    elif rating == 3:
        st.write("😐")
    elif rating == 4:
        st.write("🙂")
    else:
        st.write("😀")
    
    feedback_text = st.text_area(
        "Please share your experience with us",
        placeholder="What did you like or dislike? How was your overall experience?",
        height=150
    )
    
    suggestions = st.text_area(
        "Do you have any suggestions for improvement?", 
        placeholder="Your ideas help us serve you better...",
        height=100
    )
    
    # Optional aspect-specific ratings
    st.subheader("Rate Specific Aspects (Optional)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ease_of_use = st.select_slider("Ease of Use", options=["Poor", "Below Average", "Average", "Good", "Excellent"], value="Average")
        customer_service = st.select_slider("Customer Service", options=["Poor", "Below Average", "Average", "Good", "Excellent"], value="Average")
    
    with col2:
        value_for_money = st.select_slider("Value for Money", options=["Poor", "Below Average", "Average", "Good", "Excellent"], value="Average")
        features = st.select_slider("Features & Functionality", options=["Poor", "Below Average", "Average", "Good", "Excellent"], value="Average")
    
    # Likelihood to recommend
    nps = st.slider("How likely are you to recommend us to others? (0-10)", min_value=0, max_value=10, value=7)
    
    # Contact permission
    contact_permission = st.checkbox("I'm open to being contacted about my feedback if needed")
    
    # Submit button
    submit_button = st.form_submit_button("Submit Feedback")

# Form processing
if submit_button:
    # Form validation
    if not email:
        st.error("Please provide your email address so we can follow up if needed.")
    elif not is_valid_email(email):
        st.error("Please enter a valid email address.")
    elif product_used == "Select an option":
        st.error("Please select which product or service you're providing feedback about.")
    elif not feedback_text:
        st.error("Please share your feedback with us.")
    else:
        # Collect all specific ratings
        specific_ratings = {
            "ease_of_use": ease_of_use,
            "customer_service": customer_service,
            "value_for_money": value_for_money,
            "features": features
        }
        
        # Send feedback via email - THIS LINE IS NOW ENABLED
        success = send_feedback_email(
            name, 
            email, 
            rating, 
            product_used, 
            duration, 
            feedback_text, 
            suggestions,
            specific_ratings,
            nps,
            contact_permission
        )
        
        if success:
            st.success("Thank you for your valuable feedback! We appreciate you taking the time to share your thoughts with us.")
            
            # Show a thank you message based on rating
            if rating >= 4:
                st.balloons()
                st.write("We're thrilled to hear you had a positive experience! Your feedback helps us maintain our high standards.")
            else:
                st.write("We appreciate your honest feedback and will use it to improve our services.")
                
        else:
            st.error("There was a problem submitting your feedback. Please try again later.")

# Additional information sidebar
with st.sidebar:
    st.subheader("Why Your Feedback Matters")
    st.write("""
    Your feedback is invaluable to us! It helps us:
    - Understand what we're doing right
    - Identify areas for improvement
    - Develop new features based on your needs
    - Provide better service to all our customers
    """)
    
    st.divider()
    
    st.subheader("What Happens Next?")
    st.write("""
    1. Our team reviews all feedback regularly
    2. We prioritize improvements based on customer input
    3. If you've given permission, we may contact you for more details
    4. You'll see the impact of your feedback in future updates!
    """)
    
    st.divider()
    
    # Add some contact information
    st.subheader("Have Questions?")
    st.write("Email us: farm.luna.123@gmail.com")
    st.write("Call us:7978018725")