var data_set = {};
var interval = 1;
var range = 24 * 60 * 60 * 1000;
var n = 0; // plot id number

document.addEventListener('DOMContentLoaded', () => {
    setInterval(update, interval*1000);
    });

function update() {

    // Initialize new request
    const request = new XMLHttpRequest();
    request.open('POST', '/update');

    // Callback function for when request completes
    request.onload = () => {

        // Extract JSON data from request
        let res = JSON.parse(request.responseText);
        let data = res["data"]
        
        console.log(data)

        if (res["success"] === "False") {
            console.log("response was unsccessful")
        }

        const date_time = new Date(data["date_time"])
        delete data.date_time;
        document.querySelector('#date_time').innerHTML = date_time;

        const status = data["Status"];
        delete data.Status;
        document.querySelector('#status').innerHTML = "";
        for (k in status) {
            const content = "<li>" + k + ": " + status[k] + "</li>"
            document.querySelector('#status').innerHTML += content;
        }

        document.querySelector('#data').innerHTML = "";
        for (k in data) {
            const content = "<li>" + k + ": " + data[k] + "</li>";
            document.querySelector('#data').innerHTML += content;
        }

        if (Object.getOwnPropertyNames(data_set).length === 0) {
            
            console.log("the first batch of data arrived")
            data_set["date_time"] = [date_time];
            for (k in data) {
                data_set[k] = [data[k]];
            }
            for (k in status) {
                data_set[k] = [status[k]];
            }

            var x = document.querySelector("#params");
            var y = document.createElement("OPTGROUP");
            x.appendChild(y);
            y.setAttribute("label", "data");
            for (k in data) {
                var z = document.createElement("OPTION");
                z.setAttribute("value", k);
                z.innerHTML = k;
                y.appendChild(z);
            }
            y = document.createElement("OPTGROUP");
            x.appendChild(y);
            y.setAttribute("label", "status");
            for (k in status) {
                var z = document.createElement("OPTION");
                z.setAttribute("value", k);
                z.innerHTML = k;
                y.appendChild(z);
            }
        
        } else {

            console.log("data arrived")
            if (date_time > data_set["date_time"][data_set["date_time"].length - 1]) {
                data_set["date_time"].push(date_time);
                for (k in data) {
                    data_set[k].push(data[k]);
                }
                for (k in status) {
                    data_set[k].push(status[k]);
                }
            }
        }

        while ((data_set["date_time"][data_set["date_time"].length - 1] - data_set["date_time"][1]) >= range) {
            for (k in data_set) {
                data_set[k].shift();
            }
        }

        document.querySelectorAll(".plots").forEach( (plot) => {
            const update = {
                x: data_set["date_time"]
            };
            Plotly.relayout(plot, update)
        });

    }

    // Send requests
    request.send();   
    return false;
}

function plot() {
    let container = document.querySelector("#plots");
    let div = document.createElement("DIV");
    container.insertBefore(div, container.firstChild);
    div.setAttribute("class", "plots");
    n++;
    plot_id = "plot_" + n
    div.setAttribute("id", plot_id);

    const e = document.querySelector("#params");
    const param = e.options[e.selectedIndex].value

    const data = [{
        x: data_set["date_time"],
        y: data_set[param],
        type: 'scatter'}];

    const layout = {
        title: param, 
    };

    Plotly.newPlot(plot_id, data, layout);

    let del = document.createElement("BUTTON");
    div.appendChild(del);
    del.setAttribute("class", "delete");
    del.setAttribute("float", "left");
    del.innerHTML = "delete"
    del.onclick = function() {
        this.parentNode.parentNode.removeChild(this.parentNode);
    }

}








