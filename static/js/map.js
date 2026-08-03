console.log("mqtt connecting...");
const wsURL = JSON.parse(document.getElementById('websocket-url').textContent);
const client = mqtt.connect(wsURL, {
    keepalive: 60,
    protocolId: "MQTT",
    protocolVersion: 4,
    clean: true,
    reconnectPeriod: 5000,
    connectTimeout: 15 * 1000,
    reconnectOnConnackError: true,
});

const mapElement = document.querySelector('#map');
const logElement = document.querySelector('#log');

function addToLog(msg) {
    if (!msg.display) return;
    var text = msg.display;

    var element = document.createElement("li");
    // HACK: Yes, this is a trivial XSS if you have control/MITM of the websocket
    element.innerHTML = text;
    logElement.prepend(element);

    while (logElement.childElementCount > 20) {
        logElement.removeChild(logElement.lastChild);
    }
}

function updateElementState(msg) {
    if (!msg.target || !msg.type || !msg.state) return;
    var targetElements = mapElement.querySelectorAll('.' + msg.target + '.' + msg.type);
    for (var el of targetElements) {
        if (msg.type === "heating") {
            el.innerHTML = msg.state !== "off" ? msg.state + "°" : "";
        } else if (msg.type == "temperature") {
            el.innerHTML = msg.state + "°";
        } else {
            el.className.baseVal = [msg.target, msg.type, msg.state].join(' ');
        }
    }
}


client.on("connect", () => {
    console.log("mqtt connected");

    [
        "doorman/+/user",
        "tool/+/user",
        "tool/+/status", // for when tool controllers are powered down
        "environment/+/heating",
        "environment/g1/elsys/temperature",
        "sensor/g11/temperature/28c893a704000068",
        "sensor/g2/temperature/28c9b9a70400001a",
        "sensor/g8/temperature/282c7da7040000e5",
        "sensor/g14/temperature/28ff1097c4170523",
    ].forEach(key => {
        console.log(`mqtt subscribe: ${key}`);
        client.subscribe(key);
    });


    // There will initially be a spam of x not in use / empty from retained topics,
    // so clear the log after that
    setTimeout(() => {
        while (logElement.childElementCount > 0) {
            logElement.removeChild(logElement.lastChild);
        }
        addToLog({display: "welcome"});
    }, 500);
});

client.on("message", (topic, message, packet) => {
    var value = message.toString();
    var msg = undefined;
    if (topic.startsWith("doorman/") && topic.endsWith("/user")) {
        if (value.length === 0) // door closing again, ignore
            return;

        var room = topic.split("/")[1];
        if (value == "anonymous" || ["g1", "g2", "g8", "g11", "g14"].indexOf(room) === -1)
            return;

        msg = {
            display: `<span class=username>${value}</span> entered <span class=room>${room}</span>`,
            type: "room",
            target: room,
            state: "active",
        };
        setTimeout(() => {
            updateElementState({
                display: "",
                type: "room",
                target: room,
                state: "inactive",
            });
        }, 5000);
    } else if (topic.startsWith("tool/") && (topic.endsWith("/user") || topic.endsWith("/status"))) {
        var tool = topic.split("/")[1];
        if (value.length === 0 || (topic.endsWith("/status") && value === "offline")) {
            msg = {
                display: `<span class=tool>${tool}</span> no longer in use`,
                type: "tool",
                target: tool,
                state: "inactive",
            };
        } else if (topic.endsWith("/user") && value !== "anonymous") {
            msg = {
                display: `<span class=username>${value}</span> is now using <span class=tool>${tool}</span>`,
                type: "tool",
                target: tool,
                state: "active",
            };
        }
    } else if (topic.startsWith("environment/") && topic.endsWith("/heating")) {
        var room = topic.split("/")[1];
        msg = {
            display: `<span class=room>${room}</span> heating set to <span class=temp>${value}</span>`,
            typ: "heating",
            target: room,
            state: value,
        };
    } else if (topic.includes("temperature")) {
        var room = topic.split("/")[1];

        msg = {
            display: "",
            type: "temperature",
            target: room,
            state: value,
        };
    }
    if (msg) {
        addToLog(msg);
        updateElementState(msg);
    }
});

client.on("error", (err) => {
    addToLog({display: "mqtt connection error: " + err});
    client.end();
})

client.on("reconnect", () => {
    console.log("mqtt reconnecting...");
});
