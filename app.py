from flask import Flask, request, jsonify, send_file, render_template
import pandas as pd
import os

app = Flask(__name__, static_folder='.', template_folder='.')  # 指定当前目录为静态文件目录

# 读取Excel文件
print("Current working directory:", os.getcwd())
EXCEL_FILE = "/home/ElizaYU/lotto_program/会员名单测试版.xlsx"  # 请确保该文件存在
WINNERS_FILE = '中奖名单.xlsx'
print("Excel file path:", EXCEL_FILE)

df = pd.read_excel(EXCEL_FILE)
winners = pd.DataFrame(columns=df.columns)

# 主页面路由
@app.route('/')
def index():
    return render_template('index.html')

# 获取会员名单
@app.route('/get_names', methods=['GET'])
def get_names():
    names = df['会员'].tolist()
    return jsonify({'names': names})

# 添加中奖者
@app.route('/add_winner', methods=['POST'])
def add_winner():
    global winners
    data = request.json
    index = data['index']
    name = data['name']
    new_winner = df[df['序号'] == index]
    if not new_winner.empty:
        winners = pd.concat([winners, new_winner], ignore_index=True)
        winners.to_excel(WINNERS_FILE, index=False)
    return jsonify({'status': 'success'})

# 下载中奖名单
@app.route('/download_winners', methods=['GET'])
def download_winners():
    if not os.path.exists(WINNERS_FILE):
        return jsonify({'error': '中奖名单文件不存在'}), 404
    return send_file(WINNERS_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
