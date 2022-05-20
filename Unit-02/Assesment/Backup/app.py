from flask import Flask, render_template, request, redirect, flash, session, url_for
from datetime import datetime, date
from flask_wtf import FlaskForm
import sqlite3
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectMultipleField, SelectField, widgets
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, URL, Optional, InputRequired

app = Flask(__name__)

# Security Key
app.config['SECRET_KEY'] = 'QALXWwcS1OloO3K9kqPqtkhIF/5UARf6WqQ7T88jx4cfjfsDoZqD59SRNdgqWeIuEcc762AX7th4zXv4CVGsgHNJfTkugXj8A1A8u1S3mjoeSt6F0GgERPpXrIaVNtjIXRW61VDyuH5xERGjJBoBLW1Xb9UoyyiiZCiVsMccpsI='

# Connect database
con = sqlite3.connect('static/databases/system.db', check_same_thread=False)
cur = con.cursor()

# TODO:
#   Make the other page designs paper
#   Do all the verifications for every html page and device stuff
#   all the other stuff

### Form models ####
class NoValSelectMultipleField(SelectMultipleField):
    # form.validate_on_submit() does not work with SelectMultipleField unless validation is disabled
    # but flask automactically prefroms a "pre_validation" even if you have validation off
    # so I made this class to bypass pre_validation

    # Quotes from a devloper for wtforms ("SelectFields can now skip choice validation", "I did not add the validate_choice option to SelectMultipleField which was probably a mistake.")
    # SelectMultipleField did not recive the "validate_choice=False" feature that SelectField did

    def pre_validate(self, form):
        """per_validation is disabled"""

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Log In')

class CreateTopic(FlaskForm):
    topicName = StringField('Topic Name:', validators=[DataRequired()])
    classID = SelectField("Select a Class from The Dropdown:", coerce=int, validate_choice=False, validators=[DataRequired()])
    submit = SubmitField('Create Topic')

class DeleteTopic(FlaskForm):
    topicID = SelectField('Select The Topic To Delete:', coerce=int, validate_choice=False, validators=[DataRequired()])
    submit = SubmitField('Delete Topic')

class SubmitVideo(FlaskForm):
    videoTitle = StringField('Video Title:', validators=[DataRequired()])
    videoDescription = StringField('Video Description:', validators=[DataRequired()])
    videoURL = StringField('Video URL:', validators=[DataRequired(message="You must submit a URL"), URL(message="Not a valid URL")])
    videoTopics = NoValSelectMultipleField('Video Topics:', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit Video')

class EditVideo(FlaskForm):
    videoTitle = StringField('Video Title:', validators=[DataRequired()])
    videoDescription = StringField('Video Description:', validators=[DataRequired()])
    videoURL = StringField('Video URL:', validators=[DataRequired(message="You must submit a URL"), URL(message="Not a valid URL")])
    videoTopics = NoValSelectMultipleField('Video Topics:', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Resubmit Video')

## Functions ###
def GetVideos(userID, search_request, topic_id, pending, order, limit):
    if userID:
        sql_videos = """
                    SELECT DISTINCT *
                    FROM videos
                    WHERE video_id IN (    
                        SELECT video_id 
                        FROM video_topics
                        WHERE topic_id IN (   
                            SELECT topic_id
                            FROM classes_topics
                            WHERE class_id IN (
                                SELECT class_id
                                FROM users_classes
                                WHERE user_id = ?))
                        AND topic_id LIKE ?)
                    AND video_title LIKE ?
                    AND video_pending LIKE ?
                    ORDER BY ? DESC
                    LIMIT ?;"""
        cur.execute(sql_videos, (userID, ('%' + topic_id + '%'), ('%' + search_request + '%'), ('%' + pending + '%'), order, limit,))
        result_videos = cur.fetchall()

        sql_flags = """     
                    SELECT video_id
                    FROM users_flagged_videos
                    WHERE user_id = ?;"""
        cur.execute(sql_flags, (userID,))

        # Another issue with the results should be that the output should be like ['1','4','8','2'] instead I was getting [('1,'),('4,'),('8,'),('2,')] To fix this I made an for loop to remove that comma.
        # This isnt a good final solution but I could not find any documentation on why this was.
        result_flags = []
        for flag in cur.fetchall():
            result_flags.append(flag[0])

        return result_videos, result_flags
    else:
        # If user doesnt exist must be getting videos for the index page while logged out.

        sql_videos2 = """
                    SELECT *
                    FROM videos 
                    WHERE video_title LIKE ?
                    AND video_pending LIKE ?
                    ORDER BY ? DESC
                    LIMIT ?;"""
        cur.execute(sql_videos2, (('%' + search_request + '%'), ('%' + pending + '%'), order, limit,))
        result_videos2 = cur.fetchall()

        return [result_videos2]

def GetClases(userID,getList):
    results = []
    # To prevent unnecessary sql querys being run and not having to have 3 different functions I made it so I can grab whichever combination I need
    if 'subjects' in getList:
        sql_subjects = """
                    SELECT *
                    FROM subjects
                    WHERE subject_code IN (
                        SELECT subject_code
                        FROM classes
                        WHERE class_id IN (
                            SELECT class_id
                            FROM users_classes
                            WHERE user_id = ?));"""
        cur.execute(sql_subjects, (userID,))
        result_subjects = cur.fetchall()

        results.append(result_subjects)
    if 'classes' in getList:
        sql_classes = """
                    SELECT *
                    FROM classes c, subjects s
                    WHERE class_id IN (
                        SELECT class_id
                        FROM users_classes
                        WHERE user_id = ?)
                    AND c.subject_code = s.subject_code;"""
        cur.execute(sql_classes, (userID,))
        result_classes = cur.fetchall()

        results.append(result_classes)
    if 'topics' in getList:
        sql_topics = """
                    SELECT t.topic_id, topic_description, c.class, c.subject_code, s.subject_description
                    FROM topics t, classes_topics ct, classes c, users_classes us, subjects s
                    WHERE t.topic_id = ct.topic_id
                    AND ct.class_id = c.class_id
                    AND c.class_id = us.class_id
                    AND us.user_id = ?
                    AND c.subject_code = s.subject_code;"""
        cur.execute(sql_topics, (userID,))
        result_topics = cur.fetchall()

        results.append(result_topics)

    return results

########## routes ##########
@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    # Set LoginForm
    form = LoginForm()
    # If the user is logged in view recent videos
    if session.get('username'):
        # Teacher parameters
        if session['is_teacher']:
            pending = 'false'
            order = 'date_uploaded'
        else:
            pending = 'false'
            order = 'date_accepted'

        result_videos = GetVideos(session['user_id'], '', '', pending, order, 12)

        return render_template('index.html', title='Video Search', result_videos=result_videos)
    else:
        # If the user is trying to log in using POST
        if request.method == 'POST':
            if form.validate_on_submit():
                # Set username and password variables
                un = form.username.data
                pw = form.password.data

                # Check users if the combination of username and password exists
                sql_user = """
                                select *
                                from users 
                                where username = ?
                                and password = ?;"""
                cur.execute(sql_user, (un, pw,))
                result_user = cur.fetchall()

                # If a user with that username and password combination exists set session values with the users data
                if len(result_user) == 1:
                    session['user_id'] = result_user[0][0]
                    session['username'] = result_user[0][1]
                    session['is_teacher'] = result_user[0][3]
                    session['student_id'] = result_user[0][4]
                    session['staff_code'] = result_user[0][5]
                    session['firstname'] = result_user[0][6]
                    session['surname'] = result_user[0][7]
                    session['house'] = result_user[0][8]
                    session['year'] = result_user[0][9]

                    return redirect(url_for('index'))
                else:
                    flash("Username or password incorrect!")
            else:
                flash("There is something missing!")

        # If the user isnt logged in show only 3 videos
        result_videos = GetVideos('', '', '', 'false', 'date_accepted', 3)
        return render_template('index.html', title='Video Search', form=form, result_videos=result_videos)

@app.route('/logout')
def logout():
    # clear out the session
    if session.get('username'):
        session['user_id'] = None
        session['username'] = None
        session['is_teacher'] = None
        session['student_id'] = None
        session['staff_code'] = None
        session['firstname'] = None
        session['surname'] = None
        session['house'] = None
        session['year'] = None
        flash("You have successfully logged out")
    else:
        flash("You have to be logged in to do that!")
    return redirect(url_for('index'))

@app.route('/search')
def search():
    if session.get('username'):
        # If search args are found set it to search_request otherwise set search_request empty
        if request.args.get('search'):
            search_request = request.args.get('search')
        else:
            search_request = ''

        # If id args are found set it to topic_id otherwise set topic_id empty
        if request.args.get('id'):
            topic_id = request.args.get('id')
        else:
            topic_id = ''

        # Set differences from students and teachers searches
        if session['is_teacher'] == 'true':
            pending = ''
            order = 'date_uploaded'
        else:
            pending = 'false'
            order = 'date_accepted'

        # Get topics
        topics = GetClases(session['user_id'], ['topics'])

        # Get videos with previous parameters. Limit video amounts by 100 as this an only a concept my website doesn’t have pages.
        result_videos = GetVideos(session['user_id'], search_request, topic_id, pending, order, 100)

        # Render search page
        return render_template('search.html', title='Video Search', result_videos=result_videos, search_request=search_request, topics=topics)
    else:
        # User can't acsess this page unless the user is logged in
        flash("You have to be logged in to do that!")
        return redirect(url_for('index'))

@app.route('/video', methods=['GET','POST'])
def video():
    # If user had a username / logged in
    if session.get('username'):
        if request.args.get('id'):
            # Set video_id as the request arg
            video_id = request.args.get('id')

            # Check if the video_id is valid from the sql
            sql_video = """
                                SELECT *
                                FROM videos
                                WHERE video_id = ?;"""
            cur.execute(sql_video, (video_id,))
            result_video = cur.fetchall()

            # If results greater then 0 a video has been found
            if len(result_video)>0:
                # POST requests from videos options
                if request.method == "POST":
                    # Spaghetti elif statements for all the buttons
                    # Video flag btn
                    if request.form.get("flag_btn") == 'flag':
                        sql_flag = """
                                    INSERT INTO users_flagged_videos (user_id, video_id)
                                    VALUES (?, ?);"""
                        cur.execute(sql_flag, (session['user_id'], video_id,))
                        flash("Successfully flagged video!")
                    elif request.form.get("flag_btn") == 'unflag':
                        sql_flag = """
                                    DELETE FROM users_flagged_videos
                                    WHERE user_id = ?
                                    AND video_id = ?;"""
                        cur.execute(sql_flag, (session['user_id'], video_id,))
                        flash("Successfully unflagged video!")

                    # Video report btn
                    elif request.form.get("report_btn") == 'report':
                        sql_report = """
                                    UPDATE videos
                                    SET reported_url_issue = 'true'
                                    WHERE video_id = ?;"""
                        cur.execute(sql_report, (video_id,))
                        flash("Successfully reported broken link!")
                    elif request.form.get("report_btn") == 'unreport':
                        sql_report = """
                                    UPDATE videos
                                    SET reported_url_issue = 'false'
                                    WHERE video_id = ?;"""
                        cur.execute(sql_report, (video_id,))
                        flash("Successfully reported an okay link!")

                    # Video pending btn
                    elif request.form.get("pending_btn") == 'approve':
                        sql_pending = """
                                    UPDATE videos
                                    SET video_pending = 'false', date_accepted = 'Update'
                                    WHERE video_id = ?;"""
                        cur.execute(sql_pending, (video_id,))
                        flash("Successfully approved video")
                    elif request.form.get("pending_btn") == 'disapprove':
                        sql_pending = """
                                    UPDATE videos
                                    SET video_pending = 'true', date_accepted = '' 
                                    WHERE video_id = ?;"""
                        cur.execute(sql_pending, (video_id,))
                        flash("Successfully disapproved video")

                    # Commit changes I placed it outside for debugging and you only need it once for any buttons so to reduce the amount of times I need to type it its out here.
                    con.commit()

                # Get videos topics
                sql_topic = """
                                    SELECT vt.topic_id, t.topic_description
                                    FROM video_topics vt, topics t 
                                    WHERE vt.video_id = ?
                                    AND vt.topic_id = t.topic_id;"""
                cur.execute(sql_topic, (video_id,))
                result_topic = cur.fetchall()

                # Get other videos
                result_other_videos = GetVideos(session['user_id'], '', '', 'false', 'date_accepted', 12)

                # Combine results for the video with its topics to one variable
                results_video = result_video[0], result_topic

                # Render html
                return render_template('video.html', title=str(results_video[0][1]), results_video=results_video, result_other_videos=result_other_videos)
            else:
                # Else a video could not be found so flash a message to the user and return them to the search page
                flash("A video with that id does not exist!")
                return redirect(url_for('search'))
        else:
            # If the user trys to request the page without the id get variable flash them a message and return them to the search page
            flash("You have to have a video_id to be able to accsess that page!")
            return redirect(url_for('search'))
    else:
        # Only logged in useres should be able to acsess this page (at the momment)
        flash("You have to be logged in to do that!")
        return redirect(url_for('index'))

@app.route('/submitvideo', methods=['GET','POST'])
def submitvideo():
    form = SubmitVideo()
    if session.get('username'):
        topics = GetClases(session['user_id'],['topics'])

        if request.method == 'POST':
            if form.validate_on_submit():
                # Form vars
                videoTitle = form.videoTitle.data
                videoDescription = form.videoDescription.data
                videoURL = form.videoURL.data
                videoTopics = form.videoTopics.data

                # If teacher then video_pending = false and date_accepted = now
                if session['is_teacher']=='true':
                    video_pending = 'false'
                    date_accepted = 'Update'
                else:
                    video_pending = 'true'
                    date_accepted = None

                # Input new video ot videos table if student have it not enabled but if teacher do
                sql_video = """
                            INSERT INTO videos (video_title, video_description, video_url, video_submitted_by_user, video_pending, date_accepted)
                            VALUES (?, ?, ?, ?, ?, ?);"""
                cur.execute(sql_video, (videoTitle, videoDescription, videoURL, session['user_id'], video_pending, date_accepted))
                con.commit()

                # Get the video_id for the just submitted video
                video_id = cur.lastrowid

                # add topics for the video
                sql_topic = """
                            INSERT INTO video_topics(video_id, topic_id)
                            VALUES (?, ?);"""

                for topic in videoTopics:
                    cur.execute(sql_topic, (video_id, topic,))

                con.commit()

                flash("Video succesfully submitted!")
            else:
                flash("There is something missing or something is invalid!")

        return render_template('submitvideo.html', title='Submit Video', form=form, topics=topics)
    else:
        flash("You have to be logged in to do that!")
        return redirect(url_for('index'))

@app.route('/createtopic', methods=['GET','POST'])
def createtopic():
    form = CreateTopic()
    if session.get('username'):
        if session['is_teacher'] == 'true':
            if request.method == 'POST':
                if form.validate_on_submit():
                    # Assign form data to variables
                    topicName = form.topicName.data
                    classID = form.classID.data

                    # Insert into database
                    sql_topic = """
                                INSERT INTO topics (topic_description)
                                VALUES (?);"""
                    cur.execute(sql_topic, (topicName,))
                    con.commit()

                    # Get the video_id for the just submitted video
                    topic_id = cur.lastrowid

                    # add topics for the video
                    sql_class_topic = """
                                INSERT INTO classes_topics(class_id, topic_id)
                                VALUES (?, ?);"""
                    cur.execute(sql_class_topic, (classID, topic_id,))
                    con.commit()

                    flash("Topic succesfully created!")
                else:
                    flash("There is something missing or something is invalid!")

            classes = GetClases(session['user_id'], ['classes'])

            return render_template('createtopic.html', title='Create Topic', form=form, classes=classes)
        else:
            flash("You do not have permission to do that!")
            return redirect(url_for('index'))
    else:
        flash("You have to be logged in to do that!")
        return redirect(url_for('index'))

@app.route('/deletetopic', methods=['GET','POST'])
def deletetopic():
    form = DeleteTopic()
    if session.get('username'):
        if session['is_teacher'] == 'true':
            if request.method == 'POST':
                if form.validate_on_submit():
                    topicID = form.topicID.data

                    # Delete video topics
                    sql_video_topics = """
                                DELETE FROM video_topics
                                WHERE topic_id = ?;"""
                    cur.execute(sql_video_topics, (topicID,))
                    con.commit()

                    # Delete classes topics
                    sql_classes_topics = """
                                DELETE FROM classes_topics
                                WHERE topic_id = ?;"""
                    cur.execute(sql_classes_topics, (topicID,))
                    con.commit()

                    # Delete the topic itself
                    sql_topic = """
                                DELETE FROM topics
                                WHERE topic_id = ?;"""
                    cur.execute(sql_topic, (topicID,))
                    con.commit()

                    flash("Topic succesfully deleated!")
                else:
                    flash("There is something missing or something is invalid!")

            topics = GetClases(session['user_id'], ['topics'])

            return render_template('deletetopic.html', title='Delete Topic', form=form, topics=topics)
        else:
            flash("You do not have permission to do that!")
            return redirect(url_for('index'))

    else:
        flash("You have to be logged in to do that!")
        return redirect(url_for('index'))

@app.route('/editvideo', methods=['GET','POST'])
def editvideo():
    form = EditVideo()
    if session.get('username'):
        if request.args.get('id'):
            video_id = request.args.get('id')

            if session['is_teacher'] != 'true':
                sql_validation = """
                            SELECT *
                            FROM videos
                            WHERE video_id = ?
                            AND video_submitted_by_user = ?;"""
                cur.execute(sql_validation, (video_id, session['user_id'],))
                sql_validation = cur.fetchall()

                if len(sql_validation)<1:
                    flash("You don't have permission to do that!")
                    return redirect(url_for('search'))

            topics = GetClases(session['user_id'],['classes','topics'])

            if request.method == 'POST':
                if request.form.get("delete_btn") == 'delete':
                    # delete previous topics for video
                    sql_topic_delete = """
                                DELETE FROM video_topics
                                WHERE video_id = ?;"""
                    cur.execute(sql_topic_delete, (video_id,))
                    con.commit()

                    # delete flags associated with the video
                    sql_flags_delete = """
                                DELETE FROM users_flagged_videos
                                WHERE video_id = ?;"""
                    cur.execute(sql_flags_delete, (video_id,))
                    con.commit()

                    # delete the video
                    sql_video_delete = """
                                DELETE FROM videos
                                WHERE video_id = ?;"""
                    cur.execute(sql_video_delete, (video_id,))
                    con.commit()

                    flash("Video successfully deleted!")
                    return redirect(url_for('search'))

                elif form.validate_on_submit():
                    # Form vars
                    videoTitle = form.videoTitle.data
                    videoDescription = form.videoDescription.data
                    videoURL = form.videoURL.data
                    videoTopics = form.videoTopics.data

                    # If teacher then video_pending = false and date_accepted = now
                    if session['is_teacher']=='true':
                        video_pending = 'false'
                        date_accepted = 'Update'
                    else:
                        video_pending = 'true'
                        date_accepted = None

                    # Update video
                    sql_video = """
                                UPDATE videos 
                                SET video_title = ?, video_description = ?, video_url = ?, video_submitted_by_user = ?, video_pending = ?, date_accepted = ?
                                WHERE video_id = ?;"""
                    cur.execute(sql_video, (videoTitle, videoDescription, videoURL, session['user_id'], video_pending, date_accepted, video_id,))
                    con.commit()

                    # delete previous topics for video
                    sql_topic_delete = """
                                DELETE FROM video_topics
                                WHERE video_id = ?;"""
                    cur.execute(sql_topic_delete, (video_id,))
                    con.commit()

                    # add topics for the video
                    sql_topic_add = """
                                INSERT INTO video_topics(video_id, topic_id)
                                VALUES (?, ?);"""

                    for topic in videoTopics:
                        cur.execute(sql_topic_add, (video_id, topic,))

                    con.commit()

                    flash("Video succesfully resubmitted!")
                    return redirect(url_for('search'))
                else:
                    flash("There is something missing or something is invalid!")

            sql_video = """
                                SELECT *
                                FROM videos
                                WHERE video_id = ?;"""
            cur.execute(sql_video, (video_id,))
            result_video = cur.fetchall()

            if len(result_video) > 0:
                return render_template('editvideo.html', title='Edit Video', form=form, result_video=result_video[0], topics=topics)
            else:
                # Else a video could not be found so flash a message to the user and return them to the search page
                flash("A video with that id does not exist or you dont have acsess to it!")
                return redirect(url_for('search'))
        else:
            flash("You have to have a video_id to be able to acsess that page!")
            return redirect(url_for('search'))
    else:
        flash("You have to be logged in to do that!")
        return redirect(url_for('index'))

@app.route('/user')
def user():
    if session.get('username'):
        result_topics = GetClases(session['user_id'],['classes','topics'])
        return render_template('user.html', title='User Page', result_topics=result_topics)
    else:
        flash("You have to be logged in to do that!")
        return redirect(url_for('index'))

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    app.run(host, port, debug=True)
