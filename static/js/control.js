// regular old buttons
$('.ajax').click(function(e) {
    $.ajax({
        url: '/trigger/' + $(this).data('id')
    });
    e.preventDefault();
});

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

    $(`[data-subscribe-topic]`).each(function() {
        topics.add($(this).data("subscribe-topic"));
    });

    $.map(mqtt_group_topics, function(value, key) {
        topics.add(key);
    });

    topics.forEach((value, key, set) => {
        console.log(`mqtt subscribe: ${key}`);
        client.subscribe(key);
    });
});

var mqtt_group_topics = {};

function mqtt_update_group_names(topic) {
    $(`[class="tile-group-title"][data-name]`).each(function() {
        var name = $(this).data("name");

        if (topic == "") {
            if (!name.includes("${"))
                return;
        } else {
            if (!name.includes("${" + topic + "}"))
                return;
        }

        $.map(mqtt_group_topics, function(value, key) {
            name = name.replace("${" + key + "}", value);
        });

        $(this).text(name);
    });
};

(function() {
    $(`[class="tile-group-title"][data-name]`).each(function() {
        var name = $(this).data("name");

        while (name.includes("${")) {
            var topic = name.substring(name.indexOf("${") + 2).split("}")[0];
            name = name.substring(name.indexOf("${") + 2 + topic.length + 1);

            mqtt_group_topics[topic] = "?";
        }
    });

    mqtt_update_group_names("");
})();

client.on("message", (topic, message, packet) => {
    var value = message.toString();
    var inactives = $(`[data-subscribe-topic="${topic}"][data-subscribe-value!="${value}"]`);
    var actives = $(`[data-subscribe-topic="${topic}"][data-subscribe-value="${value}"]`);
    inactives.removeClass("subscribe-active");
    inactives.addClass("subscribe-inactive");
    actives.removeClass("subscribe-inactive");
    actives.addClass("subscribe-active");

    if (topic in mqtt_group_topics) {
        mqtt_group_topics[topic] = value;
        mqtt_update_group_names(topic);
    }
});

client.on("error", (err) => {
    console.log("mqtt connection error: ", err);
    client.end();
})

client.on("reconnect", () => {
    console.log("mqtt reconnecting...");
});

