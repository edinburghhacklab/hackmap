// mqtt stuff
console.log("mqtt connecting...");
const wsURL = JSON.parse(document.getElementById('websocket-url').textContent);
const client = mqtt.connect(wsURL, {
    keepalive: 60,
    protocolId: "MQTT",
    protocolVersion: 4,
    clean: true,
    reconnectPeriod: 5000,
    connectTimeout: 30 * 1000,
});

client.on("connect", () => {
    console.log("mqtt connected");

    var topics = new Set();

    $(`[data-printer]`).each(function() {
        var printer = $(this).data("printer");
        topics.add(`printers/${printer}/state`);
        topics.add(`printers/${printer}/file`);
        topics.add(`printers/${printer}/percent_done`);
        topics.add(`printers/${printer}/time_remaining_mins`);
    });

    topics.forEach((value, key, set) => {
        console.log(`mqtt subscribe: ${key}`);
        client.subscribe(key);
    });
});

client.on("message", (topic, message, packet) => {
    var value = message.toString();
    let printer = topic.split("/")[1];
    let typ = topic.split("/")[2];
    let printerSection = $(`section[data-printer=${printer}]`);
    if (typ === "state" && value === "Printing") {
        printerSection.addClass(`active`);
        printerSection.removeClass(`preparing`);
    } else if (typ === "state" && value == "Preprint") {
        printerSection.addClass(`active`);
        printerSection.addClass(`preparing`);
        $(`[data-printer=${printer}] .percent`).text(`Preparing...`);
        $(`[data-printer=${printer}] .time`).text(``);
        $(`[data-printer=${printer}] .file`).text(``);
        $(`[data-printer=${printer}] progress`).val(0);
    } else if (typ === "state") {
        printerSection.removeClass(`active`);
        printerSection.removeClass(`preparing`);
        $(`[data-printer=${printer}] .percent`).text(``);
        $(`[data-printer=${printer}] .time`).text(``);
        $(`[data-printer=${printer}] progress`).val(0);
        return;
    }

    if (typ === "percent_done" && !printerSection.hasClass('preparing')) {
        $(`[data-printer=${printer}] .percent`).text(`${value}% complete -`);
        $(`[data-printer=${printer}] progress`).val(value);
    } else if (typ === "time_remaining_mins" && !printerSection.hasClass('preparing')) {
        $(`[data-printer=${printer}] .time`).text(`${value} minutes remaining`);
    } else if (typ === "file") {
        $(`[data-printer=${printer}] .file`).text(`Printing ${value} - `);
    }
});

client.on("error", (err) => {
    console.log("mqtt connection error: ", err);
    client.end();
})

client.on("reconnect", () => {
    console.log("mqtt reconnecting...");
});


let lightsOffTask = undefined;
function lights_on() {
    $.ajax({
        url: '/printers/lights/on'
    });

    // Turn off after 20 seconds
    if (lightsOffTask)
        clearTimeout(lightsOffTask)
    lightsOffTask = setTimeout(lights_off, 20 * 1000);
}

function lights_off() {
    $.ajax({
        url: '/printers/lights/off'
    });
}

document.onkeydown = function (e) {
    if (e.key == "a") {
        lights_on()
    }
};
