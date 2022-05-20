from flask import Flask, render_template, request, redirect, url_for, session, flash
import random #needed for random number generation
# import pygame

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my-not-so-very-secret-key'

string_list = ['Paper','Scissors','Rock','Spock','Lizard']

@app.route("/")
def index():
    # Check if the get variables exist
    if request.args.get('game'):
        # Retrieve the get variables
        player_hand, ai_hand, player_wins, ai_wins = request.args.get('game').split('x')
        player_hand, ai_hand, player_wins, ai_wins = int(player_hand), int(ai_hand), int(player_wins), int(ai_wins)

        # Set game on to True
        gameon = True

        # Set Ai's turn
        ai_hand = random.randint(0, 4)

        # Check who won the round
        d = (5 + player_hand - ai_hand) % 5

        if player_hand == 9:
            flash('New game started!')
            gameon = True
            player_hand, ai_hand, player_wins, ai_wins = 0, 0, 0, 0
        elif d == 1 or d == 3:
            flash('You won the round!')
            player_wins += 1
        elif d == 2 or d == 4:
            flash('You lost the round!')
            ai_wins += 1
        elif d == 0:
            flash('The round is a tie!')

        # Check if someone won the game
        if player_wins >= 3:
            flash('Congratulations you won the game! :)')
            gameon = False
        elif ai_wins >= 3:
            flash('Congratulations you lost the game! :(')
            gameon = False

    # If no get vars are detected refresh with get vars
    else:
        return redirect(url_for('index', game='9x9x9x9'))

    # Render layout.html and pass variables to layout.html
    session['hands'] = player_hand,ai_hand,player_wins,ai_wins
    return render_template('layout.html', hands=session['hands'], gameon=gameon, string_list=string_list)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 5000
    app.run(host, port, debug=True)