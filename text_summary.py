import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Born and raised in Mumbai, Dixit made her acting debut in 1984 with a leading role in the drama Abodh. 
After a few successive commercially failed films, she rose to prominence with the action drama Tezaab (1988), and established herself with starring roles in the top-grossing romantic 
dramas Dil (1990), Beta (1992), Hum Aapke Hain Koun..! (1994), and Dil To Pagal Hai (1997). 
She won four Filmfare Awards for Best Actress for her performances in them. Her other commercially successful films during this period include Ram Lakhan (1989), Tridev (1989), Thanedaar (1990), 
Kishen Kanhaiya (1990), Saajan (1991), Khalnayak (1993), and Raja (1995). """


def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    # print(doc)
    tokens = [token.text for token in doc]
    # print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1

    # print(word_freq)

    max_freq = max(word_freq.values())
    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text] 

    # print(sent_scores)

    select_len = int(len(sent_tokens) * 0.3)
    # print(select_len)

    summary = nlargest(select_len, sent_scores, key=sent_scores.get)
    # print(summary)

    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(summary)
    # print("Length of original text ",len(text.split(' ')))
    # print("Length of summary text ",len(summary.split(' ')))

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))