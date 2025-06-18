from transformers import pipeline
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import base64
import email

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8080)
    return build('gmail', 'v1', credentials=creds)

def read_latest_email():
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', labelIds=['SENT'], maxResults=10).execute()
    messages = results.get('messages', [])

    if not messages:
        print("ไม่มีอีเมลในกล่องส่ง")
        return

    for idx, message in enumerate(messages, start=1):
        msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
        raw_data = msg['raw']

        # ถอดรหัส base64 urlsafe
        msg_str = base64.urlsafe_b64decode(raw_data).decode("utf-8", errors="ignore")
        mime_msg = email.message_from_string(msg_str)

        subject = mime_msg.get('Subject', '(ไม่มีหัวข้อ)')
        print(f"\n--- Email {idx} ---")
        print("Subject:", subject)

        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    if body:
                        print("Body:", body.decode(errors="ignore"))
                        break
        else:
            body = mime_msg.get_payload(decode=True)
            if body:
                print("Body:", body.decode(errors="ignore"))

read_latest_email()

'''
text = """
        In earlier years, probabilistic models were used for suspect prioritization [14] and linking
 criminal styles with offender characteristics [15]. Others have used semantic search
 for exploratory applications [16]. A model based around latent semantic indexing and
 WordNet [17] achieved promising results for retrieving suspicious emails based on an
 investigator’s query. Recently, as for most other fields within natural language processing,
 performance on semantic similarity has shown significant improvement with transformer
based models [18,19,20]. For similarity and retrieval, embeddings of both words and
 sentences play a key role in many of the latest models. Influential embedding techniques
 include word2vec [21], GloVe [22] and ELMo [23]. Sentence embeddings have achieved
 state-of-the-art performance for semantic retrieval [24], and sentence-BERT [18] has
 become a popular modeling scheme, available for a large selection of languages. The
 model used here is trained with the Norwegian nb-bert-base model [25].1 For court
 decisions, the task of extracting events and their components (what, when and who)was
 evaluated with a large selection of BERT-based models [26], compared against CRF
 (conditional random fields) [27] and Flair embeddings [28], where fine-tuned BERT
 models outperformed the alternatives [29]
        """

words = text.split()



def summarize_text(text):
    summary = summarizer(text, max_length=200, min_length=(int)(len(words)/2), do_sample=True)
    return summary[0]['summary_text']

print("ข้อความที่สรุปออกมา:",summarize_text(text))
'''