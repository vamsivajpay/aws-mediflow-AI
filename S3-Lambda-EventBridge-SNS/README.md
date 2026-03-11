# Mediflow Reporting and Notification Module

This component handles the aggregation of daily feedback metrics and the automated delivery of executive summaries to hospital supervisors. It functions as the outbound communication layer of the **aws-mediflow-AI** ecosystem.

---

### Logic Workflow

* **Scheduled Trigger**: Typically invoked by an Amazon EventBridge cron rule to generate end-of-day summaries.
* **Data Aggregation**: 
    - Scans the **S3 Analytics Lake** for objects matching the current date.
    - Parses JSON payloads to calculate cumulative sentiment scores (Positive, Negative, Neutral).
    - Compiles a detailed list of identified issues and their respective severity levels.
* **Report Generation**: Dynamically formats a plain-text email body containing total sentiment counts and a detailed issue list.
* **Automated Dispatch**: Publishes the final report to an **Amazon SNS Topic**, which instantly distributes it to all subscribed supervisor email addresses.

---

### Technical Integration

* **Amazon S3**: Acts as the source data lake (`2358480-mediflow-analytics-lake`) where processed analysis files are stored.
* **Amazon SNS**: Manages the fan-out distribution of reports to the designated `Supervisor_Report_Topic`.
* **Boto3**: Utilizes S3 and SNS clients to fetch objects and publish messages.
* **Python Datetime**: Ensures the module only processes records corresponding to the current calendar day.

---

### Environment Configuration

To ensure successful report delivery, the following configurations are required:

1.  **IAM Permissions**: The Lambda role must have `s3:ListBucket`, `s3:GetObject`, and `sns:Publish` permissions.
2.  **Resource ARNs**: The SNS Topic ARN and S3 Bucket name must match the environment-specific identifiers defined in the source code.
3.  **SNS Subscription**: Supervisors must have confirmed their email subscriptions to the SNS Topic to receive the automated reports.

---

### Sample Output Format
The module generates a structured email including:
- **Hospital Feedback Summary Header**
- **Total Sentiment Counts** (Aggregated Pos/Neg/Neu scores)
- **Detailed Issue List** (Formatted with Severity levels)
