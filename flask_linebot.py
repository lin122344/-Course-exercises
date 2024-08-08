from flask import Flask, redirect, url_for #flask 是工具箱(moduie模組)，Flask是工具(Class類別)

app = Flask(__name__)#製作出一個由Flask類別生成的物件(Object)

@app.route("/")  #裝飾器 :跟目錄要做什麼事
def say_hello_world(username=""):
    return "<h1>Hello, World!</h1>"

@app.route("/tell_me_a_joke")  #裝飾器 :跟目錄要做什麼事
def tell_me_a_joke():
    return "<h1>Ha ha ha ha</h1>"

@app.route("/eat/<string:what_fruit>")  #裝飾器 :跟目錄要做什麼事
def eat_fruit(what_fruit):
    return redirect(url_for('say_fruit_is_gone',fruit=what_fruit)) # url_for(route_function_name)

@app.route("/<string:fruit>")  #裝飾器 :跟目錄要做什麼事
def say_apple_is_gone(fruit):
    return "<h1>" + fruit + " is gone.</h1>"


#如果我直接執行這個檔案,_name_ 就等於_main_

if __name__=='_main_':

#在command_line 下: flask--app flask_linebot.py run
    app.run(debug=True)


