import time
import gspread
import datetime
from mailchimp3 import MailChimp

# inputs:   email id (from the spreadsheet)
#           date (also spreadsheet, depending on which type of email)
#           the position of the id in the spreadsheet
#               *remember it breaks convention (starts at 1, not 0)*
#               *0 = weekly, 1 = biweekly, 2 = monthly*

def send_email(email_id, type):
    # to find out API key, go to Account >> Extras >> API Keys
    # please warn everyone else before doing anything with the keys
    print("\nOpening MailChimp account...")
    client = MailChimp(mc_api = 'API SECRET KEY', mc_user = 'USERNAME')
    print("Account Oppened")

    # gets current campaigns
    campaigns = client.campaigns.all(fields="campaigns.create_time,campaigns.id,campaigns.recipients")

    # creates a variable that stores the information of the campaign currently in use
    print("\nGetting current campaign's info...")
    current_campaign = client.campaigns.get(campaign_id = email_id)
    print("Done!")

    # sends the campaign currently in use, waits 20 sec for it to send and then deletes it
    print("\nSending the email")
    client.campaigns.actions.send(campaign_id = email_id)
    print("Please wait...")
    # it takes some time for the email to send
    time.sleep(20)
    # replicates the current email and gets its ID
    new_campaign = client.campaigns.actions.replicate(campaign_id = email_id)
    print("Done!\nNow deleting the previous email...")
    client.campaigns.delete(campaign_id = email_id)

    # writes the new id to the spreadsheet
    today = datetime.datetime.now()
    worksheet.update_cell(type+2,1,today.year)
    worksheet.update_cell(type+2,2,today.month)
    worksheet.update_cell(type+2,3,today.day)
    worksheet.update_cell(1,type+1,str(new_campaign['id']))
    print("New campaign id: ", str(new_campaign['id']))
    print("\nAll Finished!\n")

def check_date(type):
	today = datetime.datetime.now()
	prev = datetime.datetime(int(data[type+1][0]),int(data[type+1][1]),int(data[type+1][2]))
	dif = today - prev
	return dif.days

while True:
    # waits for 5 hours before running the code again
    time.sleep(60)

    # opens the google account and the sheet through the key
    print("\nOpening Google Account and Spreadsheet...")
    account = gspread.service_account(filename = 'credentials.json')
    sheet = account.open_by_key('GOOGLE SHEET KEY')
    worksheet = sheet.sheet1
    data = worksheet.get_all_values()
    print("Done!")
    # D1 has the information that tells whether the code shuold run or not
    # 	it can be either ON or OFF (if anything other than ON is in there, it will
    # 	just be OFF)
    if (data[0][3].lower() != 'on'):
        print("\nApplication turned off by the Spread Sheet.")
        worksheet.update_cell(10,10,"Turned off through spread sheet")
    else:
        # previous email sent date and current date for each email (Format = YMD)
        print("\nChecking if it is time to send the emails...")
        send_weekly = check_date(0)
        send_biweekly = check_date(1)
        send_monthly = check_date(2)

        if send_weekly >= int(data[1][4]):
            print("\nTime to send the weekly email!")
            send_email(data[0][0],0)
        else:
            print("\nIt's not time for the weekly email yet\nTime since the last weekly email: ", send_weekly)

        if send_biweekly >= int(data[2][4]):
            print("\nTime to send the bi-weekly email!")
            send_email(data[0][1],1)
        else:
            print("\nIt's not time for the bi-weekly email yet\nTime since the last biweekly email: ", send_biweekly)

        if send_monthly >= int(data[3][4]):
            print("\nTime to send the monthly email!")
            send_email(data[0][2],2)
        else:
            print("\nIt's not time for the monthly email yet\nTime since the last monthly email: ", send_monthly)
