import streamlit as st
from openai import OpenAI
from openai import OpenAIError
import os

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inject custom CSS with the background image and styling
def add_custom_css():
    st.markdown(
        """
        <style>
            /* Custom styles omitted for brevity */
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to call OpenAI API
def generate_sales_email(prompt, touches, persona, target_domain, sender_domain, additional_info, outreach_format):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an SDR/Account Executive writing sales outreach emails."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content
    except OpenAIError as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to generate the prompt
def create_sales_prompt(outreach_type, persona, target_domain, sender_domain, additional_info, num_touches, outreach_format):
    if outreach_format:
        greeting = "Hi {{first_name}},"
        signature = "\n\nBest,\n{{senders_name}}\n{{title}}\n{{phone}}"
    else:
        greeting = "Hi <First Name>,"
        signature = "\n\nBest regards,\n<Your Name>\n<Your Title>"

    prompt = (
        f"{greeting}\n"
        f"As a {persona} at {sender_domain}, I wanted to reach out to see how we can help {target_domain} improve its operations, "
        f"especially when it comes to {additional_info}. Our solutions have helped many companies in your industry tackle similar "
        f"challenges.\n\n"
        f"Let me know if you'd like to connect.\n"
        f"{signature}\n\n"
        f"Generate {num_touches} emails in a nurturing sequence."
    )

    return prompt

# Streamlit App Main
def main():
    add_custom_css()

    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

    st.title("Sales Karma: Sales Outreach Copy Generator")

    st.subheader("Enter details to create personalized sales outreach emails")

    # Input fields
    target_domain = st.text_input("Target Company Domain (e.g., targetcompany.com)", placeholder="targetcompany.com")
    persona = st.text_input("Target Persona (e.g., CTO, VP Sales)", placeholder="Account Executive")
    sender_domain = st.text_input("Your Company Domain (e.g., yourcompany.com)", placeholder="yourcompany.com")
    additional_info = st.text_input("Additional Information (optional)", placeholder="Provide extra context about your offering")

    outreach_format = st.checkbox("Format for Outreach (with variables)")
    
    if outreach_format:
        st.write("This option will format emails using Outreach tokens like {{first_name}}.")

    # Select between single outreach or nurture sequence
    outreach_type = st.selectbox(
        "Select Outreach Type",
        ("Single Email", "Nurture Sequence")
    )

    # Slider for number of nurtures if the user selects a nurture sequence
    num_touches = st.slider("Number of nurtures", 1, 10, 3) if outreach_type == "Nurture Sequence" else 1

    # Generate the email sequence prompt
    prompt = create_sales_prompt(outreach_type, persona, target_domain, sender_domain, additional_info, num_touches, outreach_format)

    # Button to generate email
    if st.button("Generate Sales Email"):
        with st.spinner("Generating sales email..."):
            result = generate_sales_email(prompt, num_touches, persona, target_domain, sender_domain, additional_info, outreach_format)
            if result:
                st.subheader("Generated Sales Email Copy")
                st.write(result)

    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
