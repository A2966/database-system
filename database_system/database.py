import mysql.connector
import pymysql
from collections import Counter
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import lsi_process
#登陸資料庫
def login():
    connection = pymysql.connect(
    host='192.168.1.110',
    user='root',
    password='1234',
    database='ingredient_recognition',
    cursorclass=pymysql.cursors.DictCursor  # 使用 DictCursor 以獲取字典格式的查詢結果
    )
    return connection

#刪除相同使用者id的食材
def delete_user_Ingredients(user_id):
    connection = login()
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 刪除語句
            sql = "DELETE FROM user_enter_ingredients WHERE Database_UserID = %s"
            
            # 執行刪除操作，將 user_id 作為參數傳遞進去
            cursor.execute(sql, (user_id,))
            
            # 提交更改
            connection.commit()
            print(f"已刪除 user_id 為 {user_id} 的所有食材資料。")

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 關閉連接
        connection.close()

#刪除指定使用者的指定食材
def delete_user_select_Ingredients(user_id,ingredients_name):
    connection = login()
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 刪除語句
            sql = """
            DELETE FROM user_enter_ingredients 
            WHERE Database_UserID = %s AND Database_Ingredients = %s
            """
            
            # 執行刪除操作，將 user_id 和 ingredients_name 作為參數傳遞進去
            cursor.execute(sql, (user_id, ingredients_name))
            
            # 提交更改
            connection.commit()
            print(f"已刪除 user_id 為 {user_id}，名稱為 '{ingredients_name}' 的食材資料。")

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 關閉連接
        connection.close()

#取得使用者所有食材
def get_user_all_Ingredients(user_id):
    connection = login()
    ingredients = {}
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 刪除語句
            sql = """
                SELECT Database_Ingredients, Database_Ingredients_Number
                FROM user_enter_ingredients 
                WHERE Database_UserID = %s
            """
            
            # 執行查詢並傳入 user_id
            cursor.execute(sql, (user_id,))
            results = cursor.fetchall()  # 獲取所有查詢結果
            
            # 將結果轉換為字典格式
            for id, row in enumerate(results):
                item_name = row['Database_Ingredients']
                quantity = row['Database_Ingredients_Number']
                unit = "個"
                ingredients[id] = {'name': item_name, 'quantity': quantity, 'unit': unit}
            if(ingredients=={}):
                return "錯誤 查無此使用者"
            else:
                return(ingredients)
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 關閉連接
        connection.close()

#檢查使用者是否有該食材    
def check_user_Ingredients(user_id,ingredients_name):
    connection = login()
    ingredients_output = {}
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 查詢語句，查詢該使用者的食材和數量
            sql = """
                SELECT Database_Ingredients, Database_Ingredients_Number
                FROM user_enter_ingredients
                WHERE Database_UserID = %s AND Database_Ingredients = %s
                LIMIT 1
            """
            
            # 執行查詢並傳入 user_id 和 ingredient_name
            cursor.execute(sql, (user_id, ingredients_name))
            result = cursor.fetchone()  # 獲取一條結果
            
            # 如果有結果，則將食材名稱和數量存入 ingredient_info
            if result:
                ingredients_output = {
                    'name': result['Database_Ingredients'],
                    'quantity': result['Database_Ingredients_Number']
                }
                #如果資料庫已存在 輸出該食材與數量
                return ingredients_output
            else:
                #如果資料庫不存在 輸出0
                return 0

    except Exception as e:
        print(f"查詢過程中發生錯誤: {e}")
    
    finally:
        # 關閉資料庫連接
        connection.close()

#修改資料庫(user_id,舊食材名稱,新食材名稱,新數量)
def change_Ingredients(user_id, old_ingredient_name, new_ingredient_name, new_quantity):
    # 連接資料庫
    connection = login()
    
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 更新語句來修改食材名稱和數量
            sql = """
                UPDATE user_enter_ingredients
                SET Database_Ingredients = %s, Database_Ingredients_Number = %s
                WHERE Database_UserID = %s AND Database_Ingredients = %s
            """
            
            # 執行更新操作，傳入新食材名稱、新數量、使用者ID及舊食材名稱
            cursor.execute(sql, (new_ingredient_name, new_quantity, user_id, old_ingredient_name))
            
            # 提交更改
            connection.commit()

            # 檢查是否有行受到影響
            if cursor.rowcount > 0:
                print(f"已成功將使用者 {user_id} 的食材 {old_ingredient_name} 修改為 {new_ingredient_name}，數量為 {new_quantity}。")
            else:
                print(f"使用者 {user_id} 的食材 {old_ingredient_name} 不存在，無法進行更新。")

    except Exception as e:
        print(f"更新過程中發生錯誤: {e}")
    
    finally:
        # 關閉資料庫連接
        connection.close()

#寫入資料庫 (使用者id,食材名稱,食材數量)
def input_Ingredients(user_id, ingredients_name, Database_Ingredients_Number):
    # 連接資料庫
    connection = login()
    oringal_Ingredients ={}
    try:
        #如果資料庫已經有該食材 判斷數量，相加，修改已存在食材的數量
        if(check_user_Ingredients(user_id,ingredients_name)):
            oringal_Ingredients = check_user_Ingredients(user_id,ingredients_name)
            print(oringal_Ingredients)
            Database_Ingredients_Number += oringal_Ingredients['quantity']
            change_Ingredients(user_id,ingredients_name,ingredients_name,Database_Ingredients_Number)
        #如果資料庫沒有該食材 直接寫入
        else:
            with connection.cursor() as cursor:
                    # 編寫 SQL 查詢語句
                sql = """
                INSERT INTO user_enter_ingredients 
                (Database_UserID, Database_Ingredients, Database_Ingredients_Number) 
                VALUES (%s, %s, %s)
                """
                # 將參數值傳入 SQL 語句 分別為:使用者id,食材名稱,食材數量
                cursor.execute(sql, (user_id, ingredients_name, Database_Ingredients_Number))

                # 提交更改
                connection.commit()
                print("寫入資料庫成功")

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 關閉連接
        connection.close()

#改變使用者階段(更改食材)
def change_user_state(user_id,new_state):
    connection = login()
    
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 更新語句來修改食材名稱和數量
            sql = """
                UPDATE user_state
                SET Database_User_State	 = %s
                WHERE Database_UserID = %s
            """
            
            # 執行更新操作，傳入新食材名稱、新數量、使用者ID及舊食材名稱
            cursor.execute(sql, (new_state,user_id))
            
            # 提交更改
            connection.commit()

            # 檢查是否有行受到影響
            if cursor.rowcount > 0:
                print(f"已成功將使用者 {user_id} 的狀態修改為 {new_state}")
            else:
                print(f"使用者 {user_id} 的狀態不存在，無法進行更新。")

    except Exception as e:
        print(f"更新過程中發生錯誤: {e}")
    
    finally:
        # 關閉資料庫連接
        connection.close()

#獲取使用者階段(更改食材)
def get_user_state(user_id):
    connection = login()
    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT Database_User_State
                FROM user_state 
                WHERE Database_UserID = %s
            """
            
            # 執行查詢並傳入 user_id
            cursor.execute(sql, (user_id,))
            results = cursor.fetchone()  # 獲取所有查詢結果
            
            #判斷使用者狀態使否已存在資料庫
            #如果不存在 寫入None
            if not results:
                sql = """
                INSERT INTO user_state 
                (Database_UserID, Database_User_State) 
                VALUES (%s, "None")
                """
                
                cursor.execute(sql, (user_id,))
                connection.commit()
                get_user_state(user_id)
            
            #如果存在 回傳使用者狀態
            else:
                return results['Database_User_State']

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 關閉連接
        connection.close()

#輸入使用者要更改的編號(更改食材)
def input_change_id(user_id,change_id):
    connection = login()
    try:
        with connection.cursor() as cursor:
            sql = """
                UPDATE user_state
                SET Database_change_id = %s
                WHERE Database_UserID = %s
                """
            
            # 執行查詢並傳入 user_id
            cursor.execute(sql, (change_id,user_id))
            print(f"{user_id}修改編號為{change_id}")
            connection.commit()


    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 關閉連接
        connection.close()

#獲取使用者要更改的編號(更改食材)
def get_change_id(user_id):
    
    connection = login()
    try:
        with connection.cursor() as cursor:
            sql = """
                SELECT Database_change_id
                FROM user_state 
                WHERE Database_UserID = %s
            """
            
            cursor.execute(sql, (user_id,))
            connection.commit()

            results = cursor.fetchone()  # 獲取所有查詢結果

            return results['Database_change_id']

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 關閉連接
        connection.close()

#獲取使用者上次查詢的食材(推薦食譜)
def get_user_Last_Ingredients(user_id):
    connection = login()
    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT Database_User_Last_Ingredients
                FROM user_state 
                WHERE Database_UserID = %s
            """
            
            # 執行查詢並傳入 user_id
            cursor.execute(sql, (user_id,))
            results = cursor.fetchone()  # 獲取所有查詢結果
            
            #判斷使用者狀態使否已存在資料庫
            #如果不存在 寫入None
            if not results:
                sql = """
                INSERT INTO Database_User_Last_Ingredients 
                (Database_UserID, Database_User_Last_Ingredients) 
                VALUES (%s, "None")
                """
                
                cursor.execute(sql, (user_id,))
                connection.commit()
                get_user_state(user_id)
            
            #如果存在 回傳使用者狀態
            else:
                return results['Database_User_Last_Ingredients']

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 關閉連接
        connection.close()

#改變使用者上次查詢的食材(推薦食譜)
def change_user_Last_Ingredients(user_id,Last_Ingredients):
    connection = login()
    
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 更新語句來修改食材名稱和數量
            sql = """
                UPDATE user_state
                SET Database_User_Last_Ingredients= %s
                WHERE Database_UserID = %s
            """
            
            # 執行更新操作，傳入新食材名稱、新數量、使用者ID及舊食材名稱
            cursor.execute(sql, (Last_Ingredients,user_id))
            
            # 提交更改
            connection.commit()

            # 檢查是否有行受到影響
            if cursor.rowcount > 0:
                print(f"已成功將使用者 {user_id} 上次的食材修改為 {Last_Ingredients}")
                #如果成功更新回傳1 進行食材更新 要重新推薦食譜
                return 1
            else:
                print(f"使用者 {user_id} 的上次食材不用進行更新。")
                #如果失敗回傳0 不進行食材更新
                return 0

    except Exception as e:
        print(f"更新過程中發生錯誤: {e}")
    
    finally:
        # 關閉資料庫連接
        connection.close()

#改變使用者上次推薦出來的食譜(推薦食譜)
def save_user_Last_Recipes(user_id,Last_Recipes):
    connection = login()
    
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 更新語句來修改食材名稱和數量
            sql = """
                UPDATE user_state
                SET Database_User_Last_recipes= %s
                WHERE Database_UserID = %s
            """
            
            # 執行更新操作，傳入新食材名稱、新數量、使用者ID及舊食材名稱
            cursor.execute(sql, (Last_Recipes,user_id))
            
            # 提交更改
            connection.commit()

            # 檢查是否有行受到影響
            if cursor.rowcount > 0:
                print(f"已成功將使用者 {user_id} 上次的食譜修改為 {Last_Recipes}")
                #如果成功更新回傳1 進行食材更新 要重新推薦食譜
                return 1
            else:
                print(f"使用者 {user_id} 的上次食材不用進行更新。")
                #如果失敗回傳0 不進行食材更新
                return 0

    except Exception as e:
        print(f"更新過程中發生錯誤: {e}")
    
    finally:
        # 關閉資料庫連接
        connection.close()

#獲取使用者上次查詢出來的食譜(推薦食譜)
def get_user_Last_recipes(user_id):
    connection = login()
    try:
        with connection.cursor() as cursor:

            sql = """
                SELECT Database_User_Last_recipes
                FROM user_state 
                WHERE Database_UserID = %s
            """
            
            # 執行查詢並傳入 user_id
            cursor.execute(sql, (user_id,))
            results = cursor.fetchone()  # 獲取所有查詢結果
            
            recipes = results['Database_User_Last_recipes'].split(',')
            return recipes

    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        # 關閉連接
        connection.close()

def get_recipe_by_name(recipe_Name):
    connection = login()
    recipe={'recipe_Name':'',
            'recipe_ingredients':'',
            'instructions':'',
            'recipe_url':'',
            'recipe_photo_url':''
            }
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 查詢語句
            sql = """
                SELECT recipe_Name, recipe_ingredients, instructions, recipe_url, recipe_photo_url
                FROM recipe
                WHERE recipe_Name = %s
            """
            
            # 執行查詢並傳入 recipe_Name
            cursor.execute(sql, (recipe_Name,))
            result = cursor.fetchone()  # 獲取查詢結果

            # 如果查詢有結果，則將結果存入 recipe 字典
            if result:
                recipe['recipe_Name'] = result['recipe_Name']
                recipe['recipe_ingredients'] = result['recipe_ingredients']
                recipe['instructions'] = result['instructions']
                recipe['recipe_url'] = result['recipe_url']
                recipe['recipe_photo_url'] = result['recipe_photo_url']
            else:
                print("找不到該食譜。")
                recipe['recipe_Name'] = "查詢過程中發生錯誤"
                recipe['recipe_ingredients'] = "查詢過程中發生錯誤"
                recipe['instructions'] = "查詢過程中發生錯誤"
                recipe['recipe_url'] = "查詢過程中發生錯誤"
                recipe['recipe_photo_url'] = "https://img.zdic.net/kai/cn/7121.svg"

    except Exception as e:
        print(f"查詢過程中發生錯誤: {e}")
    
    finally:
        # 關閉連接
        connection.close()

    return recipe

def get_recipe_by_ingredients(recipe_ingredients):
    # 定義一個清單來存放查詢結果
    recipe_names = []

    # 連接資料庫
    connection = login()
    try:
        with connection.cursor() as cursor:
            # 編寫 SQL 查詢語句，使用 LIKE 進行模糊匹配
            sql = """
                SELECT recipe_Name
                FROM recipe
                WHERE recipe_ingredients LIKE %s
            """
            
            # 加入通配符 % 以進行模糊匹配
            cursor.execute(sql, ('%' + recipe_ingredients + '%',))
            results = cursor.fetchall()  # 獲取所有匹配的結果

            # 如果有結果，將每個 recipe_Name 存入 recipe_names 清單
            for result in results:
                recipe_names.append(result['recipe_Name'])

            # 如果沒有找到匹配結果
            if not recipe_names:
                print(f"找不到包含 '{recipe_ingredients}' 的食譜。")

    except Exception as e:
        print(f"查詢過程中發生錯誤: {e}")
    
    finally:
        # 關閉連接
        connection.close()

    return recipe_names

'''舊版 現在採用lsi
def find_top_recipes(ingredients_list, top_n=10):
    #ingredients_list為陣列 例:["地瓜粉", "薄荷葉", "九層塔"]
    # top_n為前n個最常出現的 
    # 使用 Counter 來計算食譜名稱出現的次數
    recipe_counter = Counter()

    for ingredient in ingredients_list:
        # 使用剛剛的函式查詢包含該食材的食譜名稱
        recipes = get_recipe_by_ingredients(ingredient)
        recipe_counter.update(recipes)  # 更新計數器

    # 找到出現次數最多的前 N 個食譜
    most_common_recipes = recipe_counter.most_common()
    
    # 分組按出現次數
    grouped_recipes = {}
    for recipe, count in most_common_recipes:
        if count not in grouped_recipes:
            grouped_recipes[count] = []
        grouped_recipes[count].append(recipe)

    # 將每組按亂序排列
    for count in grouped_recipes:
        random.shuffle(grouped_recipes[count])

    # 按次數降序排列，取出前 N 個
    top_recipes = []
    for count in sorted(grouped_recipes.keys(), reverse=True):
        for recipe in grouped_recipes[count]:
            if len(top_recipes) < top_n:
                top_recipes.append((recipe, count))
            else:
                break

    return top_recipes

def get_recipe_count():
    connection = login()
    try:
        with connection.cursor() as cursor:
            # SQL 查詢語句，用於計算食譜總數
            sql = "SELECT COUNT(*) AS recipe_count FROM recipe"
            cursor.execute(sql)
            result = cursor.fetchone()  # 獲取結果

            if result:
                recipe_count = result['recipe_count']
                print(f"資料庫中共有 {recipe_count} 筆食譜。")
                return recipe_count
            else:
                print("無法取得食譜數量。")
                return 0

    except Exception as e:
        print(f"發生錯誤: {e}")
        return 0
    finally:
        # 關閉連接
        connection.close()

def find_top_recipes2(userid):
    top_n=10 #找出最接近的數量
    threshold = 0.1#如果低於這個數字 就不輸出

    #先將使用者食材儲存在item
    item = {}
    item = get_user_all_Ingredients(userid)
    #把使用者食材組成單一條字串
    user_ingredients = ""
    names = [item['name'] for item in item.values()]
    user_ingredients = ' '.join(names)

    """
    將使用者的食材與資料庫中的食譜進行比較，找出最相似的前 N 個食譜。
    """
    connection = login()
    try:
        with connection.cursor() as cursor:
            # 從資料庫查詢所有食譜的名稱與食材
            sql = "SELECT recipe_Name, recipe_ingredients FROM recipe"
            cursor.execute(sql)
            recipes = cursor.fetchall()

            if not recipes:
                print("資料庫中沒有食譜。")
                return []

            # 準備資料進行相似度計算
            recipe_names = []
            recipe_ingredients_list = []

            for recipe in recipes:
                recipe_names.append(recipe['recipe_Name'])
                recipe_ingredients_list.append(recipe['recipe_ingredients'])

            # 使用者的食材加到比較列表中
            all_texts = [user_ingredients] + recipe_ingredients_list

            # 計算 TF-IDF 向量
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(all_texts)

            # 計算使用者食材與每個食譜的相似度
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

            # 將相似度與食譜名稱配對並過濾低於閾值的結果
            recipe_similarities = [
                (name, similarity)
                for name, similarity in zip(recipe_names, cosine_sim)
                if similarity >= threshold
            ]

            # 按相似度降序排序
            recipe_similarities.sort(key=lambda x: x[1], reverse=True)

            # 取出前 N 個相似度最高的食譜
            top_recipes = recipe_similarities[:top_n]

            return top_recipes

    except Exception as e:
        print(f"發生錯誤: {e}")
        return []
    finally:
        connection.close()
'''

def update_recipe_photo_url():
    connection = login()  # 確保你有一個 login() 函式來連接資料庫
    try:
        with connection.cursor() as cursor:
            # 更新所有 photo_url 為 "無照片" 的食譜
            sql = """
                UPDATE recipe
                SET recipe_photo_url = 'https://img.zdic.net/kai/cn/7121.svg'
                WHERE recipe_photo_url = '無照片'
            """
            affected_rows = cursor.execute(sql)
            connection.commit()
            print(f"成功更新 {affected_rows} 筆資料！")
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        connection.close()

'''測試'''
if __name__ == "__main__":
    # user_indgredients = " ".join([item['name'] for item in get_user_all_Ingredients("U99bf7d93399b51d98f97f0cfc861ebb2").values()])
    # top10_recipes = lsi_process.lsi_find_top_10_recipe("U99bf7d93399b51d98f97f0cfc861ebb2")
    # push_10_recipe = {}
    # save_recipes = ""
    # if all(recipe == "空" for recipe in top10_recipes):
    #     print("找不到符合的食譜。")
    # else:
    #     for i in range(10):
    #         if top10_recipes[i] != "空":
    #             save_recipes += top10_recipes[i] + ","
    #             recipe = get_recipe_by_name(top10_recipes[i])
    #             push_10_recipe[i] = {
    #                 'title': recipe['recipe_Name'],
    #                 'recipe_photo_url': recipe['recipe_photo_url']
    #             }
    #     save_user_Last_Recipes("U99bf7d93399b51d98f97f0cfc861ebb2",save_recipes)

    # print(top10_recipes)
    update_recipe_photo_url()
    print(login())