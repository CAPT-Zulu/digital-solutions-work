// Create Element
const createChild = async function(parent,element,attributes) {
    // Create promise to prevent the result being an unfulfilled promise
    return new Promise((resolve, reject) => {
        try {
            // Create and append child element with parameters
            let child = parent.appendChild(Object.assign(document.createElement(element),attributes));
            // Return the child element
            resolve(child);
        } catch (ex) {
            // Error de-bugging
            console.log("ERROR: Error occurred while appending child element '" + String(element) + "' to parent '" + parent.outerHTML + "' with parameters '" + JSON.stringify(attributes) + "'! Error type " + ex);
            reject(ex);
        }
    });
};

// url parameters const
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

// API Question Send
function apiQuestionSend(request) {
    try {
        $.ajax({
            type: "POST",
            contentType: "application/json;charset=utf-8",
            url: "/api",
            traditional: "true",
            data: JSON.stringify(request),
            dataType: "json"
        });
    } catch (ex) {
        // Error de-bugging
        console.log("ERROR: Error occurred while posting data! Error type " + ex);
    }
}

// API Get Leaderboard
const apiGetLeader = async function(event_id) {
    // Create promise to prevent the result being an unfulfilled promise
    return new Promise((resolve, reject) => {
        // Attempt to get questions
        try {
            // Create the API url and add ID parameter
            let url = '/api?id=' + event_id;
            console.log('DEBUG BASE URL:', url);
            // Using jQuery ajax request the API url with parameters
            $.ajax({
                url: url,
                async: true,
                cache: false,
                dataType: 'json',
                error: function() {
                    // Error de-bugging
                    throw 'COULD NOT GET A VALID JSON FROM THE URL';
                }
            }).then((json) => {
                // If the API responded return the json to the function
                if (json!=null && Object.keys(json).length>0) {
                    console.log('DEBUG DATA/JSON:', json); //DEBUG ALL DATA FROM JSON
                    resolve(json);
                } else {
                    // Error de-bugging
                    throw 'TOPIC IS INVALID / NO QUESTIONS FOUND';
                }
            }).catch((err, json) => {
                // Error de-bugging
                console.log("ERROR: '" + err + "' DEBUG: ", json);
            });
        } catch (ex) {
            // Error de-bugging
            console.log("ERROR: Error occurred while getting data! Error type " + ex);
            reject(ex);
        }
    });
};

// Get Settings
function getSettings() {
    // Return data found inside script data tag
    return JSON.parse(document.getElementById('data').textContent);
}

// Request Questions
const getQuestions = async function(categories,limit,diff,tags,comp) {
    // Create promise to prevent the result being an unfulfilled promise
    return new Promise((resolve, reject) => {
        // Attempt to get questions
        try {
            // Create the API url and add any parameters if necessary
            let url = 'https://the-trivia-api.com/api/questions?';
            if (categories) {url += ('categories=' + categories)}
            if (limit) {url += ('&limit=' + limit)}
            if (diff) {url += ('&difficulty=' + diff)}
            if (tags) {url += ('&tags=' + tags)}
            console.log('DEBUG BASE URL:', url);
            // Using jQuery ajax request the API url with parameters
            $.ajax({
                url: url,
                async: true,
                cache: false,
                dataType: 'json',
                error: function() {
                    // Error de-bugging
                    throw 'COULD NOT GET A VALID JSON FROM THE URL';
                }
            }).then((json) => {
                // If the API responded return the json to the function
                if (json!=null && Object.keys(json).length>0) {
                    // Set result json to json
                    let json_result = json
                    console.log('DEBUG DATA/JSON:', json_result); //DEBUG ALL DATA FROM JSON
                    // Remove questions that are in comp
                    for (let step = 0; step < Object.keys(comp).length; step++) {
                        // If there are less than 1 question which the user has not completed ignore completed questions
                        if (Object.keys(json_result).length < 1) {
                            // Resolve the questions
                            resolve(json)
                        } else {
                            // Else remove completed questions from available questions
                            json_result = json_result.filter(e => e !== comp[step]);
                        }
                    }
                    // Resolve the questions
                    resolve(json_result);
                } else {
                    // Error de-bugging
                    throw 'TOPIC IS INVALID / NO QUESTIONS FOUND';
                }
            }).catch((err, json) => {
                // Error de-bugging
                console.log("ERROR: '" + err + "' DEBUG: ", json);
            });
        } catch (ex) {
            // Error de-bugging
            console.log("ERROR: Error occurred while getting data! Error type " + ex);
            reject(ex);
        }
    });
};

// Create Question
async function createQuestion(parent,json,i,max) {
    // Clear previous question
    parent.innerHTML = "";
    // Get data for current question
    if (i>=max) {
        if (parent.className === "quiz-loop") {
            let questions = await getQuestions('',5,'','');
            createQuestion(parent, questions, 0,questions.length);
        } else {
            parent.innerHTML = "You have completed the QUIZ! Play again?";
            return null
        }
    }
    let question = json[i];
    // set the next question
    i++
    let incorrect = 0
    // Create the question container
    let container = await createChild(parent,"div",{className:"question-container"});
    // Create question counter
    await createChild(container,"p",{innerText:(i + "/" + max)})
    // Create the question h1 element
    await createChild(container,"h1",{className:"",innerText:question['question']});
    // Create div container for the buttons
    let button_container = await createChild(container,"div",{className:"question-buttons"});
    // Get the amount of answers SHITTING'S
    let a = (question['incorrectAnswers'].length + 1);
    let c = Math.floor(Math.random() * a)
    let f = 0
    // Create the buttons
    for (let step = 0; step < a; step++) {
        if (step===c) {
            await createChild(button_container,"button",{
                class:"",
                innerText:question['correctAnswer'],
                onclick: function() {
                    console.log("Correct Answer!", question);
                    let request = {event:urlParams.get('id'),id:question['id'],diff:question['difficulty'],
                        inc:incorrect};
                    apiQuestionSend(request);
                    createQuestion(parent,json,i,max);
                }
            });
        } else {
            await createChild(button_container, "button", {
                class: "",
                innerText: question['incorrectAnswers'][f],
                onclick: function () {
                    console.log("Incorrect Answer!", question);
                    this.style.backgroundColor = "red";
                    incorrect++
                }
            });
            f++;
        }
    }
}

// Create Quiz
async function createQuiz() {
    // Check if a quiz exists on the page
    let quiz = document.getElementById("quiz");
    // If a quiz exists get questions sort out the questions a user has already answered and then load the first question
    if (quiz) {
        // Get settings
        let data = getSettings()
        // Get Questions
        let questions = await getQuestions(data['categories'],10,data['difficulty'],'',data['comp']);
        createQuestion(quiz, questions, 0,questions.length);
    }
}
createQuiz();

// Create Leader Board
// Create Quiz
async function createLeader() {
    // Check if a leaderboard exists on the page
    let board = document.getElementById("leaderboard");
    // If a leaderboard exists get the current leaderboard
    if (board) {
            let leaderboard_interval = setInterval(async function () {
                let data = await apiGetLeader(urlParams.get('id'));
                board.innerHTML = "";
                for (let i=0; i < data['data'].length; i++) {
                    board.innerHTML += "<div class='card-container'><h2>" + (i+1) + "</h2><h2>" + data['data'][i] + "</h2></div>";
                }

            }, 6000);
    }
}
createLeader();

// Old Stuff
// async function startUp() {
        // for (let question in questions) {
        //     quiz.innerHTML += ("<div><div><h1>" + questions[question]['question'] + "</h1></div><div><p>" + questions[question]['id'] + "</p></div></div>");
        // }
        // let settings = await getSettings();
        // if (settings !== undefined) {
        //     let questions = await getQuestions('',1,'','');
        //     quiz.innerHTML = ("<div><div><h1>" + questions[0][0] + "</h1></div><div><p>" + questions[0][1] + "</p></div></div>");
        // }
//     }
// }
// async function startUp() {
//     let quiz_data = document.getElementById("quiz_data");
//     if (quiz_data) {
//         let questions = await getQuestions('',5,'','');
//         quiz_data.value = JSON.stringify({questions});
//         quiz_data.parentElement.innerHTML +=("<button type=\"submit\">Play Quiz!</button>")
//     }
//     // try {
//     //     let questions = await getQuestions('',5,'','')
//     //     $.ajax({
//     //         type: "POST",
//     //         contentType: "application/json;charset=utf-8",
//     //         url: "/index",
//     //         traditional: "true",
//     //         data: JSON.stringify({questions}),
//     //         dataType: "json"
//     //     });
// 	// } catch (ex) {
// 	// 	console.log("ERROR: Error occurred while getting data! Error type " + ex);
//     // }
// }
// <script id="my_model" type="text/json">
//   {{ my_model|json_encode()|raw }}
// </script>
// Startup on page load
// document.onload = startUp()