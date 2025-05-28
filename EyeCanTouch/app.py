from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def page1():
    return render_template('page1.html')

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/page3')
def page3():
    return render_template('page3.html')

@app.route('/page4')
def page4():
    return render_template('page4.html')

@app.route('/page5')
def page5():
    return render_template('page5.html')

@app.route('/page6')
def page6():
    return render_template('page6.html')

@app.route('/page7')
def page7():
    return render_template('page7.html')

@app.route('/page8')
def page8():
    return render_template('page8.html')

@app.route('/page9')
def page9():
    return render_template('page9.html')

@app.route('/page10')
def page10():
    return render_template('page10.html')

@app.route('/page11')
def page11():
    return render_template('page11.html')

@app.route('/lowpage1')
def lowpage1():
    return render_template('lowpage1.html')

@app.route('/lowpage2')
def lowpage2():
    return render_template('lowpage2.html')

@app.route('/lowpage3')
def lowpage3():
    return render_template('lowpage3.html')

@app.route('/lowpage4')
def lowpage4():
    return render_template('lowpage4.html')

@app.route('/lowpage5')
def lowpage5():
    return render_template('lowpage5.html')

@app.route('/lowpage6')
def lowpage6():
    return render_template('lowpage6.html')

@app.route('/lowpage7')
def lowpage7():
    return render_template('lowpage7.html')

@app.route('/lowpage8')
def lowpage8():
    return render_template('lowpage8.html')

@app.route('/lowpage9')
def lowpage9():
    return render_template('lowpage9.html')

@app.route('/lowpage10')
def lowpage10():
    return render_template('lowpage10.html')

@app.route('/lowpage11')
def lowpage11():
    return render_template('lowpage11.html')

if __name__ == '__main__':
    # 외부 IP에서 접근할 수 있도록 설정
    app.run(host='0.0.0.0', port=1999, debug=True)