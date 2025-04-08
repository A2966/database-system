# 食譜整合與查詢資料庫系統

# 應用情境與使用案例
***應用情境**  
1.不知道如何處理剩餘食材   
許多人在家中有多種剩餘食材，卻不確定如何搭配來製作餐點。系統可以根據現有的食材自動推薦合適的食譜，解決食材浪費的問題。   
2.時間有限，不知道做什麼菜   
忙碌的生活讓許多人沒有時間去計劃餐點，尤其是下班後精疲力盡時。系統能快速提供多種餐點選擇，省去思考要做什麼的煩惱，提升效率。   
3.不熟悉食材或廚藝技巧   
有些人可能對某些食材不熟悉，或者不知道該如何烹調。透過系統的食譜推薦與詳細的製作步驟，使用者可以學習如何使用不同的食材來烹飪出美味的餐點。   


***使用案例**  
使用者：忙碌的上班族  
需求：工作繁忙，沒有時間計劃餐點，卻又希望能在家吃得健康    
解決方案：  
根據使用者輸入食材（如高麗菜、不吃豬牛）。  
系統迅速推薦食譜，節省使用者時間。  
  
使用者：烹飪新手  
需求：廚藝經驗不足，不熟悉製作過程與食材使用比例等。    
解決方案：  
根據使用者輸入所需的食材。  
系統迅速推薦食譜，並提供詳細的食譜製作過程。  

# 組員
41143247  葉紘愷  
41143251  蔡沅杰  
41143256  黎丞家  
41143268  許豪中

# 系統需求說明  
前端介面：LINE Bot​
後端開發：Flask / Python  
資料庫系統：MariaDB  

# 完整性限制
![食譜資料表](https://github.com/user-attachments/assets/38f2c7fe-3705-41ea-b03b-f6bb7bbac7a4)
![使用者資料表](https://github.com/user-attachments/assets/a9d35ad9-666f-497f-bd5b-52fbe733484e)
![使用者持有食材](https://github.com/user-attachments/assets/66e01658-aace-4215-9def-256a1341ab38)
![食譜推薦結果](https://github.com/user-attachments/assets/5f6f98be-8d65-4d67-b35b-9d807eafb670)

# ER Diagram
![image](https://github.com/user-attachments/assets/73ce79ed-2156-4b2a-bcff-ba7195cc0f08)
食譜(Recipe) 資料表屬性
食譜ID(Recipe_ID)
食譜名稱(Recipe_Name)
食譜所需食材(Ingredient)
步驟(Instructions)
食譜照片(Recipe_photo_url)

使用者(User) 資料表屬性
使用者ID(User_ID)
LINE ID(LINE_ID)
使用者狀態(User_State)
使用者欲更改食材(Change_id)
使用者上一次輸入食材(User_Last_Ingredients)
使用者上一次推薦食譜(User_Last_recipes)

使用者持有食材(User_Ingredients) 資料表屬性
使用者食材ID(User_Ingredients_ID)
LINE ID(LINE_ID)
持有食材名稱(Database_Ingredients)
數量(Quantity)


食譜推薦結果(Recipe_recommend) 資料表屬性
使用者ID(User_ID)
使用者食材ID(User_Ingredients_ID)
食譜ID(Recipe_ID)

# 詳細說明
•「Recipe」與「Recipe_Recommend」之間有一對多(1..n)的關係。
一個推薦結果可以對應到多個食譜，但一個食譜只能對應到一個推薦結果。
•「User」與「Recipe_Recommend」之間有一對多(1..n)的關係。
一個推薦結果只會對應到一個使用者，但一個使用者可以有很多推薦結果。
•「User_Ingredients」與「Recipe_Recommend」之間有一對多(1..n)的關係。
一個推薦結果會對應到多個使用者食材，而每個使用者食材必須對應到一個推薦結果。
