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

#### 1. 不知道如何處理剩餘食材
許多人在家中有多種剩餘食材，卻不確定如何搭配來製作餐點。系統可以根據食材自動推薦合適的食譜，讓你善用剩餘食材，解決食材浪費的問題。

#### 2. 時間有限，不知道做什麼菜
忙碌的生活讓許多人沒有時間去計劃餐點，尤其是下班後精疲力盡時。系統能快速提供多種餐點選擇，省去思考要做什麼的煩惱，提升效率。

#### 3. 不熟悉食材或廚藝技巧
有些人可能對某些食材不熟悉，或者不知道該如何烹調。透過系統的食譜推薦與詳細的製作步驟，使用者可以學習如何使用不同的食材來烹飪出美味的餐點。

### 👥 使用案例

#### 案例一：忙碌的上班族
**需求：**
- 工作繁忙，沒有時間計劃餐點
- 希望能在家吃得健康

**解決方案：**
1. 根據使用者輸入食材（如高麗菜、豬肉、牛肉）
2. 系統迅速推薦食譜，節省使用者時間

#### 案例二：烹飪新手
**需求：**
- 廚藝經驗不足
- 不熟悉製作過程與食材使用比例

**解決方案：**
1. 根據使用者輸入所需的食材
2. 系統迅速推薦食譜，並提供詳細的食譜製作過程

## 系統架構

### 技術堆疊
- 前端介面：LINE Bot
- 後端開發：Flask / Python
- 資料庫系統：phpMyAdmin

## 資料庫結構

### 完整性限制
#### 📘 Recipe 資料表

| 欄位名稱         | 說明         | 資料型態 | 是否為空 | 值域                  |
|------------------|--------------|----------|-----------|-----------------------|
| `Recipe_ID`      | 食譜 ID      | 只允許數字    | N         | 從 1 開始的整數        |
| `Recipe_Name`    | 食譜名稱     | 只允許文字  | N         | 長度 1~100 的文字      |
| `Ingredient`     | 食譜所需食材 | 全部皆可    | N         | 長度 0~250 的文字      |
| `Instructions`   | 食譜步驟     | 全部皆可      | N         | 長度 0~500 的文字      |
| `Recipe_photo_url` | 食譜圖片連結 | 只允許文字  | Y         | 長度 0~255 的文字，網址(包含 http 或 https )，只能使用ASCII 字元，且須符合RFC 3986 標準     |

---

#### 👤 User 資料表

| 欄位名稱               | 說明               | 資料型態 | 是否為空 | 值域                  |
|------------------------|--------------------|----------|-----------|-----------------------|
| `User_ID`              | 使用者 ID          | 只允許數字     | N         | 從 1 開始的整數        |
| `LINE_ID`              | LINE ID            | 只允許文字  | N         | 長度 1~50 的文字，輸入僅限半形英數字，及「.」「-」「_」等3種類的符號       |
| `User_State`           | 使用者狀態         | 只允許文字  | Y         | 長度 0~20 的文字       |
| `Change_id`            | 使用者欲更改食材   | 只允許數字      | Y         | 長度 0~500 的文字      |
| `User_Last_Ingredients`| 上次輸入的食材     | 全部皆可     | Y         | 長度 0~250 的文字      |
| `User_Last_recipes`    | 上次推薦的食譜     | 全部皆可     | Y         | 長度 0~250 的文字      |

---

#### 🥣 User_Ingredients 資料表

| 欄位名稱             | 說明         | 資料型態 | 是否為空 | 值域                  |
|----------------------|--------------|----------|-----------|-----------------------|
| `User_Ingredients_ID`| 使用者食材 ID| 只允許數字      | N         | 從 1 開始的整數        |
| `LINE_ID`            | LINE ID      | 只允許文字  | N         | 長度 1~50 的文字，輸入僅限半形英數字，及「.」「-」「_」等3種類的符號      |
| `Database_Ingredients`| 食材名稱    | 只允許文字  | N         | 長度 1~100 的文字      |
| `Quantity`           | 數量         | 只允許數字     | N         | 從 0 開始的整數        |

---

#### 🍽️ Recipe_recommend 資料表

| 欄位名稱             | 說明             | 資料型態 | 是否為空 | 值域                                           |
|----------------------|------------------|----------|-----------|------------------------------------------------|
| `User_ID`            | 使用者 ID        | 只允許數字     | N         | 參考 `User.User_ID`                            |
| `User_Ingredients_ID`| 使用者食材 ID    | 只允許數字     | N         | 參考 `User_Ingredients.User_Ingredients_ID`    |
| `Recipe_ID`          | 食譜 ID          | 只允許數字     | N         | 參考 `Recipe.Recipe_ID` |
![食譜資料表](https://github.com/user-attachments/assets/b654f910-51d2-4c88-bfef-e896fe29d220)
![使用者資料表](https://github.com/user-attachments/assets/2a17b1b3-d871-4f59-bfcc-1a1f93cb2db2)
![使用者持有食材](https://github.com/user-attachments/assets/6605d210-6fdc-488d-bb12-9966aa12fd1b)
![食譜推薦結果](https://github.com/user-attachments/assets/db0c44f0-9f63-46d7-b83e-1ba0ed8b0dd0)


### ER Diagram
![ER Diagram](https://github.com/user-attachments/assets/73ce79ed-2156-4b2a-bcff-ba7195cc0f08)

### 資料表結構

#### 1. Recipe (食譜資料表)
| 欄位名稱 | 說明 |
|----------|------|
| Recipe_ID | 食譜ID |
| Recipe_Name | 食譜名稱 |
| Ingredient | 食譜所需食材 |
| Instructions | 步驟 |
| Recipe_photo_url | 食譜照片 |

#### 2. User (使用者資料表)
| 欄位名稱 | 說明 |
|----------|------|
| User_ID | 使用者ID |
| LINE_ID | LINE ID |
| User_State | 使用者狀態 |
| Change_id | 使用者欲更改食材 |
| User_Last_Ingredients | 使用者上一次輸入食材 |
| User_Last_recipes | 使用者上一次推薦食譜 |

#### 3. User_Ingredients (使用者持有食材資料表)
| 欄位名稱 | 說明 |
|----------|------|
| User_Ingredients_ID | 使用者食材ID |
| LINE_ID | LINE ID |
| Database_Ingredients | 持有食材名稱 |
| Quantity | 數量 |

#### 4. Recipe_recommend (食譜推薦結果資料表)
| 欄位名稱 | 說明 |
|----------|------|
| User_ID | 使用者ID |
| User_Ingredients_ID | 使用者食材ID |
| Recipe_ID | 食譜ID |

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





