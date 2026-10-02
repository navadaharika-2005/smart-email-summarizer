import streamlit as st
from transformers import pipeline

from gmail_service import connect_gmail, get_emails, get_email


st.set_page_config(
    page_title="Smart Email Summarizer",
    page_icon="📧",
    layout="centered"
)

st.title("📧 Smart Email Summarizer")
st.write("Turn long emails into short, clear summaries.")


@st.cache_resource
def load_model():
    return pipeline(
        "summarization",
        model="sshleifer/distilbart-cnn-12-6"
    )


# Connect to Gmail
service = connect_gmail()


# Get emails from inbox
emails = get_emails(service, max_results=10)


# Session state
if "summary" not in st.session_state:
    st.session_state.summary = ""

if "email_text" not in st.session_state:
    st.session_state.email_text = ""


st.subheader("📬 Your Gmail Inbox")


if emails:

    email_options = {}

    for email in emails:
        display_name = (
            f"{email['subject']} — {email['sender']}"
        )

        email_options[display_name] = email["id"]


    selected_email = st.selectbox(
        "Select an email",
        list(email_options.keys())
    )


    if st.button(
        "📖 Load Email",
        use_container_width=True
    ):

        message_id = email_options[selected_email]

        with st.spinner("Reading email..."):

            email = get_email(
                service,
                message_id
            )

        st.session_state.email_text = email["body"]
        st.session_state.summary = ""

        st.success("Email loaded successfully!")


else:

    st.warning("No emails found in your Gmail inbox.")


# Show loaded email
if st.session_state.email_text:

    st.subheader("📩 Email Content")

    st.text_area(
        "Email",
        value=st.session_state.email_text,
        height=250,
        disabled=True
    )


    summary_length = st.selectbox(
        "Choose summary length",
        ["Short", "Medium", "Detailed"]
    )


    if st.button(
        "✨ Summarize Email",
        use_container_width=True
    ):

        with st.spinner("Generating your summary..."):

            try:

                summarizer = load_model()


                if summary_length == "Short":
                    max_len, min_len = 60, 10

                elif summary_length == "Medium":
                    max_len, min_len = 100, 20

                else:
                    max_len, min_len = 150, 40


                result = summarizer(
                    st.session_state.email_text,
                    max_length=max_len,
                    min_length=min_len,
                    do_sample=False,
                    truncation=True
                )


                st.session_state.summary = (
                    result[0]["summary_text"]
                )


            except Exception as error:

                st.error(
                    f"Could not generate summary: {error}"
                )


# Show summary
if st.session_state.summary:

    st.subheader("📝 AI-Generated Summary")

    st.success(
        st.session_state.summary
    )


    st.text_input(
        "Copy your summary from here",
        value=st.session_state.summary,
        key="copy_summary_text"
    )


    st.code(
        st.session_state.summary,
        language=None
    )


    st.download_button(
        label="📥 Download Summary",
        data=st.session_state.summary,
        file_name="email_summary.txt",
        mime="text/plain",
        use_container_width=True
    )