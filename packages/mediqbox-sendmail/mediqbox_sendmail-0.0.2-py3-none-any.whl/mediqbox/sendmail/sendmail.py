import os

from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from pydantic import NameEmail, field_validator
from typing import Any, Optional, Protocol, runtime_checkable

from mediqbox.abc.abc_component import (
  AbstractComponent,
  ComponentConfig,
  InputData
)

# TODO inline images. See: https://stackoverflow.com/a/23853079

### <!-- Some helper methods

def encode_name_email(name_email: NameEmail) -> str:
  encoded_name = Header(name_email.name, 'utf-8').encode()
  return f"{encoded_name} <{name_email.email}>"

def add_attachment(
    message: MIMEMultipart,
    attachment: str
) -> None:
  with open(attachment, 'rb') as fp:
    data = fp.read()

  filename = os.path.basename(attachment)
  part = MIMEApplication(data)
  part.add_header(
    'Content-Disposition',
    'attachment',
    filename=Header(filename, 'utf-8').encode()
  )
  message.attach(part)

### -->

@runtime_checkable
class EmailClientProtocol(Protocol):
  def send_raw_email(self, raw_message: bytes) -> None: ...

class SendmailConfig(ComponentConfig):
  email_client: Any

  @field_validator('email_client')
  def email_client_must_implement_protocol(cls, v: Any) -> Any:
    if not isinstance(v, EmailClientProtocol):
      raise ValueError('`email_client` must implement `send_raw_email` method defined by `EmailClientProtocol`')
    return v
  
class SendmailInputData(InputData):
  From: NameEmail
  To: list[NameEmail]
  Cc: Optional[list[NameEmail]] = None
  Subject: str = ""
  TextBody: Optional[str] = None
  HtmlBody: Optional[str] = None
  Attachments: Optional[list[str]] = None

  @field_validator('To')
  def at_least_one_recipient(cls, v: list[NameEmail]) -> list[NameEmail]:
    if not len(v):
      raise ValueError("Empty 'To'")
    return v
  
  @field_validator('Attachments')
  def attachments_are_files(cls, v: list[str]|None) -> list[str]|None:
    if v and len(v):
      for att in v:
        if not os.path.isfile(att):
          raise ValueError(f"{att} in Attachments is not a valid file")
    return v

class Sendmail(AbstractComponent):

  def process(self, input_data: SendmailInputData) -> None:
    message = MIMEMultipart()

    message['Subject'] = input_data.Subject
    message['From'] = encode_name_email(input_data.From)
    message['To'] = ', '.join([encode_name_email(to) for to in input_data.To])
    if input_data.Cc and len(input_data.Cc):
      message['Cc'] = ', '.join([encode_name_email(cc) for cc in input_data.Cc])
    
    # Attach text body
    if input_data.TextBody:
      message.attach(MIMEText(input_data.TextBody, 'plain'))

    # Attach html body
    if input_data.HtmlBody:
      message.attach(MIMEText(input_data.HtmlBody, 'html'))

    # Add attachments
    if input_data.Attachments:
      for att in input_data.Attachments:
        add_attachment(message, att)
    
    self.config.email_client.send_raw_email(message.as_string())