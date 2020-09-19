

import log
import smtplib
from email.mime.text import MIMEText

class IssueMngr:

    def __init__(self):
        pass

    def rpc_reportIssue(self, faultID, text):
        # log it
        log.message("ISSUE:\n", text)
        # send it
        try:
            msg = MIMEText(text)
            msg["Subject"] = "Outer Space Issue %s" % faultID
            msg["From"] = "game_alpha@ospace.net"
            msg["To"] = "qark@ospace.net"
            smtp = smtplib.SMTP("localhost")
            smtp.sendmail(
                "game_alpha@ospace.net",
                ["qark@ospace.net"],
                msg.as_string()
            )
            smtp.quit()
        except:
            log.warning("Cannot send issue by e-mail")
        return 1

    def shutdown(self):
        pass
