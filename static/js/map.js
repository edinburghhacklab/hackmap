document.addEventListener("DOMContentLoaded", function() {
    const wsURL = JSON.parse(document.getElementById('websocket-url').textContent);
    const chatSocket = new WebSocket(wsURL);
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
            console.log(el);
            if (msg.type === "heating") {
                el.innerHTML = msg.state !== "off" ? msg.state + "°C" : "";
            } else {
                el.className.baseVal = [msg.target, msg.type, msg.state].join(' ');
            }
        }
    }

    chatSocket.onmessage = function(e) {
        var msg = JSON.parse(e.data);
        console.log(msg);
        addToLog(msg);
        updateElementState(msg);
    };

    chatSocket.onclose = function(e) {
        addToLog({display: "socket closed unexpectedly. please reload."});
        // TODO: Show error
    };
});
