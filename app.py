from flask import Flask, render_template, request, send_from_directory, session
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置一个用于加密session数据的密钥，替换为实际的密钥

# 读取西语 Excel 文件
data_es = pd.read_excel('yunjin_s.xlsx')
# 将西语数据转换为字典，方便查询
data_dict_es = data_es.set_index('中文').T.to_dict()

# 读取日语 Excel 文件
data_ja = pd.read_excel('yunjin_j1.xlsx')
# 将日语数据转换为字典，方便查询
data_dict_ja = data_ja.set_index('中文').T.to_dict()


@app.route('/')
def index():
     # 当用户访问主页时，清除之前记录的语言选择（如果存在），让用户可以重新选择
    session.pop('language', None)
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    # 获取用户选择的语言，如果是首次搜索，从表单获取并存入session
    if 'language' not in session:
        session['language'] = request.form['language']
    language = session['language']
    query = request.form['query']

    if language == 'es':
        # 如果选择西语，查询西语数据
        result = data_dict_es.get(query, None)
        return render_template('search_result.html', query=query, result=result)
    elif language == 'ja':
        # 如果选择日语，查询日语数据
        result = data_dict_ja.get(query, None)
        return render_template('search_for_japan.html', query=query, result=result)


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    app.run(debug=True)