import json
import os
import boto3

ACC_NUM = os.getenv("account_num")
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event, indent=2))
        alerts = event.get("alerts", [])
        for alert in alerts:
            alert_name = alert.get("labels", {}).get("alertname", "UnknownAlert")
            summary = alert.get("annotations", {}).get("summary", "No summary provided")
            description = alert.get("annotations", {}).get("description", "No summary provided")
            namespace = alert.get("labels", {}).get("namespace", "UnknownNamespace")

            # Create a message for SNS
            message = {
                "AlertName": alert_name,
                "Summary": summary,
                "Description": description,
                "Namespace": namespace
            }
            print(f"Sending alert: {message}")
            response = sns_client.publish(
                TopicArn=f"arn:aws:sns:us-east-1:{ACC_NUM}:prometheus-alerts",
                Message=json.dumps(message),
                Subject=f"Alert: {alert_name}"
            )
            print(f"Published to SNS: {response}")
        
        return {
            "statusCode": 200,
            "body": json.dumps("Alerts processed and sent to SNS!")
        }
    except Exception as e:
        print(f"Error processing alerts: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error: {str(e)}")
        }

