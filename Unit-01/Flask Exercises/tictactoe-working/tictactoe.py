from flask import Flask, render_template, request, redirect, url_for, session, flash
import random #needed for random number generation

app = Flask(__name__)

app.config['SECRET_KEY'] = 'myverysecretkey' #used so session cookies can be encryptec


def check_for_winner(player):

    #initialise result
    result = False
    #check rows
    for i in range(3):
        if session['board'][i][0] == player and session['board'][i][1] == player \
                and session['board'][i][2] == player:
            result = True

    #check columns
    if result == False:
        for i in range(3):
            if session['board'][0][i] == player and session['board'][1][i] == player \
                    and session['board'][2][i] == player:
                result = True

    #check diagonals
    if result == False:
        if session['board'][0][0] == player and session['board'][1][1] == player \
            and session['board'][2][2] == player:
            result = True
        else:
            if session['board'][2][0] == player and session['board'][1][1] == player \
                and session['board'][0][2] == player:
                result = True
    # return result
    return result



@app.route("/")
def index():
    #check if get variables exist
    if request.args.get('r') and request.args.get('c'):
        #retrieve the get variables
        r = int(request.args.get('r'))
        c = int(request.args.get('c'))

        #adjust the game board for user choice
        session['board'][r][c] = 'x'

        #check if won
        r = check_for_winner('x')
        #if won ...
        if r is True:
            flash('Congratulations you won!')
            session['gameon'] = False

        # else do computer turn
        else:
            #generate random number for cc and cr
            r = random.randint(0,2)
            c = random.randint(0,2)
            #check if cc and cr is a valid option
            while session['board'][r][c] != '-':
                r = random.randint(0, 2)
                c = random.randint(0, 2)
            #update game board
            session['board'][r][c] = 'o'
            #check if computer has one
            r = check_for_winner('o')
            if r is True:
                flash('You lost!')
                session['gameon'] = False


    # otherwise start new game
    else:
        #initialise game board
        session['board'] = [['-','-','-'], ['-','-','-'], ['-','-','-']]
        #set gameon to be true
        session['gameon'] = True
        #message user to confirm new game
        flash('New game started!')

    #update game board
    session['board'] = session['board']
    # render template and pass variables to template
    return render_template('tictactoe.html', board=session['board'], gameon=session['gameon'])


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    app.run(host, port, debug=True)