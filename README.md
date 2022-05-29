# passport_checker
Script to send me an email notification when my polish passport is ready for pickup.

Instructions:

1. Run 'pip install -r requirements.txt' to install of the required packages.

2. Populate 'work_ids_to_check.csv' with the correct passport work_ids 
(16 digit number under the barcode of your reciept), as well as the email 
you'd like a notification to if the passport from that work_id is ready.

3. The password for the admin email account (used for sending the emails) is redacted.
To have this script work you would need to provide the login credentials to your own account.
Ie. update 'ADMIN_EMAIL' and 'ADMIN_PASSWORD'

4. Schedule program as necessary. I scheduled this python to run on computer startup, 
using Windows Task Scheduler. (Option 2 from here: 
https://www.geeksforgeeks.org/schedule-a-python-script-to-run-daily/)
