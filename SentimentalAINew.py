import sys
import requests
import json
# Client ID/Secret/http_API/
client_id = "02ydbo5p9q"
client_secret = "d2ak5TVswGD9fsnNfBxNKPsHitPixoNCL9sqePTl"
url="https://naveropenapi.apigw.ntruss.com/sentiment-analysis/v1/analyze"
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret,
    "Content-Type": "application/json"
}

# Note1. 각 함수들이 호출하는 sentiment AI API는 모두 같음. 그럼 하나의 함수를 사용하는게 좋습니다.
# Note2. __를 붙여서 외부에서 부르는 
def __getSentiment(userContent):
    data = {
        "content" : userContent
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if(response.status_code == 200):
        return json.loads(response.text)
    else:
        print("Error : " + response.text)
        raise Exception(str(response.status_code)) # Note2. Error인 경우 아무것도 명시하지 않음. return을 해주거나 exception을 일으켜주어서 마감을 해줄 필요가 있음 #1. Error인 경우 아무것도 명시하지 않음. return을 해주거나 exception을 일으켜주어서 마감을 해줄 필요가 있음. 그래야지 이 함수를 호출하는 곳에서 거기에 맞는 처리를 할 수가 있음

# Note3. 공통으로 사용하는 기능을 함수로 분리하여 재사용합니다.
def __displayOutSentences(message, sentences):
    print (message)
    for sentence in sentences: print (sentence)
    print ('\n')

# Note4. 함수는 하나의 목적을 갖는게 좋습니다.
# Feedback for user Situation content
def getSituationFeedback():
    data = input("오늘의 감정을 느끼게 한 사건은 무엇이었나요? 주관적인 표현을 빼고 객관적인 표현을 사용하여 최대한 간단 명료하게 써 보아요.\n")
    print ('\n')
    while True:
        # Note4. 앞서 Exception raise 하는 것을 try except로 처리해줍니다.
        try:
            sentiment = __getSentiment(data)
            sentimentScore = sentiment.get("document").get("confidence")
            neutralScore = sentimentScore['neutral']
            negativeScore = sentimentScore['negative']
            positiveScore = sentimentScore['positive']
            sentences = sentiment.get('sentences')
        except Exception as e:
            print ('API Error : ', str(e))

        # Note5. 배열을 사용하는게 자연스러워보입니다.
        negativeSentences = []
        positiveSentences = []

        # feedback message 길이로 판단하는 것보다는 정확한 data로 판단하는게 정확합니다.
        if neutralScore > 30:
            print("사건을 생각과 감정으로부터 분리하여 객관적으로 잘 작성하셨습니다.")
            break

        for sentence in sentences:
            if sentence['sentiment'] == 'negative': negativeSentences.append(sentence['content'])
            elif sentence['sentiment'] == 'positive': positiveSentences.append(sentence['content'])

        if negativeScore > positiveScore:
            print('사건을 기술한 글에서 부정적 감정이 느껴져요. 혹시 사건을 부정적인 시각에 치우쳐 바라본 것은 아닐까요?\n')
            negativeGuideMessage = "다음 문장들이 부정적인 감정에 치우친 문장들입니다.\n "
            __displayOutSentences(negativeGuideMessage, negativeSentences)
        else:
            print('사건을 표현한 글에서 다양한 감정이 느껴져요. 중립적으로 바라보지 못한다면 효과적인 상담이 어려울 수 있어요.\n')
            positiveGuideMessage = "다음 문장들이 감정에 치우친 문장들입니다.\n "
            __displayOutSentences(positiveGuideMessage, positiveSentences)
        data = input("위의 피드백을 바탕으로 다시 한 번 일어난 일을 써 볼까요?\n")
        print ('\n')

if __name__ == '__main__': # Note3. 이 곳에서부터 시작됨
    getSituationFeedback()
#    getThoughtFeedback()
#    getEmotionFeedback()
#    getBehaviorFeedback()