import gspread
import datetime

# Checks the current date, comparing it with the
def check_date(type):
	today = datetime.datetime.now()
	prev = datetime.datetime(int(data[type+1][0]),int(data[type+1][1]),int(data[type+1][2]))
	dif = today - prev
	return dif.days

def send_email(email_id,type):
	print("Email ID: ", email_id)
	str = "unknown"
	if type == 0: str = "weekly"
	elif type == 1: str = "bi-weekly"
	elif type == 2: str = "monthly"
	print("Email type: ", str)

# opens the google account and the sheet through the key
print("\nOpening Google Account and Spreadsheet...")
account = gspread.service_account(filename = 'credentials.json')
sheet = account.open_by_key('GOOGLE SHEET KEY')
worksheet = sheet.sheet1
data = worksheet.get_all_values()
print("Done!")

# previous email sent date and current date for each email (Format = YMD)
send_weekly = check_date(0)
send_biweekly = check_date(1)
send_monthly = check_date(2)

if send_weekly >= 7:
	print("\nTime to send the weekly email!")
	# send_email(data[0][0],0)
else:
    print("It's not time for the weekly email yet")

if send_biweekly >= 14:
	print("\nTime to send the bi-weekly email!")
	# send_email(data[0][1],1)
else:
    print("It's not time for the bi-weekly email yet")

if send_monthly >= 30:
	print("\nTime to send the monthly email!")
	# send_email(data[0][2],2)
else:
    print("It's not time for the monthly email yet")
