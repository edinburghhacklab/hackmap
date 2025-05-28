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
    if (typ === "state" && value === "Printing") {
        $(`section[data-printer=${printer}]`).addClass(`active`);
    } else if (typ === "state" && value == "Preprint") {
        $(`section[data-printer=${printer}]`).addClass(`active`);
        $(`[data-printer=${printer}] .percent`).text(`Preparing to print...`);
        $(`[data-printer=${printer}] .time`).text(``);
        $(`[data-printer=${printer}] progress`).val(0);
    } else if (typ === "state") {
        $(`section[data-printer=${printer}]`).removeClass(`active`);
        $(`[data-printer=${printer}] .percent`).text(``);
        $(`[data-printer=${printer}] .time`).text(``);
        $(`[data-printer=${printer}] progress`).val(0);
    }

    if (typ === "percent_done") {
        $(`[data-printer=${printer}] .percent`).text(`${value}% complete -`);
        $(`[data-printer=${printer}] progress`).val(value);
    } else if (typ === "time_remaining_mins" && value != "0") {
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
