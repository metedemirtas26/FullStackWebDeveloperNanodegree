from flask import Flask, request, redirect, url_for

from forumdb import get_firstQuestion, get_secondQuestion, get_thirdQuestion

app = Flask(__name__)

HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Logs Analysis Project</title>
  </head>
  <body>
    <h1>Logs Analysis Project</h1>
    <tr><h3>
    Question <br>
    </h3>
    %s
    </tr>
  </body>
</html>
'''

QUERYRESULT1 = '''\
    &nbsp <td class=post>"%s" --- %s views</td> <br>
'''

QUERYRESULT2 = '''\
    &nbsp <td class=post>%s --- %s views</td> <br>
'''

QUERYRESULT3 = '''\
    &nbsp <td class=post>%s --- %s percent errors</td> <br>
'''


@app.route('/', methods=['GET'])
def main():
    '''Main page of the forum.'''
    resultOfFirstQuestions = "".join(QUERYRESULT1 % (
        title, views) for title, views in get_firstQuestion())
    html = HTML_WRAP % resultOfFirstQuestions
    return html


@app.route('/1', methods=['GET'])
def main1():
    '''Main page of the forum.'''
    resultOfFirstQuestions = "".join(QUERYRESULT1 % (
        title, views) for title, views in get_firstQuestion())
    html = HTML_WRAP % resultOfFirstQuestions
    return html


@app.route('/2', methods=['GET'])
def main2():
    resultOfSecondQuestions = "".join(QUERYRESULT2 % (
        name, views) for name, views in get_secondQuestion())
    html = HTML_WRAP % resultOfSecondQuestions
    return html


@app.route('/3', methods=['GET'])
def main3():
    resultOfThirdQuestions = "".join(QUERYRESULT3 % (
        name, views) for name, views in get_thirdQuestion())
    html = HTML_WRAP % resultOfThirdQuestions
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
