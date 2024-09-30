import openai
import streamlit as st
import pandas as pd
import pyperclip

# Configure OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Inject custom CSS
def add_custom_css():
    st.markdown(
        """
        <style>
            /* Custom styles omitted for brevity */
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to call OpenAI API for generating the sales email
def generate_sales_email(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional sales email assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message["content"]
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Main app function
def main():
    st.title("Sales Karma Email Generator")
    
    target_domain = st.text_input("Target Domain", placeholder="example.com")
    persona = st.text_input("Persona", placeholder="SDR or Account Executive")
    additional_info = st.text_area("Additional Information", placeholder="Include any extra details about the target or the sender")
    
    # Option for selecting outreach format
    outreach_format = st.checkbox("Format for Outreach with Variables", help="Use outreach variables like <First Name>, <Senders Name>")

    # Prompt to generate the email
    if st.button("Generate Email"):
        with st.spinner("Generating sales email..."):
            prompt = (
                f"Write an introductory, first-time outreach email targeted to a {persona} at {target_domain}. "
                f"Use {additional_info} to provide more context. "
                f"IMPORTANT: This is the first email, so do not mention any prior conversations."
            )
            
            if outreach_format:
                prompt += " Please format the email for Outreach.io by using variables like <First Name> and <Senders Name>."
            
            email_copy = generate_sales_email(prompt)
            
            if email_copy:
                st.subheader("Generated Email Copy")
                st.write(email_copy)
                
                # Copy to clipboard button
                if st.button("Copy to Clipboard"):
                    pyperclip.copy(email_copy)
                    st.success("Email copied to clipboard!")

if __name__ == "__main__":
    main()
