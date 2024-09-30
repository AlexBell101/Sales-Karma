import streamlit as st
from openai import OpenAI
from openai import OpenAIError
import os

# Configure OpenAI API key via environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
def create_sales_prompt(persona, target_domain, senders_domain, additional_info, num_touches, is_outreach_format=False):
    # Start with the salutation format
    if is_outreach_format:
        intro = "Hi {{first_name}},"
    else:
        intro = "Hi <First Name>,"

    # Strongly worded prompt to ensure no mention of previous conversations
    case_study_prompt = (
        f"Write an introductory, first-time outreach email targeted to an {persona} at {target_domain}. "
        f"IMPORTANT: This is the first email and there has been NO previous conversation. "
        f"DO NOT mention any prior email, conversation, or any reference to earlier interactions. "
        f"Use the sender's domain {senders_domain} to provide context about the sender's company and explain how it can help {target_domain}. "
        f"Do not use placeholder phrases like 'XYZ Company'. You may use a hypothetical example relevant to challenges {target_domain} might face in their industry. "
        f"Here is additional information to consider when writing the email: {additional_info}. "
        f"Keep the email concise, professional, and end with a clear call to action to schedule a call."
    )

    # Add specific instructions if Outreach format is selected
    if is_outreach_format:
        case_study_prompt += (
            " Format the email for Outreach using tokens such as <First Name>, <senders Name>, <senders Title>, and <senders Phone>. "
            "Begin the email with 'Hi {{first_name}},' and include sender tokens in the closing section."
        )

    # Add nurture sequence instructions if multiple touches are selected
    if num_touches > 1:
        case_study_prompt += (
            f" Generate {num_touches} emails as part of a nurture sequence. "
            "The first email should introduce the sender and solution, while subsequent emails should provide increasing detail about the value proposition."
        )

    return intro + "\n" + case_study_prompt
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
