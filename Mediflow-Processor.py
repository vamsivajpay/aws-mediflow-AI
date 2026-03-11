import boto3
import json
import random
from datetime import datetime

bedrock = boto3.client(service_name='bedrock-runtime')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('2358480_PatientFeedback')

def lambda_handler(event, context):
    try:
        if 'sessionState' in event:
            slots = event['sessionState']['intent']['slots']
            patient_text = slots['patient_story']['value']['interpretedValue']
            intent_name = event['sessionState']['intent']['name']
        else:
            patient_text = event.get('test_input', "Feedback text here")
            intent_name = "ProvideFeedback"
    except Exception:
        return build_lex_response("Error reading input.", "Failed", "ProvideFeedback")

    # ID Generation
    call_id = f"{datetime.now().strftime('%y%m')}-{random.randint(100000, 999999)}"

    # Prompt with Red/Yellow/Green rules
    system_prompt = f"""
    Analyze this healthcare feedback: "{patient_text}"
    Rules:
    - NEGATIVE sentiment -> color_tag: RED
    - NEUTRAL sentiment -> color_tag: YELLOW
    - POSITIVE sentiment -> color_tag: GREEN
    Return ONLY a JSON array with issue_id, issue_title, sentiment, and color_tag.
    """

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": system_prompt}]
    })

    try:
        response = bedrock.invoke_model(modelId='anthropic.claude-3-5-sonnet-20240620-v1:0', body=body)
        raw_ai_text = json.loads(response.get('body').read())['content'][0]['text']
        structured_issues = json.loads(raw_ai_text[raw_ai_text.find('['):raw_ai_text.rfind(']')+1])
        
        # Determine Overall Severity (Red > Yellow > Green)
        tags = [i.get('color_tag', 'YELLOW') for i in structured_issues]
        if 'RED' in tags:
            overall_sev = 'RED'
        elif 'YELLOW' in tags:
            overall_sev = 'YELLOW'
        else:
            overall_sev = 'GREEN'

    except Exception as e:
        print(f"Error: {e}")
        return build_lex_response("AI processing failed.", "Failed", intent_name)

    # Save to DynamoDB
    table.put_item(
        Item={
            'FeedbackID': call_id,
            'EntityName': 'ANALYSIS_REPORT',
            'RawText': patient_text,
            'Issues': structured_issues,
            'OverallSeverity': overall_sev,
            'Timestamp': datetime.now().isoformat()
        }
    )

    return build_lex_response(f"Recorded. Reference ID: {call_id}.", "Fulfilled", intent_name)

def build_lex_response(message, state, intent_name):
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {"name": intent_name, "state": state}
        },
        "messages": [{"contentType": "PlainText", "content": message}]
    }