import os

from dotenv import load_dotenv

from mediqbox.sendmail.sendmail import (
  Sendmail,
  SendmailConfig,
  SendmailInputData
)
from tests.ses_email_client import SesEmailClient

load_dotenv()

from tests.settings import settings

def test_sendmail() -> None:
  data_dir = os.path.join(os.path.dirname(__file__), 'data')

  input_data = SendmailInputData(
    From=settings.From,
    To=[settings.To],
    Cc=[settings.Cc],
    Subject=settings.Subject,
    TextBody=settings.Body,
    Attachments=[os.path.join(data_dir, item) for item in [
      'att.txt', 'att.pdf']]
  )

  with SesEmailClient(settings.AWS_PROFILE_NAME) as email_client:
    sendmail = Sendmail(config=SendmailConfig(
      email_client=email_client
    ))
    sendmail.process(input_data)

  assert True

if __name__ == '__main__':
  test_sendmail()