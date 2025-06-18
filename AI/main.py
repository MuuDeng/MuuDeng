from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

text = """Motivation: The quantity of criminal cases year 2009 in Taiwan is up to 1.8 millions, Each prosecutor 
        must handle over 211 cases per month, complaints on over loading is laud and clear. While 70% of 
        criminal cases are drug Abuse, public danger, larceny and fraud, these types of criminal cases may 
        have different story though, the complexity are relative simple than cases of killing, corruption etc., 
        but prosecutors still spend costly time on these cases handling. In this paper we try to use text mining 
        technology to provide solution on this issue. 
        Approach: We use the police’s investigation document of criminal case to compare with judgment 
        history of court, and use Cosine Similarity algorithm to calculate coefficient of similarity, base on the 
        highest coefficient, we find the closest judgment of this type of criminal case, that can be used to 
        decide and generate the draft of indictment for prosecutor."""


def summarize_text(text):
    summary = summarizer(text, max_length=200, min_length=200, do_sample=True)
    return summary[0]['summary_text']

print("ข้อความที่สรุปออกมา:",summarize_text(text))