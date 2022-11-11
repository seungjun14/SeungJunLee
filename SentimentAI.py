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

# Get Negative/Positive/Neutral scores from CLOVA Sentiment API
def getSentimentScore(userContent):
    data = {
        "content" : userContent
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if(response.status_code == 200):
        sentimentScore = json.loads(response.text).get("document").get("confidence")
        return sentimentScore
    else:
        print("Error : " + response.text)
 
# Feedback for user Situation content
def getSituationFeedback(situationContent):
    data = {
        "content" : situationContent
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    sentimentScore = json.loads(response.text).get("document").get("confidence")
    negativeSentences = "다음 문장들이 부정적인 감정에 치우친 문장들입니다.\n "
    sentimentSentences = "다음 문장들이 감정에 치우친 문장들입니다.\n "
    for sentences in json.loads(response.text).get("sentences"):
        if sentences["sentiment"] == "negative": 
            negativeSentences += sentences["content"] + "\n"
            sentimentSentences += sentences["content"] + "\n"
        if sentences["sentiment"] == "positive": sentimentSentences += sentences["content"] + "\n"
    if(sentimentScore["neutral"] > 30):
        return "사건을 생각과 감정으로부터 분리하여 객관적으로 잘 작성하셨습니다."
    elif(sentimentScore["negative"] > sentimentScore["positive"]):
        return "사건을 기술한 글에서 부정적 감정이 느껴져요. 혹시 사건을 부정적인 시각에 치우쳐 바라본 것은 아닐까요?\n" + negativeSentences
    else:
        return "사건을 표현한 글에서 다양한 감정이 느껴져요. 중립적으로 바라보지 못한다면 효과적인 상담이 어려울 수 있어요.\n" + sentimentSentences
        
# Feedback for user Thought content
def getThoughtFeedback(thoughtContent):
    data = {
        "content" : thoughtContent
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    sentimentScore = json.loads(response.text).get("document").get("confidence")
    if(sentimentScore["negative"] > 95):
        return "'생각'란에는 감정을 느끼기 전, 사건을 바라보는 '나'의 해석을 써야 합니다. 지금 써 주신 '생각'에는 이미 감정이 포함되어 있습니다."
    elif(sentimentScore["positive"] > 95):
        return "'생각'란에는 감정을 느끼기 전, 사건을 바라보는 '나'의 해석을 써야 합니다. 지금 써 주신 '생각'에는 이미 감정이 포함되어 있습니다."
    else:
        return "사건에 대한 해석을 감정과 분리하여 잘 작성하셨습니다."

# Feedback for user Emotion content
def getEmotionFeedback(emotionContent):
    data = {
        "content" : emotionContent
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    sentimentScore = json.loads(response.text).get("document").get("confidence")
    if(sentimentScore["negative"] > 99):
        return "긍정적이지 못한 감정이 느껴졌군요. 나쁜 감정은 발생하는 것만으로 고통스러울 수 있습니다. 이런 감정에 어떻게 행동하셨나요?"
    elif(sentimentScore["positive"] > 99):
        return "긍정적인 감정을 느꼈다니 다행입니다. 그 후에는 어떻게 행동하셨나요?"
    else:
        return "사건에 대한 감정을 조금 더 직접적으로 명시해주어야 합니다. 감정은 최대한 간결하게 표현할수록 정확하게 인지할 수 있습니다. '사건'에 대한 '생각'과 '감정'을 헷갈리는 분들도 많답니다."
        
# Feedback for user Behavior content
def getBehaviorFeedback(behaviorContent):
    data = {
        "content" : behaviorContent
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    sentimentScore = json.loads(response.text).get("document").get("confidence")
    if(sentimentScore["negative"] > 95):
        return "조금은 감정적인 행동을 한 것으로 보이네요. 스스로의 행동에 대해 어떻게 생각하시나요?"
    elif(sentimentScore["negative"] > 50):
        return "감정에 휩싸인 행동을 하지는 않아 다행이에요. 이제 오늘 일에 대해 느낀점을 말해보아요."
    else:
        return "감정을 잘 절제하여 다행입니다. 이제 오늘을 돌아보며 느낀점에 대해 얘기해볼까요?"

# 감정일기 작성 보조 인공지능
def getCognitiveBehaviorTherapy():
    situation = input("오늘의 감정을 느끼게 한 사건은 무엇이었나요? 주관적인 표현을 빼고 객관적인 표현을 사용하여 최대한 간단 명료하게 써 보아요.\n")
    SituationFeedback = getSituationFeedback(situation)
    while(len(SituationFeedback) > 40):
        print(SituationFeedback)
        situation = input("위의 피드백을 바탕으로 다시 한 번 일어난 일을 써 볼까요?\n")
        SituationFeedback = getSituationFeedback(situation)
    print(SituationFeedback)

    thought = input("위 사건에 대한 나의 생각은 무엇이었나요? 사건을 내가 어떻게 해석하였는지, 오늘의 감정을 느끼게 된 이유를 써 보아요.\n")
    print(getThoughtFeedback(thought))

    emotion = input("오늘의 감정을 조금 더 구체적으로 표현해 보아요. 감정의 정도, 지속시간, 변화 과정 등 감정 자체에 대해서 적어 보아요.\n")
    EmotionFeedback = getEmotionFeedback(emotion)
    while(len(EmotionFeedback) > 75):
        print(EmotionFeedback)
        emotion = input("위 지시에 맞춰 감정을 다시 한 번 적어볼까요?\n")
        EmotionFeedback = getEmotionFeedback(emotion)
    print(EmotionFeedback)

    behavior = input()
    print(getBehaviorFeedback(behavior))

    conclusion = input("오늘 있었던 일에 대해 어떤 결론이 났고, 그에 대해 어떻게 생각하시나요? 결과는 마음에 들 수도, 들지 않을 수도 있습니다. 그런 생각까지 같이 써 보아요.\n")

getCognitiveBehaviorTherapy()
