Project Overview
This repository contains an autonomous feedback intelligence system designed for healthcare environments. The project creates an end-to-end automated pipeline that captures patient feedback and converts it into high-priority alerts and executive reports. By moving away from manual data entry, the system ensures that urgent patient concerns are identified and escalated in real time.
--------------------------------------------------
Core Features
Conversational Data Capture: Uses a natural language interface to gather unstructured feedback from users.

Automated Orchestration: Employs a serverless heartbeat to manage daily reporting cycles without human intervention.

Intelligent Sentiment Analysis: Processes raw text to isolate critical issues and categorize them by severity.

Proactive Notification: Delivers formatted summaries and urgent notifications directly to management inboxes.

Trend Visibility: Provides structured summaries of operational performance and service trends.
--------------------------------------------------
Architecture Flow
Input: Amazon Lex captures the patient's voice or text feedback.

Storage: Raw interactions are stored in Amazon DynamoDB and Amazon S3 for record-keeping.

Trigger: Amazon EventBridge initiates a scheduled daily review of all stored feedback.

Analysis: AWS Lambda orchestrates Amazon Bedrock (Claude 3.5) to analyze sentiments and summarize the day's data.

Output: Amazon SNS pushes the final report and any high-priority alerts to the designated stakeholders.
--------------------------------------------------
Technical Stack
Conversational Interface: Amazon Lex

Compute: AWS Lambda

Orchestration: Amazon EventBridge

AI Integration: Amazon Bedrock (Claude 3.5)

Messaging: Amazon SNS

Storage: Amazon DynamoDB, Amazon S3

Analytics: Amazon Athena
--------------------------------------------------
Deployment
This project is built using a serverless architecture, ensuring high scalability and low operational cost. Deployment requires the configuration of the Lex Bot for data ingestion and the setup of EventBridge rules to trigger the analysis Lambda functions.
