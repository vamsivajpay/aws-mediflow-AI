# Lex-Bedrock Intelligence Engine

This component serves as the automated reasoning layer for the **aws-mediflow-AI** pipeline. It orchestrates the flow between conversational input, generative AI analysis, and persistent storage.

---

### Logic Workflow

* **Lex Trigger**: The function is invoked as a code hook when a patient provides feedback via Amazon Lex.
* **AI Orchestration**: It extracts the raw transcript and passes it to **Claude 3.5 Sonnet (via Amazon Bedrock)** with a specialized system prompt.
* **Sentiment Tagging**: The AI categorizes the feedback into a structured JSON format, assigning color-coded severity tags:
    * **RED**: Negative sentiment (Urgent attention required).
    * **YELLOW**: Neutral sentiment (Standard follow-up).
    * **GREEN**: Positive sentiment (Service commendation).
* **State Persistence**: The analyzed data, including an auto-generated Reference ID and overall severity score, is saved to **Amazon DynamoDB**.

---

### Technical Integration

* **Amazon Lex**: Extracts the `patient_story` slot value from the intent session state.
* **Amazon Bedrock**: Utilizes `anthropic.claude-3-5-sonnet` for advanced NLP and structured JSON output.
* **Amazon DynamoDB**: Stores the final analysis report using a partition key (`FeedbackID`) and sort key (`EntityName`).
* **Boto3**: Manages the runtime clients for seamless cross-service communication.

---

### Environment Configuration

To ensure this code executes correctly, the following must be configured:

1.  **IAM Permissions**: The Lambda execution role requires `bedrock:InvokeModel`, `dynamodb:PutItem`, and `logs:CreateLogGroup`.
2.  **Table Name**: The DynamoDB table must be named `2358480_PatientFeedback`.
3.  **Model Access**: Amazon Bedrock model access for Claude 3.5 Sonnet must be enabled in the AWS Region.

---

### Output Schema
The function returns a **Lex Close Dialog Action**, providing the user with a unique Reference ID and setting the intent state to `Fulfilled`.
