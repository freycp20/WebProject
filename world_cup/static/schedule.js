window.addEventListener("DOMContentLoaded", async () => {
    let button = document.getElementById("refresh-leaderboard")
    // button.style.width = "50px";
    // button.style.height = "40px";
    // button.style.padding = "50px";

    button.addEventListener("click", refresh_scores);
})

function refresh_scores() {
    url = "/get-user-scores/"
    console.log("here")
    fetch(url)
        .then(validateJSON)
        .then(update_table)
}
function update_table(data) {
    let tableBody = document.getElementById("leaderboard-body")
    tableBody.innerHTML = ""
    // const items = Object.values(data).sort((first, second) => {
    //     return second - first;
    // });

    for (const item of sortObj(data)) {
        let tr = document.createElement("tr")

        let name = document.createElement("td")
        name.innerText = item[0]

        let score = document.createElement("td")
        score.innerText = item[1]

        tr.appendChild(name)
        tr.appendChild(score)
        tableBody.appendChild(tr)
    }
}

function sortObj(obj) {
    // Sort object as list based on values
    return Object.keys(obj).map(k => ([k, obj[k]])).sort((a, b) => (b[1] - a[1]))
}

/**
 * Validate a response to ensure the HTTP status code indcates success.
 * 
 * @param {Response} response HTTP response to be checked
 * @returns {object} object encoded by JSON in the response
 */
 function validateJSON(response) {
    if (response.ok) {
        return response.json();
    } else {
        return Promise.reject(response);
    }
}