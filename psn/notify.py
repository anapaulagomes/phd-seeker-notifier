import os
from datetime import datetime

import sendgrid

from dotenv import load_dotenv

load_dotenv()

sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))


def send_email(positions, country):
    today = datetime.today()
    week_number, year = today.isocalendar()[1], today.year
    positions_html = [
        f"<p>{index}) "
        f"<a href={position['link']}>{position['title']}</a> "
        f"({position['last_seen']})"
        f"</p>"
        for index, position in enumerate(positions, start=1)
    ]
    positions_section = "".join(positions_html)
    message = sendgrid.Mail(
        from_email=(os.environ.get("FROM_EMAIL"), "PhD Seeker Notifier"),
        to_emails=(os.environ.get("TO_EMAILS"), "Ana Paula Gomes"),
        subject=f"Open PhD positions in {country} (week {week_number}/{year}) 🎓",
        html_content=f"""
            <h2>Open PhD positions</h2>
            {positions_section}
        """
    )
    try:
        sg.send(message)
    except Exception as e:
        print(f"Error sending email: {e}.")
    else:
        print("Email sent successfully")
