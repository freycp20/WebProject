
window.addEventListener("DOMContentLoaded", async () => {
    setEventListeneners(9, 1)
    setEventListeneners(5, 2)
    setEventListeneners(3, 3)
    setEventListeneners(1, 4)

    document.getElementById("save_bracket").addEventListener("click", checkIfComplete)
    // for (let i=1; i<9; i++) {
        
    //     let h_t_input = document.getElementById(`round1_${i}_home_team`)
    //     let h_t_li = document.getElementById(`round1_${i}_home_team-li`)
    //     let h_t_label = document.getElementById(`round1_${i}_home_team-label`)
    //     let a_t_input = document.getElementById(`round1_${i}_away_team`)
    //     let a_t_li = document.getElementById(`round1_${i}_away_team-li`)
    //     let a_t_label = document.getElementById(`round1_${i}_away_team-label`)
    //     if (i%2 == 1) {
    //         h_t_input.addEventListener("click", evt => {
    //             setTeam(evt, h_t_label, "home_team")
    //         })
    //         a_t_input.addEventListener("click", evt => {
    //             setTeam(evt, a_t_label, "home_team")
    //         })
    //     } else {
    //         h_t_input.addEventListener("click", evt => {
    //             setTeam(evt, h_t_label, "away_team")
    //         })
    //         a_t_input.addEventListener("click", evt => {
    //             setTeam(evt, a_t_label, "away_team")
    //         })
    //     }
    //     console.log(h_t_input.getAttribute("next"))
    //     console.log(h_t_input)
    //     // a_t_input.addEventListener("click", evt => {
    //     //     // console.log(evt.target)
    //     //     // console.log(h_t_input)
    //     //     if (i%2 == 1) {
    //     //         let index = Math.floor((i-1)/2 + 1)
    //             // let next_input = document.getElementById(`round2_${index}_home_team`)
    //             // let next_label = document.getElementById(`round2_${index}_home_team-label`)
    //             // console.log(h_t_label)
    //             // console.log(h_t_input)
    //             // console.log(h_t_li)
    //             // console.log(next_label)
    //             // console.log(next_input)
    //             // next_input.type = "radio"
    //             // next_label.removeAttribute("hidden")
    //             // next_label.innerText = h_t_label.innerText
    //     //     } else {
    //     //         let index = Math.floor((i-1)/2 + 1)
    //     //         let next_input = document.getElementById(`round2_${index}_away_team`)
    //     //         let next_label = document.getElementById(`round2_${index}_away_team-label`)
    //     //         console.log(a_t_label)
    //     //         console.log(a_t_input)
    //     //         console.log(a_t_li)
    //     //         console.log(next_label)
    //     //         console.log(next_input)
    //     //         next_input.type = "radio"
    //     //         next_label.removeAttribute("hidden")
    //     //         next_label.innerText = a_t_label.innerText
    //     //     }
    //     //     // console.log(h_t.value)
    //     //     // let val = floor(i/2)
            
    //     //     // document.getElementById("round2_0_home_li").innerHTML = `<input type="radio" name="{{loop.index}}" id="{{}}_home_team" value="{{home_team}}">${h_t_li.innerText}</input<br>`
    //     //     // <input type="radio" name="{{loop.index}}" id="{{loop.index}}_home_team" value="{{home_team}}">{{match.home_team.name}}</input<br>

    //     //     // var team = document.getElementById("1_home_team").innerText
    //     //     // console.log(team4
    //     // })
    //     // h_t_input.addEventListener("click", evt => {
    //     //     // console.log(evt.target)
    //     //     // console.log(h_t_input)
    //     //     if (i%2 == 1) {
    //     //         let index = Math.floor((i-1)/2 + 1)
    //     //         let next_input = document.getElementById(`round2_${index}_home_team`)
    //     //         let next_label = document.getElementById(`round2_${index}_home_team-label`)
    //     //         console.log(h_t_label)
    //     //         console.log(h_t_input)
    //     //         console.log(h_t_li)
    //     //         console.log(next_label)
    //     //         console.log(next_input)
    //     //         next_input.type = "radio"
    //     //         next_label.removeAttribute("hidden")
    //     //         next_label.innerText = h_t_label.innerText
    //     //     } else {
    //     //         let index = Math.floor((i-1)/2 + 1)
    //     //         let next_input = document.getElementById(`round2_${index}_away_team`)
    //     //         let next_label = document.getElementById(`round2_${index}_away_team-label`)
    //     //         console.log(a_t_label)
    //     //         console.log(a_t_input)
    //     //         console.log(a_t_li)
    //     //         console.log(next_label)
    //     //         console.log(next_input)
    //     //         next_input.type = "radio"
    //     //         next_label.removeAttribute("hidden")
    //     //         next_label.innerText = a_t_label.innerText
    //     //     }
    //     //     // console.log(h_t.value)
    //     //     // let val = floor(i/2)
            
    //     //     // document.getElementById("round2_0_home_li").innerHTML = `<input type="radio" name="{{loop.index}}" id="{{}}_home_team" value="{{home_team}}">${h_t_li.innerText}</input<br>`
    //     //     // <input type="radio" name="{{loop.index}}" id="{{loop.index}}_home_team" value="{{home_team}}">{{match.home_team.name}}</input<br>

    //     //     // var team = document.getElementById("1_home_team").innerText
    //     //     // console.log(team4
    //     // })
    // }
    // h_t.addEventListener("click", evt => {
    //     // console.log(evt.target)
    //     console.log(h_t)
    //     console.log(h_t.value)
    //     document.getElementById("round2_0_home_li").innerHTML = `<input type="radio" name="{{loop.index}}" id="{{loop.index}}_home_team" value="{{home_team}}">${h_t_li.innerText}</input<br>`
    //     // <input type="radio" name="{{loop.index}}" id="{{loop.index}}_home_team" value="{{home_team}}">{{match.home_team.name}}</input<br>

    //     // var team = document.getElementById("1_home_team").innerText
    //     // console.log(team)
    // })
    // document.getElementById()

})
function checkIfComplete() {

    console.log(document.getElementsByClassName("game_input"))

    let inputs = document.getElementsByClassName("game_input")
    let input_labels = []
    let count_selected = 0
    for (const input of inputs) {
        if (input.labels == null) {
            console.log("DEF not complete")
            return
        } 
        if (input.checked) {
            count_selected++
        }
        input_labels.push({team_name: input.labels[0].innerText,
                        checked: input.checked,
                        round: input.getAttribute("data_round"),
                        match_id: input.getAttribute("data_match_id")})
    }
    data = {
        input_labels: input_labels
    }
    // console.log(input_labels)

    // let winners = {

        // }
    // for (const game_input of inputs) {
    //     if (game_input.getAttribute("type") === "hidden") {
    //         console.log("SOME EMPTY")
    //         return
    //     }
    //     if (game_input.checked) {
    //         count_selected++
    //         let key = `${game_input.getAttribute("data_round")}`
    //         // let match = (((winners).key || {}).game_input.getAttribute("data_match_id") || {})
            
    //         if (key in winners) {
    //             winners[key]({
    //                 id: game_input.getAttribute("id"),
    //                 name: game_input.labels[0].innerText
    //             })
    //         }
    //     } 
    // }
    if (count_selected != 15) {
        console.log("Not complete")
        return
    }
    doRequest(data).then(resp => {
        console.log(resp);
    });
    // let num_teams = 8

    // for


}

async function doRequest(data) {

    let url = 'http://127.0.0.1:5000/create-bracket/';
    // let data = {'name': 'John Doe', 'occupation': 'John Doe'};

    let res = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });

    if (res.ok) {

        // let text = await res.text();
        // return text;
        console.log("Okay")
        // let ret = await res.json();
        // return JSON.parse(ret.data);

    } else {
        return `HTTP error: ${res.status}`;
    }
}


function setEventListeneners(n, round) {
    for (let i = 1; i<n;i++) {
        let h_t_input = document.getElementById(`round${round}_${i}_home_team`)
        // let h_t_li = document.getElementById(`round1_${i}_home_team-li`)
        let h_t_label = document.getElementById(`round${round}_${i}_home_team-label`)
        let a_t_input = document.getElementById(`round${round}_${i}_away_team`)
        // let a_t_li = document.getElementById(`round1_${i}_away_team-li`)
        let a_t_label = document.getElementById(`round${round}_${i}_away_team-label`)
        // console.log(h_t_input)
        if (i%2 == 1) {
            h_t_input.addEventListener("click", evt => {
                setTeam(evt, h_t_label, "home_team")
            })
            a_t_input.addEventListener("click", evt => {
                setTeam(evt, a_t_label, "home_team")
            })
        } else {
            h_t_input.addEventListener("click", evt => {
                setTeam(evt, h_t_label, "away_team")
            })
            a_t_input.addEventListener("click", evt => {
                setTeam(evt, a_t_label, "away_team")
            })
        }
        // console.log(h_t_input.getAttribute("next"))
        // console.log(h_t_input)
    }
}
function setTeam(event, label, team) {
    let next = event.currentTarget.getAttribute("next")
    // console.log(event.currentTarget.getAttribute("next") | 0)
    
    // console.log(`LABEL : ${label.innerText}`)

    // let round = parseInt(event.currentTarget.getAttribute("data_round"), 10) + 1
    // console.log(`round${round}_${index}_${team}`)
    // console.log(`round${round}_${index}_${team}-label`)
    let next_input = document.getElementById(next)
    let next_label = document.getElementById(`${next}-label`)    
    
    next_input.type = "radio"
    next_label.removeAttribute("hidden")
    next_label.innerText = label.innerText
    let checked = next_input.checked
    // console.log(checked)
    // console.log(next_label)
    // console.log(event.currentTarget.labels[0])

    next = next_input.getAttribute("next")
    next_input = document.getElementById(next)
    // console.log(next)
    // console.log(next_input)
    while (!!next_input) {
        // console.log("HERE")
        if (checked) {
            // console.log("here")
            let text = next_label.innerText
            next_label = document.getElementById(`${next}-label`) 
            next_label.innerText = text
            checked = next_input.checked
            next = next_input.getAttribute("next")
            next_input = document.getElementById(next)
        }
        else {
            break;
        }
    }
}