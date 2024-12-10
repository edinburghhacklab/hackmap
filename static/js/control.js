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
    client.subscribe("sensor/g1/temperature");
    for (var el of document.querySelectorAll('.subscribe-inactive')) {
        let topic = el.dataset.subscribeTopic
        if (topic) {
            console.log(`mqtt subscribe: ${topic}`);
            client.subscribe(topic);
        }
    }
});

client.on("message", (topic, message, packet) => {
    var value = message.toString();
    var inactives = $(`[data-subscribe-topic="${topic}"][data-subscribe-value!="${value}"]`);
    var actives = $(`[data-subscribe-topic="${topic}"][data-subscribe-value="${value}"]`);
    inactives.removeClass("subscribe-active");
    inactives.addClass("subscribe-inactive");
    actives.removeClass("subscribe-inactive");
    actives.addClass("subscribe-active");
    /* TODO make this configurable */
    if (topic == "sensor/g1/temperature") {
        $(`[class="tile-group-title"][data-id="5"]`).text(`Heating (G1 is currently ${value}°C)`);
    }
});

client.on("error", (err) => {
    console.log("mqtt connection error: ", err);
    client.end();
})

client.on("reconnect", () => {
    console.log("mqtt reconnecting...");
});

