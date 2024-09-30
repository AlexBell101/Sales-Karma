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
    if is_outreach_format:
        intro = "Hi {{first_name}},"
    else:
        intro = "Hi <First Name>,"

    case_study_prompt = (
        f"Write an introductory sales email for an {persona} at {target_domain}. "
        f"Make it clear that this is the first communication between the sender and recipient, "
        f"so do not reference any previous emails, meetings, or conversations. "
        f"Use the sender's domain {senders_domain} to provide context about the sender's company and expertise, "
        f"If no real case study is available, suggest a hypothetical use case relevant to {target_domain}'s industry, "
        f"but don't use placeholder names. "
        f"Here is additional information for context: {additional_info}. "
        f"Keep the email concise, and end with a clear call to action for scheduling a call or providing more information. "
    )

    # Prompt for Outreach formatting
    if is_outreach_format:
        case_study_prompt += (
            "The email should be formatted for Outreach, including tokens such as "
            "<First Name>, <senders Name>, <senders Title>, and <senders Phone>. "
            "Include tokens at the start of the email and in the closing section."
        )
    
    # Nurture sequence
    if num_touches > 1:
        case_study_prompt += (
            f"Generate {num_touches} emails in a nurture sequence, "
            "starting with an introduction and followed by a gradual increase in product details and value proposition."
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
