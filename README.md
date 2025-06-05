# 食譜查詢資料庫系統
使用者輸入他所持有的食材，系統會依照使用者所提供的食材，進行最佳的食譜推薦。
## 📋 目錄
- [組員資訊](#組員資訊)
- [應用情境與使用案例](#應用情境與使用案例)
- [系統架構](#系統架構)
- [資料庫結構](#資料庫結構)
- [詳細說明](#詳細說明)
- [資料庫Schema](#資料庫Schema)

## 組員資訊

| 學號 | 姓名 | 分工 |
|------|------|------|
| 41143247 | 葉紘愷 | 資料庫架構 |
| 41143251 | 蔡沅杰 | 資料爬蟲 |
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

![使用案例圖](https://github.com/user-attachments/assets/d2d7bfe0-fff6-4fc1-b585-3ca5a731ba84)

![使用案例圖](https://github.com/user-attachments/assets/f21126c9-21eb-4390-bab3-4693852f7022)

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

# 資料庫結構說明

## 完整性限制

### 📋 Recipe 資料表

| 欄位名稱 | 資料型態 | 是否可為空 | 欄位說明 | 值域/限制 | 實際資料舉例 |
|---------|----------|------------|----------|------------|-------------|
| Recipe_ID | INT | 否 | 食譜編號（主鍵） | 自動編號，唯一 | 101 |
| Recipe_Name | VARCHAR(100) | 否 | 食譜名稱 | 任意名稱 | 羅宋湯 |
| Ingredient | TEXT | 否 | 使用食材列表 | 以文字描述所需食材，以,分隔 | 番茄,馬鈴薯 |
| Instructions | TEXT | 是 | 食譜步驟說明 | 任意文字 | 半顆的洋蔥切丁、紅蘿蔔、馬玲薯切丁... |
| Recipe_url | TEXT | 是 | 詳細食譜連結 | 合法 URL | https://example.com/recipe |
| Recipe_photo_url | TEXT | 是 | 食譜圖片網址 | 合法圖片 URL | https://imgur.com/pasta.jpg |

```sql
CREATE TABLE Recipe (
    Recipe_ID INT PRIMARY KEY AUTO_INCREMENT,
    Recipe_Name VARCHAR(100) NOT NULL,
    Ingredient TEXT NOT NULL,
    Instructions TEXT,
    Recipe_url TEXT,
    Recipe_photo_url TEXT
);

-- 範例資料
INSERT INTO Recipe (Recipe_Name, Ingredient, Instructions, Recipe_url, Recipe_photo_url)
VALUES ('羅宋湯', '番茄,馬鈴薯', '半顆的洋蔥切丁、紅蘿蔔、馬玲薯切丁...', 'https://example.com/recipe', 'https://imgur.com/pasta.jpg');
```

### 👤 User 資料表

| 欄位名稱 | 資料型態 | 是否可為空 | 欄位說明 | 值域/限制 | 實際資料舉例 |
|---------|----------|------------|----------|------------|-------------|
| LINE_ID | VARCHAR(50) | 否 | 使用者的 LINE 識別碼 | 唯一值，主鍵 | U49bbc79ed892a8b8357a3699327850da |
| User_State | VARCHAR(20) | 是 | 使用者目前狀態 | 任意狀態描述文字 | none |
| user_dislike | TEXT | 是 | 使用者不喜歡的食材 | 以逗號分隔的食材名稱 | 洋蔥,青椒 |

```sql
CREATE TABLE User (
    LINE_ID VARCHAR(50) PRIMARY KEY,
    User_State VARCHAR(20),
    user_dislike TEXT
);

-- 範例資料
INSERT INTO User (LINE_ID, User_State, user_dislike)
VALUES ('U49bbc79ed892a8b8357a3699327850da', 'none', '洋蔥,青椒');
```

### 🥬 Ingredient 資料表

| 欄位名稱 | 資料型態 | 是否可為空 | 欄位說明 | 值域/限制 | 實際資料舉例 |
|---------|----------|------------|----------|------------|-------------|
| Ingredient_ID | INT | 否 | 食材編號（主鍵） | 唯一 | 1 |
| Ingredient_Name | VARCHAR(50) | 否 | 食材名稱 | 任意食材名稱 | 番茄 |

```sql
CREATE TABLE Ingredient (
    Ingredient_ID INT PRIMARY KEY AUTO_INCREMENT,
    Ingredient_Name VARCHAR(50) NOT NULL
);

-- 範例資料
INSERT INTO Ingredient (Ingredient_Name) VALUES ('番茄');
```

### 🥣 User_Ingredients 資料表

| 欄位名稱 | 資料型態 | 是否可為空 | 欄位說明 | 值域/限制 | 實際資料舉例 |
|---------|----------|------------|----------|------------|-------------|
| LINE_ID | VARCHAR(50) | 否 | 使用者的 LINE 識別碼 | 參照 User.LINE_ID | U49bbc79ed892a8b8357a3699327850da |
| Ingredients | VARCHAR(50) | 否 | 食材名稱 | 任意食材名稱 | 馬鈴薯 |
| Quantity | VARCHAR(20) | 是 | 食材數量 | > 0 的整數 | 2 |

```sql
CREATE TABLE User_Ingredients (
    LINE_ID VARCHAR(50) NOT NULL,
    Ingredients VARCHAR(50) NOT NULL,
    Quantity VARCHAR(20),
    FOREIGN KEY (LINE_ID) REFERENCES User(LINE_ID),
    CHECK (CAST(Quantity AS SIGNED) > 0 OR Quantity IS NULL)
);

-- 範例資料
INSERT INTO User_Ingredients (LINE_ID, Ingredients, Quantity)
VALUES ('U49bbc79ed892a8b8357a3699327850da', '馬鈴薯', '2');
```

### ⭐ Favorite_recipes 資料表

| 欄位名稱 | 資料型態 | 是否可為空 | 欄位說明 | 值域/限制 | 實際資料舉例 |
|---------|----------|------------|----------|------------|-------------|
| LINE_ID | VARCHAR(50) | 否 | 使用者的 LINE 識別碼 | 參照 User.LINE_ID | U49bbc79ed892a8b8357a3699327850da |
| Recipe_ID | INT | 否 | 食譜編號 | 參照 Recipe.Recipe_ID | 101 |
| Favorite_time | DATETIME | 否 | 加入最愛的時間 | 格式：YYYY-MM-DD HH:MM:SS | 2025-06-05 15:00:00 |
| Note | TEXT | 是 | 備註說明 | 任意文字 |  |

```sql
CREATE TABLE Favorite_recipes (
    LINE_ID VARCHAR(50) NOT NULL,
    Recipe_ID INT NOT NULL,
    Favorite_time DATETIME NOT NULL,
    Note TEXT,
    FOREIGN KEY (LINE_ID) REFERENCES User(LINE_ID),
    FOREIGN KEY (Recipe_ID) REFERENCES Recipe(Recipe_ID),
    PRIMARY KEY (LINE_ID, Recipe_ID)
);

-- 範例資料
INSERT INTO Favorite_recipes (LINE_ID, Recipe_ID, Favorite_time)
VALUES ('U49bbc79ed892a8b8357a3699327850da', 101, '2025-06-05 15:00:00');
```

## 資料庫關聯圖

使用者（User）可以:
1. 擁有多個喜愛的食譜（Favorite_recipes）
2. 擁有多個食材（User_Ingredients）
3. 每個食譜（Recipe）可以被多個使用者收藏
4. 每個食材（Ingredient）可以被多個使用者擁有

## 注意事項

1. 所有的 LINE_ID 都需要參照 User 表的 LINE_ID
2. Recipe_ID 需要參照 Recipe 表的 Recipe_ID
3. 日期時間格式統一使用 YYYY-MM-DD HH:MM:SS
4. 食材數量必須為正整數
5. URL 需要是合法的網址格式
---



### ER Diagram
![Chenerdiagram1](https://github.com/user-attachments/assets/3e717033-d061-4bb0-88fe-160e0db90727)



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

#### 3. Favorite_Ingredients (使用者喜愛食譜資料表)
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

#### Recipe 與 Recipe_Recommend (1..n)
- 一個推薦結果可以對應到多個食譜
- 一個食譜只能對應到一個推薦結果

#### User 與 Recipe_Recommend (1..n)
- 一個推薦結果只會對應到一個使用者
- 一個使用者可以有很多推薦結果

#### User_Ingredients 與 Recipe_Recommend (1..n)
- 一個推薦結果會對應到多個使用者食材
- 每個使用者食材必須對應到一個推薦結果

---

## 資料庫Schema

### 📋 目錄
- [資料表概覽](#資料表概覽)
- [詳細資料表結構](#詳細資料表結構)
  - [Recipe (食譜資料表)](#1-recipe-食譜資料表)
  - [User (使用者資料表)](#2-user-使用者資料表)
  - [User_Ingredients (使用者持有食材資料表)](#3-user_ingredients-使用者持有食材資料表)
  - [Recipe_recommend (食譜推薦結果資料表)](#4-recipe_recommend-食譜推薦結果資料表)
- [資料表範例](#資料表範例)

### 資料表概覽
本系統包含四個主要資料表，用於管理食譜推薦系統：
- Recipe：儲存食譜基本資訊
- User：管理使用者資料
- User_Ingredients：追蹤使用者擁有的食材
- Recipe_recommend：記錄推薦結果

#### 詳細資料表結構

#### 1. Recipe (食譜資料表)

```sql
CREATE TABLE Recipe (
    Recipe_ID INT PRIMARY KEY AUTO_INCREMENT,
    Recipe_Name VARCHAR(100) NOT NULL,
    Ingredient TEXT NOT NULL,
    Instructions TEXT NOT NULL,
    Recipe_photo_url VARCHAR(255)
);
```

##### 欄位說明
| 欄位名稱 | 資料型態 | 說明 | 備註 |
|----------|----------|------|------|
| Recipe_ID | INT | 食譜唯一識別碼 | 主鍵，自動遞增 |
| Recipe_Name | VARCHAR(100) | 食譜名稱 | 不可為空 |
| Ingredient | TEXT | 所需食材清單 | 不可為空 |
| Instructions | TEXT | 烹飪步驟說明 | 不可為空 |
| Recipe_photo_url | VARCHAR(255) | 食譜照片URL | 可為空 |

#### 2. User (使用者資料表)

```sql
CREATE TABLE User (
    User_ID INT PRIMARY KEY AUTO_INCREMENT,
    LINE_ID VARCHAR(50) NOT NULL UNIQUE,
    User_State VARCHAR(20) DEFAULT 'None',
    Change_id INT,
    User_Last_Ingredients TEXT,
    User_Last_recipes TEXT
);
```

##### 欄位說明
| 欄位名稱 | 資料型態 | 說明 | 備註 |
|----------|----------|------|------|
| User_ID | INT | 使用者唯一識別碼 | 主鍵，自動遞增 |
| LINE_ID | VARCHAR(50) | LINE平台使用者ID | 不可重複 |
| User_State | VARCHAR(20) | 使用者狀態 | 預設值：'None' |
| Change_id | INT | 欲更改食材ID | 可為空 |
| User_Last_Ingredients | TEXT | 上次輸入食材 | 可為空 |
| User_Last_recipes | TEXT | 上次推薦食譜 | 可為空 |

#### 3. User_Ingredients (使用者持有食材資料表)

```sql
CREATE TABLE User_Ingredients (
    User_Ingredients_ID INT PRIMARY KEY AUTO_INCREMENT,
    LINE_ID VARCHAR(50) NOT NULL,
    Database_Ingredients VARCHAR(100) NOT NULL,
    Quantity INT DEFAULT 1,
    FOREIGN KEY (LINE_ID) REFERENCES User(LINE_ID)
);
```

##### 欄位說明
| 欄位名稱 | 資料型態 | 說明 | 備註 |
|----------|----------|------|------|
| User_Ingredients_ID | INT | 食材記錄識別碼 | 主鍵，自動遞增 |
| LINE_ID | VARCHAR(50) | 使用者LINE ID | 外鍵參照User表 |
| Database_Ingredients | VARCHAR(100) | 食材名稱 | 不可為空 |
| Quantity | INT | 數量 | 預設值：1 |

#### 4. Recipe_recommend (食譜推薦結果資料表)

```sql
CREATE TABLE Recipe_recommend (
    User_ID INT NOT NULL,
    User_Ingredients_ID INT NOT NULL,
    Recipe_ID INT NOT NULL,
    PRIMARY KEY (User_ID, User_Ingredients_ID, Recipe_ID),
    FOREIGN KEY (User_ID) REFERENCES User(User_ID),
    FOREIGN KEY (User_Ingredients_ID) REFERENCES User_Ingredients(User_Ingredients_ID),
    FOREIGN KEY (Recipe_ID) REFERENCES Recipe(Recipe_ID)
);
```

##### 欄位說明
| 欄位名稱 | 資料型態 | 說明 | 備註 |
|----------|----------|------|------|
| User_ID | INT | 使用者ID | 複合主鍵之一 |
| User_Ingredients_ID | INT | 使用者食材ID | 複合主鍵之一 |
| Recipe_ID | INT | 食譜ID | 複合主鍵之一 |

### 資料表範例

#### 1. Recipe (食譜資料表) 範例資料
```sql
-- 新增食譜範例
INSERT INTO Recipe (Recipe_Name, Ingredient, Instructions, Recipe_photo_url) VALUES
(
    '蔥花炒蛋',
    '蔥,雞蛋,鹽,胡椒粉',
    '1. 雞蛋打散加入適量鹽調味\n2. 蔥切段\n3. 熱油鍋\n4. 倒入蛋液\n5. 加入蔥花\n6. 翻炒均勻\n7. 最後撒上胡椒粉調味',
    'https://example.com/recipes/egg-with-green-onion.jpg'
);
```

#### 2. User (使用者資料表) 範例資料
```sql
-- 新增使用者範例
INSERT INTO User (LINE_ID, User_State, User_Last_Ingredients, User_Last_recipes) VALUES
(
    'Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1',
    'None',
    '番茄,雞蛋',
    '1,2'
);
```

#### 3. User_Ingredients (使用者持有食材資料表) 範例資料
```sql
-- 新增使用者食材範例
INSERT INTO User_Ingredients (LINE_ID, Database_Ingredients, Quantity) VALUES
(
    'Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1',
    '番茄',
    2
);
```
### 資料來源
- 食譜資料來源(我們有經過同意使用此網站的食譜資料):[https://icook.tw/](https://icook.tw/)
- ![許可圖片](https://github.com/user-attachments/assets/05c4b26c-286f-44d9-a19b-cd9603e94158)





