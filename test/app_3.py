# app.py
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'user_data.db'

# 模擬資料庫連線
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/user_info', methods=['GET'])
def get_user_info():
    # --- 故意引入的【不安全寫法】: SQL 注入漏洞 ---
    
    # 程式直接從 URL 參數獲取使用者名稱
    user_id = request.args.get('user_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 警告：此處使用 f-string (或字串連接) 將未經過濾的使用者輸入直接拼接到 SQL 語句中
    # 這是危險的，攻擊者可以輸入 ' OR '1'='1 --' 來繞過驗證
    query = f"SELECT username, email FROM users WHERE user_id = {user_id}"
    
    # 執行不安全的查詢
    cursor.execute(query) 
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user)), 200
    else:
        return jsonify({"error": "User not found"}), 404

# 範例：不安全的 exec() 呼叫
def run_command(command_input):
    # --- 另一個【不安全寫法】: 不安全的 exec/eval ---
    
    # 警告：exec() 執行任何傳入的字串，若字串來自外部輸入，將導致任意程式碼執行
    exec(command_input) 
    
    return "Command attempted."


if __name__ == '__main__':
    # 為了測試，您可以先運行一次這個函數，但實際漏洞在 get_user_info 中
    run_command('print("Hello from exec")') 
    
    app.run(debug=True)