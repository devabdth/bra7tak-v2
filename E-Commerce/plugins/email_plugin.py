import sys
sys.path.insert(0, '../')

from config import Config


class EmailPlugin:
	def __init__(self):
		self.cfg: Config= Config()


	def send_raw_email(self, msg, recipent, subject):
		try:
			import smtplib
			from email.mime.text import MIMEText

			msg: MIMEText= MIMEText(msg)
			msg['Subject']= subject
			msg['To']= recipent
			msg['from']= self.cfg.email_model_email
			server= smtplib.SMTP_SSL("smtp.zoho.com", 465)
			server.login(self.cfg.email_model_email, self.cfg.email_model_access_key)

			server.sendmail(self.cfg.email_model_email, [recipent], msg.as_string())
			server.quit()
		except Exception as e:
			print(e)

	def send_raw_email_with_file(self, msg: str, recipent: str, subject: str, attachments: list):
		try:
			import smtplib
			from email.mime.application import MIMEApplication
			from email.mime.multipart import MIMEMultipart
			from email.mime.text import MIMEText
			from os.path import basename

			msg: MIMEMultipart= MIMEMultipart()
			msg['Subject']= subject
			msg['To']= recipent
			msg['from']= self.cfg.email_model_email
			msg.attach(MIMEText(msg))
			print('ONE')

			for f in attachments or []:
				with open(f, "rb") as fil:
					part = MIMEApplication(
						fil.read(),
						Name=basename(f)
					)
					# After the file is closed
					print('TWO')
					part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
					print('THREE')
					msg.attach(part)
					print('FOUR')

			server= smtplib.SMTP_SSL("smtp.zoho.com", 465)
			print('FIVE')
			server.login(self.cfg.email_model_email, self.cfg.email_model_access_key)

			server.sendmail(self.cfg.email_model_email, [recipent], msg.as_string())
			server.quit()
		except Exception as e:
			print(e)
