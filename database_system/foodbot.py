from flask import Flask, request
import json
import requests
import os
import cv2
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, ImageSendMessage, LocationSendMessage,MessageAction, TemplateSendMessage, CarouselTemplate,PostbackAction,URIAction, MessageAction, TemplateSendMessage, ButtonsTemplate
from linebot import LineBotSdkDeprecatedIn30
import warnings

import database_LSI
import TextProcess
import database 
import lsi_process

app = Flask(__name__)

access_token = 'JHhiDt9zCtuXL5Y6uupdvMnq6rvWLennlqkUcyHPNWyxo3N+kenxsiRMZmoGKtx099Paf9nZuDyehiL3Y4/JPZOlgdsRrAToRkBotWlGUc66Ltqt6/7FM4uZtgmw8fC9DBQBeynxTRz0gnk9wE12sQdB04t89/1O/w1cDnyilFU='
channel_secret = '64006d2bd468b3457ceb511b815bd46b'

warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)

documents = database_LSI.load_recipe_ingredients_from_file()
name_documents = database_LSI.load_recipe_Name_from_file()


def restart(user_id):
    
    line_bot_api = LineBotApi(access_token)
    database.delete_user_Ingredients(user_id)
    database.change_user_Last_Ingredients(user_id,"")
    database.save_user_Last_Recipes(user_id,"")
    
    #清除食材 並將使用者狀態設為None
    text_message = TextSendMessage(text="已清除食材內容")
    line_bot_api.push_message(user_id,text_message)
    database.change_user_state(user_id,"None")


@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)    
    try:
        json_data = json.loads(body)
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(channel_secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        reply_token = json_data['events'][0]['replyToken']
        type = json_data['events'][0]['message']['type']

        #獲得使用者id
        user_id = json_data['events'][0]['source']['userId']

        print("\n>使用者id:", user_id)
        print(">目前使用者階段:",database.get_user_state(user_id))
        #獲得使用者目前所在的rich_menu
        rich_menu_id = line_bot_api.get_rich_menu_id_of_user(user_id)
        if(rich_menu_id=="richmenu-d0c06ab90a4ac22079019e3120c9db14"):
            print(">使用者目前位於主選單")
        if(rich_menu_id=="richmenu-0144c049c1d6cb5ce2c44137fb12e3a6"):
            print(">使用者目前位於AI對話選單")
        #如果是輸入文字就印出來
        if(type == 'text'):
            msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
            print("輸入文字:",msg)#在終端顯示輸入的文字

            
        #使用者輸入圖片
        
        if (type == 'text'and (database.get_user_state(user_id) == "None")):
            #print("輸入文字:",msg)#在終端顯示輸入的文字

            #目前工作階段:
            print("目前工作階段:",TextProcess.check_input(msg))

             #如果使用者不是輸入指令就當輸入食材
            if(TextProcess.check_input(msg)=="輸入食材"):

                changed_input = TextProcess.change_input_word(msg)#轉換別稱
                Ingredients_input_result =TextProcess.Ingrnediets_input(changed_input)
                
                #判斷輸入格式是否正確

                #輸入格式錯誤 發送錯誤訊息
                if(Ingredients_input_result=="輸入錯誤"):
                    text_message = TextSendMessage(text="輸入錯誤 請重新輸入")
                    line_bot_api.reply_message(reply_token,text_message)
                #輸入格式正確
                else:
                    print("抓取食材:",Ingredients_input_result[0]['name'],Ingredients_input_result[0]['quantity'])
                    
                    if(Ingredients_input_result[0]['quantity']>0):
                        #寫入食材到資料庫
                        database.input_Ingredients(user_id,Ingredients_input_result[0]['name'],Ingredients_input_result[0]['quantity'])
                        #例: 輸入"番茄11顆" Ingredients_input_result為{0: {'name': '番茄', 'quantity': 4, 'unit': '顆'}}

                        #輸出目前食材給使用者
                        text_message = TextSendMessage(text=TextProcess.Ingrnediets_output(database.get_user_all_Ingredients(user_id)))
                        line_bot_api.reply_message(reply_token,text_message)
                    else:
                        text_message = TextSendMessage(text="輸入錯誤 請輸入大於0的數量")
                        line_bot_api.reply_message(reply_token,text_message)
                

            #如果收到重新開始就清除該使用者的食材資料
            if(TextProcess.check_input(msg)=="重新開始"):
                restart(user_id)
            #如果收到使用說明,就發送使用說明
            if(TextProcess.check_input(msg)=="使用說明"):
                text_message = TextSendMessage(text="""本機器人可以根據您目前擁有的食材推薦合適的食譜，協助您輕鬆料理每一餐！

📸 傳送食材照片
您可以隨時傳送食材的照片，系統會自動辨識並加入您的「持有食材清單」。
🔺 註：拍照時請盡量避免食材重疊，以免影響辨識效果。

✍️ 手動輸入食材
也可以直接輸入食材與數量，例如：
胡蘿蔔 3個

📝 更改食材
點選「更改食材」功能，可編輯、刪除您目前的持有食材。

🔁 重新開始
點選「重新開始」，系統會清空您目前的食材清單，重新開始紀錄。

📤 結束傳送
點選「結束傳送」，系統將根據您目前的食材清單推薦最適合的食譜。

💬 你問我答（AI 問答模式）
點選「你問我答」，可詢問任何與健康、營養或食譜相關的問題。若您提問的是食譜建議，AI 將自動根據您的食材推薦合適的菜單。

""")
                line_bot_api.reply_message(reply_token,text_message)
            #如果收到更改食材就開始更改食材
            if(TextProcess.check_input(msg)=="更改食材"):
                if(TextProcess.check_input(msg)=="重新開始"):
                    restart(user_id)
                else:
                    #將使用者狀態修改成change1 -修改編號
                    text_message = TextSendMessage(text=TextProcess.Ingrnediets_output(database.get_user_all_Ingredients(user_id)))
                    line_bot_api.reply_message(reply_token,text_message)
                    text_message = TextSendMessage(text="請輸入食材編號進行更改")
                    line_bot_api.push_message(user_id,text_message)
                    database.change_user_state(user_id,"change1")
            
            #如果收到結束傳送 先蒐集完食譜 接著輸出食譜選單
            if(TextProcess.check_input(msg)=="結束傳送"):
                #如果使用者沒輸入食材 提醒使用者
                if(database.get_user_all_Ingredients(user_id)=="錯誤 查無此使用者"):
                    text_message = TextSendMessage(text="請先輸入食材")
                    line_bot_api.push_message(user_id,text_message)
                try:
                    #合併使用者食材
                    user_indgredients = " ".join([item['name'] for item in database.get_user_all_Ingredients(user_id).values()])
                    push_10_recipe = {}
                    if(database.change_user_Last_Ingredients(user_id,user_indgredients)):
                    #使用者食材有更改 使用LSI演算法找出最相似的食譜
                        text_message = TextSendMessage(text="請稍後,我們正在為您搜尋食譜...")
                        line_bot_api.push_message(user_id,text_message)
                        #食譜儲存初始化
                        save_recipes = ""
                        #用LSI找最接近的食譜
                        top10_recipes = lsi_process.lsi_find_top_10_recipe(user_id,documents,name_documents)
                        #如果完全找不到適合的食譜 回傳找不到
                        if all(recipe == "空" for recipe in top10_recipes):
                            text_message = TextSendMessage(text="很抱歉,我們無法找到對應的食譜")
                            line_bot_api.push_message(user_id,text_message)
                            #如果這次沒找到食譜,把食材儲存成別的 避免下次直接搜尋食譜時進入死循環
                            database.change_user_Last_Ingredients(user_id,"上次沒找到食譜")
                        else:
                            #把食譜處理 符合LINE橫幅格式
                            for i in range(10):
                                if top10_recipes[i] != "空":
                                    #儲存食譜名稱
                                    save_recipes += top10_recipes[i] + ","
                                    #查詢食譜名稱對應食譜
                                    recipe = database.get_recipe_by_name(top10_recipes[i])
                                    push_10_recipe[i] = {
                                        'title': recipe['recipe_Name'],
                                        'recipe_photo_url': recipe['recipe_photo_url']
                                    }
                                #如果沒有食譜就顯示無
                                else:
                                    push_10_recipe[i] = {
                                        'title': "無",
                                        'recipe_photo_url': "https://img.zdic.net/kai/cn/7121.svg"}
                            #儲存使用者食譜
                            database.save_user_Last_Recipes(user_id,save_recipes)

                    else:
                    #使用者食材不用更改 沿用上次的結果
                        #取得上次的食譜
                        top10_recipes = database.get_user_Last_recipes(user_id)
                        for i in range(10):
                            if top10_recipes[i] != "空":
                                #查詢食譜名稱對應食譜
                                recipe = database.get_recipe_by_name(top10_recipes[i])
                                push_10_recipe[i] = {
                                    'title': recipe['recipe_Name'],
                                    'recipe_photo_url': recipe['recipe_photo_url']
                                }
                            #如果沒有食譜就顯示無
                            else:
                                    push_10_recipe[i] = {
                                        'title': "無",
                                        'recipe_photo_url': "https://img.zdic.net/kai/cn/7121.svg"}
                                                                                #同時輸入10個食譜集合而成的字典
                    line_bot_api.reply_message(reply_token,TextProcess.recipe_carousel(push_10_recipe))
                except Exception as e:
                    print("錯誤:",e)
        
        #使用者在更改食材第一階段:選擇編號
        elif (database.get_user_state(user_id) == "change1"):
            if(TextProcess.check_input(msg)=="重新開始"):
                restart(user_id)
            else:
                Ingredients = {}#儲存食材表
                Ingredients = database.get_user_all_Ingredients(user_id)
                
                if(msg.isdigit()):#判斷書入是否數字
                    msg_int = int(msg)
                    msg_int -= 1
                    if(int(msg_int) in Ingredients):#判斷編號是否存在資料庫
                        

                        #輸入修改編號
                        database.input_change_id(user_id,msg_int)
                        #切換階段到change3
                        database.change_user_state(user_id,"change2")
                        text_message = TextSendMessage(text="修改內容或數量?\n輸入0刪除該食材")
                        line_bot_api.reply_message(reply_token,text_message)            
                    else:
                        text_message = TextSendMessage(text="該編號不存在於食材列表 請重新輸入")
                        line_bot_api.reply_message(reply_token,text_message) 
                else:
                    text_message = TextSendMessage(text="輸入錯誤 請輸入編號")
                    line_bot_api.reply_message(reply_token,text_message)
            
        #使用者在更改食材第二階段:修改內容及數量 
        elif (database.get_user_state(user_id) == "change2"):
            if TextProcess.check_input(msg) == "重新開始":
                restart(user_id)
            elif msg == "0":
                # **刪除對應食材**
                change_id = database.get_change_id(user_id)  # 獲取使用者最近更改的食材 ID
                old_Ingredients = database.get_user_all_Ingredients(user_id)  # 取得所有食材
                
                if change_id in old_Ingredients:
                    ingredient_name = old_Ingredients[change_id]["name"]
                    database.delete_user_select_Ingredients(user_id, ingredient_name)
                    text_message = TextSendMessage(text=TextProcess.Ingrnediets_output(database.get_user_all_Ingredients(user_id)))
                else:
                    text_message = TextSendMessage(text="找不到可刪除的食材，請重新輸入")

                line_bot_api.reply_message(reply_token, text_message)
                database.change_user_state(user_id, "None")  # **恢復狀態**
            
            else:
                changed_input = TextProcess.change_input_word(msg)  # **轉換別稱**
                Ingredients_input_result = TextProcess.Ingrnediets_input(changed_input)
                
                # **輸入格式錯誤**
                if Ingredients_input_result == "輸入錯誤":
                    text_message = TextSendMessage(text="輸入錯誤，請重新輸入")
                    line_bot_api.reply_message(reply_token, text_message)
                
                # **輸入格式正確**
                else:
                    print("抓取食材:", Ingredients_input_result[0]["name"], Ingredients_input_result[0]["quantity"])  # Debug
                    
                    old_Ingredients = database.get_user_all_Ingredients(user_id)
                    change_id = database.get_change_id(user_id)

                    # **如果資料庫內已經有該食材，則先刪除**
                    if database.check_user_Ingredients(user_id, Ingredients_input_result[0]["name"]):
                        database.delete_user_select_Ingredients(user_id, Ingredients_input_result[0]["name"])
                        
                        if Ingredients_input_result[0]["quantity"] != 0:
                            # **寫入新數據**
                            database.input_Ingredients(user_id, Ingredients_input_result[0]["name"], Ingredients_input_result[0]["quantity"])
                    
                    # **如果資料庫內沒有該食材，則嘗試替換**
                    else:
                        if Ingredients_input_result[0]["quantity"] == 0:
                            text_message = TextSendMessage(text="輸入錯誤，請重新輸入")
                            line_bot_api.reply_message(reply_token, text_message)
                        else:
                            database.change_Ingredients(
                                user_id, 
                                old_Ingredients[change_id]["name"], 
                                Ingredients_input_result[0]["name"], 
                                Ingredients_input_result[0]["quantity"]
                            )
                    
                    # **回傳更新後的食材**
                    text_message = TextSendMessage(text=TextProcess.Ingrnediets_output(database.get_user_all_Ingredients(user_id)))
                    line_bot_api.reply_message(reply_token, text_message)
                    database.change_user_state(user_id, "None")    
                
        #使用者點了食譜選單的內容
    except:
        try:
            post_type = json_data['events'][0]['type']
            if(post_type=='postback'):
                user_id = json_data['events'][0]['source']['userId']
                post_data = json_data['events'][0]['postback']['data']
                print("postdata:", post_data)
                #進入AI對話階段
                if(post_data=="richmenu=QA"):
                    database.change_user_state(user_id,"QA")
                #退出AI對話階段
                if(post_data=="richmenu=menu&message=已返回主選單"):
                    #將使用者選單切回主選單
                    line_bot_api.link_rich_menu_to_user(user_id, "richmenu-d0c06ab90a4ac22079019e3120c9db14")
                    database.change_user_state(user_id,"None")

                if post_data not in ("richmenu=QA", "richmenu=menu&message=已返回主選單"):
                    print("選取食譜:",post_data)
                    recipe={
                        'recipe_Name':'',
                        'recipe_ingredients':'',
                        'instructions':'',
                        'recipe_url':'',
                        'recipe_photo_url':''
                        }
                    recipe = database.get_recipe_by_name(post_data)
                    print(recipe)
                    push_recipe_name="目前選取食譜: " + recipe['recipe_Name']
                    line_bot_api.push_message(user_id,TextSendMessage(push_recipe_name))
                    line_bot_api.push_message(user_id,TextSendMessage(recipe['recipe_ingredients']))
                    line_bot_api.reply_message(reply_token,TextSendMessage(recipe['instructions']))
                
            
        except Exception as e:
            print(e)     
    return 'OK'

if __name__ == "__main__":
    app.run()