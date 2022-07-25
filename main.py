import requests
import json
from wxpusher import WxPusher
import os


def queryData(q_sid, q_season):
    return requests.get(f"https://learnywhere.cn/api/bb/20/09/gstudy/inapp/index-data?sid={q_sid}&season={q_season}")


if __name__ == '__main__':
    sid = os.environ["SID"]
    season = os.environ["SEASON"]
    members = json.loads(queryData(sid, season).content)["data_body"]["group"]["members"]
    msg = ""
    for i in members:
        if i["is_me"]:
            calendar = i["check_calendar"]
            for j in calendar:
                if j["is_today"]:
                    if j["learn_duration"] >= 15:
                        msg = f"✅ {i['nickname']} 今日已打卡，学习时间：{j['learn_duration']} 分钟，学习词数：{j['word_count']} 个"
                    else:
                        msg = f"❌ {i['nickname']} 今日未打卡，学习时间：{j['learn_duration']} 分钟，学习词数：{j['word_count']} 个"
    WxPusher.send_message(content=msg,
                          uids=[os.environ["UID"]],
                          token=os.environ["TOKEN"],
                          url=f"https://learnywhere.cn/bb/daka/s23?sid={sid}")
