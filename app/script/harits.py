import wikipedia
import nltk
import re
import statistics
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import math
from operator import itemgetter

def fungsi_adi(masukan):
    p = wikipedia.page(str(masukan))
    content = p.content.split("References")[0]
    content = content.split('See also')[0]

    def remove_s(s):
        content = re.sub(r'[=]*[a-zA-Z ü]*[=]+', '', s)
        content = re.sub(r'[\n]+', ' ', content)
        content = re.sub(r'[–:<>+=_`~!@#$%^&*;,\'()/.\"0-9-]+', ' ', content)
        content = re.sub(r'[ ]+', ' ', content)

        return content

    def count_words(sent):
        count = 0
        words = word_tokenize(sent)
        for word in words:
            count+=1
        return count

    def create_freq_dict(sents):
        i=0
        freqDict_list=[]
        for sent in sents:
            i+=1
            freq_dict={}
            words=word_tokenize(sent)
            for word in words:
                word=word.lower()
                if word in freq_dict:
                    freq_dict[word]+=1
                else:
                    freq_dict[word]=1
                temp = {'doc_id' : i, 'freq_dict' : freq_dict}
            freqDict_list.append(temp)
        return freqDict_list

    def get_doc(sent):
        doc_info=[]
        i=0
        for s in sent:
            i+=1
            count = count_words(s)
            temp = {'doc_id' : i, 'doc_length' : count}
            doc_info.append(temp)
        return doc_info

    def computeTF(doc_info, freqDic_list):
        TF_scores=[]
        for tempDict in freqDic_list:
            id=tempDict['doc_id']
            for k in tempDict['freq_dict']:
                temp={'doc_id' : id,
                      'TF_score' : tempDict['freq_dict'][k]/doc_info[id-1]['doc_length'],
                      'key' : k
                }
                TF_scores.append(temp)
        return TF_scores

    def computeIDF(doc_info, freqDic_list):
        IDF_scores=[]
        counter=0
        for dict in freqDic_list:
            counter+=1
            for k in dict['freq_dict'].keys():
                count = sum([k in tempDict['freq_dict'] for tempDict in freqDic_list])
                temp = {'doc_id' : counter, 'IDF_score' : math.log(len(doc_info)/count), 'key' : k}
                IDF_scores.append(temp)
        return IDF_scores

    def compute_TFIDF(TF_scores, IDF_scores):
        TFIDF_scores=[]
        for j in IDF_scores:
            for i in TF_scores:
                if j['key'] == i['key'] and j['doc_id'] == i['doc_id']:
                    temp={'doc_id' : j['doc_id'],
                          'TFIDF_score' : j['IDF_score']*i['TF_score'],
                          'key' : i['key']}
            TFIDF_scores.append(temp)
        return TFIDF_scores

    text_sent = sent_tokenize(content)
    text_sents = [remove_s(s) for s in text_sent]
    doc_info = get_doc(text_sents)

    freqDict_list = create_freq_dict(text_sents)
    TF_scores=computeTF(doc_info, freqDict_list)
    IDF_scores=computeIDF(doc_info, freqDict_list)

    TFIDF_scores=compute_TFIDF(TF_scores, IDF_scores)

    def get_sent_score(TFIDF_scores, text_sents, doc_info):
        sentence_info=[]
        for doc in doc_info:
            sent_score=0
            for i in range(0, len(TFIDF_scores)):
                temp_dict = TFIDF_scores[i]
                if doc['doc_id'] == temp_dict['doc_id']:
                    sent_score+=temp_dict['TFIDF_score']
            temp={'doc_id' : doc['doc_id'], 'sent_score' : sent_score,
                  'sentence' : text_sents[doc['doc_id']-1]}
            sentence_info.append(temp)
        return sentence_info

    sentence_info = get_sent_score(TFIDF_scores, text_sents, doc_info)
    sentence_info = sorted(sentence_info, key=itemgetter('doc_id'))

    def get_summary(sentence_info):
        sum=0
        summary=[]
        array=[]
        for temp_dict in sentence_info:
            sum+=temp_dict['sent_score']
        avg=sum/len(sentence_info)
        for temp_dict in sentence_info:
            array.append(temp_dict['sent_score'])
        stdev = statistics.stdev(array)
        for sent in sentence_info:
            if(sent['sent_score']) >= avg:
                summary.append(sent)
        return summary

    summary=get_summary(sentence_info)
    # result = sorted(summary, key=itemgetter('sent_score'), reverse=True)
    result = sorted(summary[:7], key=itemgetter('doc_id'))

    guud=""
    guud+=text_sent[0]

    for i in result:
        if i['doc_id']!=1:
            a=i['doc_id']
            guud+=(" "+text_sent[a-1])
    return guud



