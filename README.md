Project Overview
This repository contains a serverless intelligence system that automates the feedback lifecycle. The project captures patient interactions, performs AI-driven analysis, and escalates critical issues to leadership without manual intervention.

Core Features
Conversational Intake: Captures unstructured feedback via natural language interfaces.

Autonomous Reporting: Removes manual data processing using scheduled event triggers.

Sentiment Intelligence: Categorizes feedback by severity to highlight urgent concerns.

Direct Escalation: Delivers high-priority alerts and executive summaries to inboxes.

Architecture Flow
Intake: Amazon Lex collects user feedback through voice or text.

Persistence: Data is stored in Amazon DynamoDB and S3 for processing.

Orchestration: Amazon EventBridge triggers the analysis engine on a schedule.

Intelligence: AWS Lambda and Amazon Bedrock analyze and summarize the feedback.

Delivery: Amazon SNS broadcasts the final reports and urgent notifications.

Technical Stack
AI and ML: Amazon Lex, Amazon Bedrock

Compute: AWS Lambda

Events: Amazon EventBridge

Storage: Amazon DynamoDB, Amazon S3

Notifications: Amazon SNS

Analysis: Amazon Athena

Deployment
This project is built on a serverless stack for scalability and cost-efficiency. Setup requires configuring the Lex bot for data ingestion and defining the EventBridge rules for the automated reporting cycle.
