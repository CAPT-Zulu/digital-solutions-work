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

// API Send
function apiSend(request) {
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

// Search System
const Search = (input, elements, parent) => {
    let result = 0;
    // For every element to search through check if the element is related to the search query and hide it if it doesn't
    for (const element of elements) {
        if (element.innerHTML.toLowerCase().includes(input.value.toLowerCase())) {
            element.parentElement.parentElement.style.display = 'flex';
            result++;
        } else {
            element.parentElement.parentElement.style.display = 'none';
        }
    }
    // If there are no results show a message (edit this to remove the option to not sure the error msg)
    const error_msg = document.querySelector('.search-noresults');
    if (!result) {
        const msgelement = document.createElement('h1');
        msgelement.innerHTML = 'No results found';
        msgelement.classList.add('search-noresults');
        if (!error_msg) {
            parent.appendChild(msgelement);
        }
    } else {
        if (error_msg) {
            error_msg.remove();
        }
    }
};

// Countdown System
if (document.getElementById('time')) {
    let start = new Date;
    start.setHours(23, 0, 0); // 11pm

    function pad(num) {
        return ("0" + parseInt(num)).substr(-2);
    }

    function tick() {
        let now = new Date;
        if (now > start) { // too late, go to tomorrow
            start.setDate(start.getDate() + 1);
        }
        let remain = ((start - now) / 1000);
        let hh = pad((remain / 60 / 60) % 60);
        let mm = pad((remain / 60) % 60);
        let ss = pad(remain % 60);
        let pr = -((remain / 86400) * 100 - 100)
        document.getElementById('time').innerHTML = hh + " hours, " + mm + " minutes and " + ss + " seconds.";
        document.getElementById('time_bar').style.width = (pr + "%");
        setTimeout(tick, 1000);
    }

    document.addEventListener('DOMContentLoaded', tick);
}

// Get Settings
const getSettings = async function() {
    // Create promise to prevent the result being an unfulfilled promise
    return new Promise((resolve, reject) => {
        // Attempt to get settings
        try {
            // Return the settings found in JSON format
            resolve(JSON.parse($('script[type="text/json"]#').text()));
        } catch (ex) {
            // Error de-bugging
            console.log("ERROR: Error occurred while getting data! Error type " + ex);
            reject(ex);
        }
    });
};

// Request Questions
const getQuestions = async function(categories,limit,diff,tags) {
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
            parent.innerHTML = "You won!";
            return null
        }
    }
    let question = json[i];
    // set the next question
    i++
    let incorrect = 0
    // Create the question container
    let container = await createChild(parent,"div",{className:"question-container"});
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
                    let request = {id:question['id'],diff:question['difficulty'],inc:incorrect};
                    apiSend(request);
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
        let questions = await getQuestions(urlParams.get('cat'),5,urlParams.get('diff'),urlParams.get('tags'));
        createQuestion(quiz, questions, 0,questions.length);
    }
}
createQuiz();

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