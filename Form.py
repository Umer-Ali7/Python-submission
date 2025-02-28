import streamlit as st
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# ✅ Google Sheets Connection Function
def connect_to_google_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("daily-python-form-1cfb276f2a29.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("Daily-Python-Challenge").sheet1  # Ensure sheet name is correct
        return sheet
    except Exception as e:
        st.error(f"❌ Google Sheets API Connection Error: {e}")
        return None

# ✅ Duplicate Submission Check Function
def is_duplicate_submission(sheet, roll_number, challenge_day):
    try:
        records = sheet.get_all_records()
        for record in records:
            if record["Roll Number"] == roll_number and record["Challenge Day"] == challenge_day:
                return True
        return False
    except Exception as e:
        st.error(f"❌ Error Fetching Records: {e}")
        return False

# ✅ Streamlit App
def main():
    st.title("📅 Daily Python Challenge Submission Form\nBe Careful Ap ek din me Sirf ek hi Submission kiya kary take ap ka LeaderBord Ban Paye Thanks ✔")

    # ✅ Initialize session state to track submission status
    if "submission_done" not in st.session_state:
        st.session_state.submission_done = False

    # ✅ Challenge Day
    challenge_day = datetime.now().strftime("%Y-%m-%d")

    # ✅ User Inputs
    st.subheader("👤 Personal Details")
    full_name = st.text_input("Full Name:")
    roll_number = st.text_input("Roll Number:")
    giaic_slot = st.text_input("GIAIC Slot:")

    st.subheader("📂 Submission Details")
    challenge_day_display = st.text_input("Challenge Day:", value=challenge_day, disabled=True)
    github_link = st.text_input("GitHub Link:")
    feedback_comment = st.text_area("Feedback & Comment (Optional):")

    # ✅ Submit Button
    if st.button("Submit 🚀"):
        if full_name and roll_number and giaic_slot and github_link:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # ✅ Google Sheets Connection
            sheet = connect_to_google_sheet()
            if sheet is None:
                return

            # ✅ Check Duplicate Submission (API + Session State)
            if st.session_state.submission_done or is_duplicate_submission(sheet, roll_number, challenge_day):
                st.error("❌ Aapne aaj pehle hi submit kar diya hai. Ek din mein sirf ek baar submit kar sakte hain.")
            else:
                try:
                    time.sleep(1)  # Google API Rate Limit Handling
                    sheet.append_row([timestamp, full_name, roll_number, giaic_slot, challenge_day, github_link, feedback_comment])
                    
                    # ✅ Mark Submission as Done
                    st.session_state.submission_done = True

                    st.success("🎉 Aapka submission successfully record ho gaya hai!")
                except Exception as e:
                    st.error(f"❌ Google Sheets API Submission Error: {e}")
        else:
            st.error("❌ Please fill in all required fields.")

# ✅ Run the App
if __name__ == "__main__":
    main()
