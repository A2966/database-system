# 食譜查詢資料庫系統
[完整報告](https://docs.google.com/document/d/1XnYxtbKad_cpNTJ_7QKpYyJQcEL0qx2E/edit?usp=sharing&ouid=115670203116726374810&rtpof=true&sd=true)
[完整簡報](https://docs.google.com/presentation/d/1M0LcFYir5Ignc69XoNfuhVLNlO72zojE/edit?usp=sharing&ouid=115670203116726374810&rtpof=true&sd=true)

使用者輸入他所持有的食材，系統會依照使用者所提供的食材，進行最佳的食譜推薦。

## 📋 目錄
- [組員資訊](#組員資訊)
- [應用情境與使用案例](#應用情境與使用案例)
- [系統架構](#系統架構)
- [資料庫結構與完整性限制](#資料庫結構與完整性限制)
- [ER Diagram](#ER_Diagram)
- [詳細說明](#詳細說明)
- [使用者權限](#使用者權限)
- [View](#View)

## 組員資訊

| 學號 | 姓名 | 分工 |
|------|------|------|
| 41143247 | 葉紘愷 | 資料庫架構設計、資料庫實際建置、完整性限制、資料表結構、期末報告PPT製作 |
| 41143251 | 蔡沅杰 | 資料爬蟲、 協助ER digram製作、使用案例圖設計、協助View製作、期末報告PPT製作|
| 41143256 | 黎丞家 | LINE bot、食譜查詢 |
| 41143268 | 許豪中 | 管理食譜網站 |

## 應用情境與使用案例

### 🎯 應用情境

#### 1. 利用剩餘食材組合出其他食譜
許多人在家中有多種剩餘食材，卻不確定如何搭配來製作餐點。系統可以根據食材自動推薦合適的食譜，並告訴你需要哪些食材來補齊，讓你善用剩餘食材，解決食材浪費的同時探索全新的食材料理方式。

#### 2. 時間有限，不知道做什麼菜
忙碌的生活讓許多人沒有時間去計劃餐點，尤其是下班後精疲力盡時。系統能快速提供多種餐點選擇，省去思考要做什麼的煩惱，提升效率。

#### 3. 不熟悉食材或廚藝技巧
有些人可能對某些食材不熟悉，或者不知道該如何烹調。透過系統的食譜推薦與詳細的製作步驟，使用者可以學習如何使用不同的食材來烹飪出美味的餐點。

###  使用案例

![使用案例圖](https://github.com/user-attachments/assets/fadfac63-4f0d-4336-acd9-d179ea0bdf11)

![使用案例圖](https://github.com/user-attachments/assets/00b1ba91-4c1b-4a1f-a8e3-e95101446aa7)

![使用案例圖](https://github.com/user-attachments/assets/93fe2b90-f2a1-4f9c-9f5f-845aa593d8dd)

- 使用者
  - 輸入食材
  - 更改食材
  - 推薦食譜
  - 設定厭惡食材
- 說明
  - 使用者可以輸入想要的食材，對應「User_Ingredients(使用者持有食材表)」。
  - 使用者輸入錯誤時可以更改所需的食材。
  - 當使用者確認所需全部食材時，推薦出最相關食譜。
  - 使用者可以自行設定討厭的食材，避免出現在食譜上面。對應「User(使用者表)」。

- 管理者
  - 新增食譜
  - 修改食譜
    
- 說明
  - 管理者可以新增新的食譜。
  - 管理者可以修改現有的食譜。

## 系統需求說明

### 新增食材
- 允許使用者輸入食材  
- 記錄使用者當前輸入的食材  

### 更改食材
- 支援使用者選擇並更改食材編號  

### 使用者偏好
- 允許使用者輸入不喜歡的食材  
- 根據使用者偏好調整推薦結果  

### 推薦食譜
- 根據使用者目前擁有的食材，推薦相符的食譜  

## 系統架構

### 技術堆疊
- 前端介面：LINE Bot
- 後端開發：Flask / Python
- 資料庫系統：phpMyAdmin

# 資料庫結構與完整性限制

## 完整性限制

### 📋 Recipe 資料表

#### 基本欄位

| 欄位名稱 | 資料型態 | 是否可為空 | 欄位說明 | 值域/限制 | 實際資料舉例 |
|---------|----------|------------|----------|------------|-------------|
| Recipe_ID | INT | 否 | 食譜編號（主鍵） | 自動編號，唯一 | 101 |
| Recipe_Name | VARCHAR(100) | 否 | 食譜名稱 | 長度1~100的文字 | 羅宋湯 |
| Ingredient | TEXT | 否 | 使用食材列表 | 以文字描述所需食材，以,分隔 | 番茄,馬鈴薯 |
| Instructions | TEXT | 是 | 食譜步驟說明 | 長度至少為 1的文字說明 | 半顆的洋蔥切丁、紅蘿蔔、馬玲薯切丁... |
| Recipe_url | TEXT | 是 | 詳細食譜連結 | 合法 URL | https://example.com/recipe |
| Recipe_photo_url | TEXT | 是 | 食譜圖片網址 | 合法圖片 URL | https://imgur.com/pasta.jpg |

#### 完整性限制說明

| 欄位名稱 | 值域限制說明 | 確認方式（MySQL） |
|---------|-------------|-----------------|
| Recipe_ID | 必須為大於 0 的整數，且不可為空，作為主鍵需保證唯一性 | 使用 AUTO_INCREMENT 確保遞增且唯一 |
| Recipe_Name | 必須為 1 到 100 個字元長度的文字，可包含中英文、數字、空格及常見標點符號，且不可為空，用以顯示食譜的完整名稱。 | CHECK (CHAR_LENGTH(Recipe_Name) BETWEEN 1 AND 100) |
| Ingredient | 必須包含至少一項食材，不可為空 | CHECK (CHAR_LENGTH(Ingredient) > 0) |
| Instructions | 至少為 1 字元長度的文字，可包含中英文、數字、空格及常見標點符號，且不可為空，用以顯示食譜的完整製作過程。 | CHECK (CHAR_LENGTH(Instructions) > 0 )|
| Recipe_url | 可為空，若不為空則必須是合法的 URL 格式 | CHECK (Recipe_url IS NULL OR Recipe_url REGEXP '^https?://[A-Za-z0-9\\-\\._~:/\\?#\\[\\]@!\\$&\'\\(\\)\\*\\+,;=]+$') |
| Recipe_photo_url | 可為空，若不為空則必須是合法的圖片 URL 格式 | CHECK (Recipe_photo_url IS NULL OR Recipe_photo_url REGEXP '^https?://.*\\.(jpg\|jpeg\|png\|gif)$') |

```sql
CREATE TABLE Recipe (
    Recipe_ID INT PRIMARY KEY AUTO_INCREMENT,
    Recipe_Name VARCHAR(100) NOT NULL,
    Ingredient TEXT NOT NULL,
    Instructions TEXT NOT NULL,
    Recipe_url TEXT,
    Recipe_photo_url TEXT,
    CHECK (CHAR_LENGTH(Recipe_Name) BETWEEN 1 AND 100),
    CHECK (CHAR_LENGTH(Ingredient) > 0),
    CHECK (Recipe_url IS NULL OR Recipe_url REGEXP '^https?://[A-Za-z0-9\\-\\._~:/\\?#\\[\\]@!\\$&\'\\(\\)\\*\\+,;=]+$'),
    CHECK (Recipe_photo_url IS NULL OR Recipe_photo_url REGEXP '^https?://.*\\.(jpg|jpeg|png|gif)$')
) ENGINE=InnoDB;


-- 範例：插入一筆食譜資料到 Recipe 表
INSERT INTO Recipe (Recipe_Name, Ingredient, Instructions, Recipe_url, Recipe_photo_url)
VALUES (
    '炒蛋',                                      -- Recipe_Name：食譜名稱
    '雞蛋, 鹽, 油',                                  -- Ingredient：食材列表
    '將雞蛋打散，加鹽後下油鍋翻炒至熟。',              -- Instructions：料理步驟說明
    'https://example.com/recipe/eggs',               -- Recipe_url：食譜詳細說明網頁連結（可選）
    'https://example.com/images/eggs.jpg'            -- Recipe_photo_url：食譜圖片連結（可選，限圖片格式）
);
```

### 👤 User 資料表

#### 基本欄位

| 欄位名稱 | 資料型態 | 是否可為空 | 欄位說明 | 值域/限制 | 實際資料舉例 |
|---------|----------|------------|----------|------------|-------------|
| LINE_ID | VARCHAR(50) | 否 | 使用者的 LINE 識別碼 | 唯一值，主鍵 | U49bbc79ed892a8b8357a3699327850da |
| User_State | VARCHAR(20) | 否 | 使用者目前狀態 | None、change1、change2 | None |
| user_dislike | TEXT | 是 | 使用者不喜歡的食材 | 以逗號分隔的食材名稱 | 洋蔥,青椒 |

#### 完整性限制說明

| 欄位名稱 | 值域限制說明 | 確認方式（MySQL） |
|---------|-------------|-----------------|
| LINE_ID | 必須為LINE提供的有效使用者識別碼，長度固定，且不可為空 | CHECK (LINE_ID REGEXP '^U[a-f0-9]{32}$') |
| User_State | 不可為空，且只能出現 None、change1、change2文字 | CHECK (User_State IS NULL   OR User_State IN ('None', 'change1', 'change2') ) |
| user_dislike | 可為空，若不為空則必須以逗號分隔各個食材名稱 | 無需額外限制 |

```sql
CREATE TABLE User (
    LINE_ID VARCHAR(50) PRIMARY KEY,
    CHECK (
    User_State IS NULL 
    OR User_State IN ('None', 'change1', 'change2')
    ),
    user_dislike TEXT,
    CHECK (LINE_ID REGEXP '^U[a-f0-9]{32}$'),
    CHECK (User_State IS NULL OR CHAR_LENGTH(User_State) <= 20)
) ENGINE=InnoDB;


--  範例：插入一位使用者到 User 表
INSERT INTO User (LINE_ID, User_State, user_dislike)
VALUES (
    'U1234567890abcdef1234567890abcdef',             -- LINE_ID：使用者LINE唯一ID，固定格式U開頭+32位小寫十六進位
    '選擇食材中',                                     -- User_State：目前使用者狀態（可為 NULL）
    '不喜香菜、不吃牛肉'                              -- user_dislike：使用者忌口內容（例如過敏、討厭食物）
);
```

### 🥬 Ingredient 資料表

#### 基本欄位

| 欄位名稱 | 資料型態 | 是否可為空 | 欄位說明 | 值域/限制 | 實際資料舉例 |
|---------|----------|------------|----------|------------|-------------|
| Ingredient_ID | INT | 否 | 食材編號（主鍵） | 唯一 | 1 |
| Ingredient_Name | VARCHAR(50) | 否 | 長度1~50的文字 | 任意食材名稱 | 番茄 |

#### 完整性限制說明

| 欄位名稱 | 值域限制說明 | 確認方式（MySQL） |
|---------|-------------|-----------------|
| Ingredient_ID | 必須為大於 0 的整數，且不可為空，作為主鍵需保證唯一性 | 使用 AUTO_INCREMENT 確保遞增且唯一 |
| Ingredient_Name | 必須為長度 1 到 50 個字元的文字，且不可為空，同一食材名稱不得重複 | CHECK (CHAR_LENGTH(Ingredient_Name) BETWEEN 1 AND 50) |

```sql
CREATE TABLE Ingredient (
    Ingredient_ID INT PRIMARY KEY AUTO_INCREMENT,
    Ingredient_Name VARCHAR(50) NOT NULL UNIQUE,
    CHECK (CHAR_LENGTH(Ingredient_Name) BETWEEN 1 AND 50)
);


-- 範例：插入一筆食材資料到 Ingredient 表
INSERT INTO Ingredient (Ingredient_Name)
VALUES (
    '雞蛋'                                            -- Ingredient_Name：單一個食材名稱（唯一）
);
```

### 🥣 User_Ingredients 資料表

#### 基本欄位

| 欄位名稱           | 資料型態        | 是否可為空 | 欄位說明          | 值域/限制                         | 實際資料舉例                            |
| -------------- | ----------- | ----- | ------------- | ----------------------------- | --------------------------------- |
| LINE\_ID       | VARCHAR(50) | 否     | 使用者的 LINE 識別碼 | 參照 `User.LINE_ID`             | U49bbc79ed892a8b8357a3699327850da |
| Ingredient\_ID | INT         | 否     | 食材的識別編號       | 參照 `Ingredient.Ingredient_ID` | 5                                 |
| Quantity       | INT | 是     | 食材數量          | 為空或為大於 0 的整數         | 2                                 |


#### 完整性限制說明


| 欄位名稱           | 值域限制說明                                       | 確認方式（MySQL）                                                        |
| -------------- | -------------------------------------------- | ------------------------------------------------------------------ |
| LINE\_ID       | 必須存在於 `User` 表中的 `LINE_ID`，且不可為空             | `FOREIGN KEY (LINE_ID) REFERENCES User(LINE_ID)`                   |
| Ingredient\_ID | 必須存在於 `Ingredient` 表中的 `Ingredient_ID`，且不可為空 | `FOREIGN KEY (Ingredient_ID) REFERENCES Ingredient(Ingredient_ID)` |
| Quantity       | 可為空，若不為空則必須為正整數                              | `CHECK (Quantity IS NULL OR Quantity > 0)`         |


```sql
CREATE TABLE User_Ingredients (
    LINE_ID VARCHAR(50) NOT NULL,
    Ingredient_ID INT NOT NULL,
    QuantityINT,
    FOREIGN KEY (LINE_ID) REFERENCES User(LINE_ID),
    FOREIGN KEY (Ingredient_ID) REFERENCES Ingredient(Ingredient_ID),
    CHECK (Quantity IS NULL OR Quantity > 0),
    PRIMARY KEY (LINE_ID, Ingredient_ID)
);


-- 範例：插入一筆使用者食材資料到 User_Ingredients 表
INSERT INTO User_Ingredients (LINE_ID, Ingredient_ID, Quantity)
VALUES (
    'U1234567890abcdef1234567890abcdef',
    (SELECT Ingredient_ID FROM Ingredient WHERE Ingredient_Name = '雞蛋'),
    2
);
```

### ⭐ Favorite_recipes 資料表

#### 基本欄位

| 欄位名稱 | 資料型態 | 是否可為空 | 欄位說明 | 值域/限制 | 實際資料舉例 |
|---------|----------|------------|----------|------------|-------------|
| LINE_ID | VARCHAR(50) | 否 | 使用者的 LINE 識別碼 | 參照 User.LINE_ID | U49bbc79ed892a8b8357a3699327850da |
| Recipe_ID | INT | 否 | 食譜編號 | 參照 Recipe.Recipe_ID | 101 |
| Favorite_time | DATETIME | 否 | 加入最愛的時間 | 格式：YYYY-MM-DD HH:MM:SS | 2025-06-05 15:00:00 |
| Note | TEXT | 是 | 備註說明 | 任意文字 | 小孩愛吃|

#### 完整性限制說明

| 欄位名稱 | 值域限制說明 | 確認方式（MySQL） |
|---------|-------------|-----------------|
| LINE_ID | 必須存在於 User 表中的 LINE_ID，且不可為空 | FOREIGN KEY (LINE_ID) REFERENCES User(LINE_ID) |
| Recipe_ID | 必須存在於 Recipe 表中的 Recipe_ID，且不可為空 | FOREIGN KEY (Recipe_ID) REFERENCES Recipe(Recipe_ID) |
| Favorite_time | 必須為有效的日期時間格式，且不可為空 | 無需額外限制（MySQL內建驗證） |
| Note | 可為空，若不為空則可包含任意文字 | 無需額外限制 |

```sql
CREATE TABLE Favorite_recipes (
    LINE_ID VARCHAR(50) NOT NULL,
    Recipe_ID INT NOT NULL,
    Favorite_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Note TEXT,
    FOREIGN KEY (LINE_ID) REFERENCES User(LINE_ID),
    FOREIGN KEY (Recipe_ID) REFERENCES Recipe(Recipe_ID),
    PRIMARY KEY (LINE_ID, Recipe_ID)
) ENGINE=InnoDB;


-- 範例：插入一筆使用者收藏的食譜資料到 Favorite_recipes 表
INSERT INTO Favorite_recipes (LINE_ID, Recipe_ID, Note)
VALUES (
    'U1234567890abcdef1234567890abcdef', 
    1, 
    '這個炒蛋真的很好吃，下次加蔥花試試'
);
```


---



### ER_Diagram
![ER_Diagram](https://github.com/user-attachments/assets/025c373d-5013-4ce7-8012-3a2428ebf0fc) 



### 資料表結構

#### 1. User (使用者資料表)
| 欄位名稱 | 說明 |
|----------|------|
| LINE_ID | 使用者LINE的ID |
| User_State | 使用者狀態 |
| User_dislike | 使用者不喜歡的食材 |

#### 2. User_Ingredients (使用者食材資料表)
| 欄位名稱 | 說明 |
|----------|------|
| User_ID | 使用者LINE的ID |
| Ingredients | 食材名稱 |
| Quantity | 食材數量 |

#### 3. Favorite_recipes (使用者喜愛食譜資料表)
| 欄位名稱 | 說明 |
|----------|------|
| LINE_ID | 使用者LINE的ID |
| Recipe_ID | 食譜的ID |
| Favorite_time | 新增喜愛的時間 |
| Note | 使用者備註 |

#### 4. Recipe (食譜推資料表)
| 欄位名稱 | 說明 |
|----------|------|
| Recipe_ID | 食譜的編號 |
| Recipe_Name | 食譜的名稱 |
| Recipe_photo_url | 食譜照片的網址 |
| Recipe_url | 食譜的網址 |
| Ingredient | 食譜中的食材 |

#### 5.Ingredient (食材資料表)
| 欄位名稱 | 說明 |
|----------|------|
| Ingredient_Name | 食材的名稱 |
| Ingredient_ID | 食材的編號 |



## 詳細說明

### 資料表關聯說明

#### User_Indgredients的外來鍵(FK)LINE_ID參照User的主鍵(PK)LINE_ID​
- 一個User可以有多個使用者食材​

#### Favorite_recipes的外來鍵(FK)LINE_ID參照User的主鍵(PK)LINE_ID​
- 一個User可以有多個收藏食譜​

#### Favorite_recipes的外來鍵(FK)Recipe_ID參照Recipe的主鍵(PK)Recipe_ID​
- 每個食譜可以被多個使用者收藏​
#### User_Ingredient的外來鍵(FK)Ingredient_ID參照Ingredient的主鍵(PK)Ingredient_ID​ 
使用者食材可以引用多個食材​ 

---
## 使用者權限

### 1.使用者

| 資料表 | 權限 | 說明 |
|------|------|------|
| reipce | SELECT | 查看食譜 | 
| user | SELECT, INSERT, UPDATE | 修改使用者資料 |
| user_ingredients | SELECT, INSERT, UPDATE | 修改使用者食材 |
| favorite_recipes | SELECT, INSERT, UPDATE | 修改使用者收藏食譜 |
```sql
CREATE USER 'user'@'%' IDENTIFIED BY '123';
GRANT SELECT ON Recipe_DB.recipe TO 'user'@'%';
GRANT SELECT, INSERT, UPDATE ON Recipe_DB.user TO 'user'@'%';
GRANT SELECT, INSERT, UPDATE ON Recipe_DB.user_ingredients TO 'user'@'%';
GRANT SELECT, INSERT, UPDATE ON Recipe_DB.favorite_recipes TO 'user'@'%';
FLUSH PRIVILEGES;
```
### 2.管理員
| 資料表 | 權限 | 說明 |
|------|------|------|
| recipe | SELECT, INSERT, UPDATE,CREATE VIEW, DELETE | 管理食譜資料表 |
| ingredients | SELECT, INSERT, UPDATE,CREATE VIEW, DELETE | 管理食材資料表 |
```sql
CREATE USER 'admin'@'%' IDENTIFIED BY '246';
GRANT SELECT, INSERT, UPDATE, CREATE VIEW, DELETE ON Recipe_DB.recipe TO 'admin'@'%';
GRANT SELECT, INSERT, UPDATE,CREATE VIEW, DELETE ON Recipe_DB.ingredients TO 'admin'@'%';
FLUSH PRIVILEGES;
```
### 3.資料庫管理員
| 資料表 | 權限 | 說明 |
|------|------|------|
| user | ALL | 管理使用者資料 |
| user_ingredients | ALL | 管理使用者食材 |
| favorite_recipes | ALL | 管理使用者收藏食譜 |
| recipe | ALL | 管理食譜資料表 |
| ingredients | ALL | 管理食材資料表 |
```sql
CREATE USER 'DBadmin'@'%' IDENTIFIED BY '888';
GRANT ALL PRIVILEGES ON Recipe_DB.* TO 'DBadmin'@'%';
FLUSH PRIVILEGES;
```

## View

### 1. 查看使用者的最愛食譜詳細資訊
```sql
CREATE VIEW View_User_Favorites AS
SELECT 
    u.LINE_ID,
    r.Recipe_ID,
    r.Recipe_Name,
    r.Ingredient,
    r.Instructions,
    r.Recipe_url,
    r.Recipe_photo_url,
    f.Favorite_time,
    f.Note
FROM Favorite_recipes f
JOIN User u ON f.LINE_ID = u.LINE_ID
JOIN Recipe r ON f.Recipe_ID = r.Recipe_ID;
```
### 使用方式
```sql
SELECT *
FROM View_User_Favorites
WHERE LINE_ID = 'Ub9ec4bdf56708afd81be89b65c16034f';
```
### 說明
- 此功能可查詢使用者（以 LINE_ID 識別）所收藏的食譜資訊，包含：
  - 食譜編號與名稱。
  - 所需食材與步驟說明。
  - 食譜來源連結與圖片。
  - 收藏時間與個人備註等。
- 詳情
  - 結合 User、Favorite_recipes 以及 Recipe 三個資料表，透過 JOIN 取得完整的收藏紀錄與食譜內容，並儲存至 View 中供快速查詢使用。  
 
### 執行結果
![image](https://github.com/user-attachments/assets/838356e5-619f-402b-a16e-d9746e102a99)

### 2. 查看使用者持有的所有食材與數量
```sql
CREATE VIEW View_User_Ingredients AS
SELECT 
    u.LINE_ID,
    ui.Ingredients AS Ingredient_Name,
    ui.Quantity
FROM User u
JOIN User_Ingredients ui ON u.LINE_ID = ui.LINE_ID;
```
### 使用方式
```sql
-- 查詢指定 LINE_ID 使用者目前的所有食材庫存
SELECT *
FROM View_User_Ingredients
WHERE LINE_ID = 'Ub9ec4bdf56708afd81be89b65c16034f';
```
### 說明
- 此功能可查詢使用者當前持有的所有食材及其數量。
- 詳情
  - 結合 User 與 User_Ingredients 表，透過 JOIN 將使用者的 LINE_ID 與食材名稱、數量做結合。
 
### 執行結果
![image](https://github.com/user-attachments/assets/0f9046f5-d978-4166-9962-2f58bccd1692)



### 資料來源
- 食譜資料來源(我們有經過同意使用此網站的食譜資料):[https://icook.tw/](https://icook.tw/)
- ![許可圖片](https://github.com/user-attachments/assets/05c4b26c-286f-44d9-a19b-cd9603e94158)





