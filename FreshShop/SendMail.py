import smtplib #登陆邮件服务器，进行邮件发送
from email.mime.text import MIMEText #负责构建邮件格式

subject = "周日学习"
content = "业精于勤荒于嬉，行成于思毁于随，good good study day day up"
sender = "clw825@foxmail.com"
recver = """3392279511@qq.com,
215558997@qq.com,
773733859@qq.com,
912575770@qq.com,
1529825704@qq.com,
1307128051@qq.com,
721788741@qq.com,
3303236612@qq.com,
710731910@qq.com,
329688391@qq.com,
626978318@qq.com,
419538402@qq.com,
1637805820@qq.com,
738389368@qq.com,
329688391@qq.com,
1225858108@qq.com,
329688391@qq.com,
1225858108@qq.com"""

password = "iznolwomwsvmgeec"

message = MIMEText(content,"plain","utf-8")
message["Subject"] = subject
message["To"] = recver
message["From"] = sender

smtp = smtplib.SMTP_SSL("smtp.qq.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
smtp.close()

