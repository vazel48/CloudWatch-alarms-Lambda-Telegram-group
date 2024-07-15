**AWS CloudWatch to Telegram Notifier**
This Python script was made to be used as an AWS Lambda function that sends AWS CloudWatch alarm notifications to a specified Telegram chat. It utilizes the Telegram Bot API to deliver messages.

**We need:**
- Telegram BOT token (BotFather will help you)
- Telegram chat ID where the notifications will be sent. (add @getmyid_bot or similar to your target tlg group to get "Current chat ID")
- Lambda function with basic IAM role (an auto-created role is enough)
- Our Python code. It utilizes libraries supported by the Lambda runtime, allowing us to add it to the function directly without creating a package.
- Proper configuration of environment variables in the Lambda function. (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)
- **Resource-based policy statement** that allows us to trigger our Lambda by CloudWatch alarm.
  Lambda - Configuration - Permissions - Resource-based policy statements - https://prnt.sc/LaBZ7xmq8UqN
- CloudWatch Alarm with action to trigger our Lambda function.

Once set up, our Lambda function will process event JSON from the CloudWatch alarm and automatically send a formatted notification message to the specified Telegram chat whenever a CloudWatch alarm is triggered.
The alarm message includes details such as alarm name, status change, account ID, region, instance ID, timestamp, description, and reason for the alarm.

**Error Handling**
If the function encounters an error while sending the message, it will log the error and return a status code 500 with an error message.
