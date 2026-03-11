import boto3
import json
from datetime import datetime

s3 = boto3.client('s3')
sns = boto3.client('sns')

BUCKET_NAME = '2358480-mediflow-analytics-lake'
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:189243246970:2358480_Supervisor_Report_Topic'

def lambda_handler(event, context):
    today = datetime.now().strftime('%Y-%m-%d')
    report_items = []
    pos, neg, neu = 0, 0, 0
    
    # 1. List all files in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    
    if 'Contents' not in response:
        return {"body": "No files found"}

    for obj in response['Contents']:
        # 2. Only read files from "today"
        file_content = s3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
        data = json.loads(file_content['Body'].read().decode('utf-8'))
        
        if data.get('report_date') == today:
            pos += data.get('pos_score', 0)
            neg += data.get('neg_score', 0)
            neu += data.get('neu_score', 0)
            report_items.append(f"- {data['overall_severity']}: {data['issue_summary']}")

    # 3. Format the Email Message
    email_body = f"""
    HOSPITAL FEEDBACK SUMMARY: {today}
    ----------------------------------
    TOTAL SENTIMENT COUNTS:
    - Positive: {pos}
    - Negative: {neg}
    - Neutral: {neu}
    
    DETAILED ISSUE LIST:
    {chr(10).join(report_items)}
    
    This is an automated report from the Mediflow Analytics Lake.
    """

    # 4. Send the Email
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:189243246970:2358480_Supervisor_Report_Topic',
        Subject=f"Daily Patient Feedback Report - {today}",
        Message=email_body
    )
    
    return {"status": "Report Sent"}