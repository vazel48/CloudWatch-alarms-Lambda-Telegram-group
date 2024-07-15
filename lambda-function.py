import json
import os
import urllib3

# Initialize HTTP client
http = urllib3.PoolManager()

# Telegram Bot API settings
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def lambda_handler(event, context):
    try:
        # Extract relevant information from the event
        alarm_name = event.get('alarmData', {}).get('alarmName', 'N/A')
        alarm_description = event.get('alarmData', {}).get(
            'configuration', {}).get('description', 'N/A')
        new_state = event.get('alarmData', {}).get(
            'state', {}).get('value', 'N/A')
        previous_state = event.get('alarmData', {}).get(
            'previousState', {}).get('value', 'N/A')
        timestamp = event.get('time', 'N/A')
        account_id = event.get('accountId', 'N/A')
        region = event.get('region', 'N/A')
        alarm_reason = event.get('alarmData', {}).get(
            'state', {}).get('reason', 'N/A')

        # Extract instance ID if available
        instance_id = 'N/A'
        metrics = event.get('alarmData', {}).get(
            'configuration', {}).get('metrics', [])
        if metrics:
            dimensions = metrics[0].get('metricStat', {}).get(
                'metric', {}).get('dimensions', {})
            instance_id = dimensions.get('InstanceId', 'N/A')

        # Construct message
        message = f"""
🚨 *AWS CloudWatch Alarm*

*Alarm Name:* {alarm_name}
*Status Change:* {previous_state} → {new_state}

*Account ID:* {account_id}
*Region:* {region}
*Instance ID:* {instance_id}
*Time:* {timestamp}

*Description:* {alarm_description}

*Reason:* {alarm_reason}

Good Luck! 🍀"""

        # Send message to Telegram
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }

        response = http.request('POST', TELEGRAM_API_URL, fields=payload)

        if response.status != 200:
            raise ValueError(
                f"Request to Telegram API failed: {response.data.decode('utf-8')}")

        return {
            'statusCode': 200,
            'body': json.dumps('Message sent successfully')
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error sending message')
        }
