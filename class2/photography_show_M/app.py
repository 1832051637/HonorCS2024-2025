from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/navigation')
def navigation():
    return render_template('pie_navigation.html')

@app.route('/discovery')
def discovery():
    return render_template('discovery.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/author')
def author():
    return render_template('author.html')

# 修改作者作品路由部分
@app.route('/author/1')
def author1_works():
    author = {
        "name": "Ansel Adams",
        "specialty": "街头摄影专家，擅长捕捉城市瞬间",
        "intro": "Ansel Adams（安塞尔·亚当斯）是美国著名风光摄影师，以黑白摄影展现美国西部壮丽景色闻名。他开创了区域曝光法，对摄影艺术和环境保护有深远影响。代表作有《月升，赫尔南德斯》和《半圆山，冬日日出》。"
    }
    works = [{"image": f"works/author1/photo_{i}.jpg", "title": f"作品{i}", "desc": "摄影作品描述"} for i in range(1, 6)]
    return render_template('author_works.html', author=author, works=works, author_id=1)

@app.route('/author/2')
def author2_works():
    author = {
        "name": "Henri Cartier-Bresson",
        "specialty": "人像摄影大师",
        "intro": "Henri Cartier-Bresson（亨利·卡蒂埃-布列松）被誉为“决定性瞬间之父”，是纪实摄影和街头摄影的奠基人之一。他善于捕捉生活中转瞬即逝的精彩画面，影响了无数摄影师。"
    }
    works = [{"image": f"works/author2/photo_{i}.jpg", "title": f"作品{i}", "desc": "摄影作品描述"} for i in range(1, 6)]
    return render_template('author_works.html', author=author, works=works, author_id=2)

@app.route('/author/3')
def author3_works():
    author = {
        "name": "Annie Leibovitz",
        "specialty": "自然风光摄影师",
        "intro": "Annie Leibovitz（安妮·莱博维茨）是美国著名肖像摄影师，以为《滚石》《名利场》等杂志拍摄名人肖像而闻名。她的作品风格大胆、富有创意，极具视觉冲击力。"
    }
    works = [{"image": f"works/author3/photo_{i}.jpg", "title": f"作品{i}", "desc": "摄影作品描述"} for i in range(1, 6)]
    return render_template('author_works.html', author=author, works=works, author_id=3)

@app.route('/author/4')
def author4_works():
    author = {
        "name": "Robert Capa",
        "specialty": "纪实摄影师",
        "intro": "Robert Capa（罗伯特·卡帕）是著名战地摄影师，以拍摄战争前线的真实场景著称。他共同创办了玛格南图片社，代表作有诺曼底登陆等战争影像。"
    }
    works = [{"image": f"works/author4/photo_{i}.jpg", "title": f"作品{i}", "desc": "摄影作品描述"} for i in range(1, 6)]
    return render_template('author_works.html', author=author, works=works, author_id=4)

@app.route('/author/5')
def author5_works():
    author = {
        "name": "Cindy Sherman",
        "specialty": "概念摄影艺术家",
        "intro": "Cindy Sherman（辛迪·舍曼）是美国当代摄影艺术家，以自我扮演和概念摄影闻名。她通过镜头探讨身份、性别和社会角色等主题，作品极具思想性和艺术性。"
    }
    works = [{"image": f"works/author5/photo_{i}.jpg", "title": f"作品{i}", "desc": "摄影作品描述"} for i in range(1, 6)]
    return render_template('author_works.html', author=author, works=works, author_id=5)

if __name__ == '__main__':
    app.run(debug=True, port=8000)