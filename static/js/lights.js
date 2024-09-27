document.addEventListener("DOMContentLoaded", function() {
    function lightPressed(e) {
        e.preventDefault();
        if (this.classList.contains('active')) {
            this.classList.remove('active');
        } else {
            this.classList.add('active');
        }
        updateSelectionBox();
    }

    document.querySelectorAll('.light').forEach(el => el.addEventListener('click', lightPressed))

    function updateSelectionBox() {
        var numSelected = document.querySelectorAll('.light.active').length;
        if (numSelected == 0) {
            document.querySelector('#selection-status').innerText = `No lights selected.`;
            document.querySelector('#deselect').classList.add('hidden');
            document.querySelector('#presets').classList.remove('hidden');
            document.querySelector('#actions').classList.add('hidden');
        } else if (numSelected == 1){
            document.querySelector('#selection-status').innerText = `${numSelected} light selected.`;
            document.querySelector('#deselect').classList.remove('hidden');
            document.querySelector('#presets').classList.add('hidden');
            document.querySelector('#actions').classList.remove('hidden');
        } else {
            document.querySelector('#selection-status').innerText = `${numSelected} lights selected.`;
            document.querySelector('#deselect').classList.remove('hidden');
            document.querySelector('#presets').classList.add('hidden');
            document.querySelector('#actions').classList.remove('hidden');
        }
    }

    function deselect() {
        document.querySelectorAll('.light.active').forEach(el => el.classList.remove('active'));
        updateSelectionBox();
    }
    document.querySelector('#deselect').addEventListener('click', deselect);

    function selectPreset() {
        var preset = this.dataset.preset;
        var toSelect = [];
        switch(preset) {
        case "workbench":
            toSelect = [
                document.querySelector('.light[data-id="2"]'),
                document.querySelector('.light[data-id="5"]'),
                document.querySelector('.light[data-id="8"]'),
                document.querySelector('.light[data-id="1"]'),
                document.querySelector('.light[data-id="4"]'),
                document.querySelector('.light[data-id="7"]'),
                document.querySelector('.light[data-id="0"]'),
                document.querySelector('.light[data-id="3"]'),
                document.querySelector('.light[data-id="6"]'),
            ];
            break;
        case "social":
            toSelect = [
                document.querySelector('.light[data-id="9"]'),
                document.querySelector('.light[data-id="14"]'),
                document.querySelector('.light[data-id="17"]'),
                document.querySelector('.light[data-id="10"]'),
                document.querySelector('.light[data-id="13"]'),
                document.querySelector('.light[data-id="16"]'),
                document.querySelector('.light[data-id="11"]'),
                document.querySelector('.light[data-id="12"]'),
                document.querySelector('.light[data-id="15"]'),
            ];
            break;
        case "all":
        default:
            toSelect = document.querySelectorAll('.light');
        }
        for (var light of toSelect) {
            light.classList.add('active');
        }
        updateSelectionBox();
    }
    document.querySelectorAll('input[data-preset]')
        .forEach(el => el.addEventListener('click', selectPreset));

    function setLights(e) {
        e.preventDefault();
        var val = this.dataset.brightness;
        var ids = Array.from(document.querySelectorAll('.light.active'))
            .map(el => el.dataset.id);
        console.log(ids, val);
        fetch(`/lights/${ids.join(",")}/${Math.floor(val)}`, {method: "POST"});
    }

     function sliderUpdateDisplay(e) {
         e.preventDefault();
         var touchX = e.changedTouches ? e.changedTouches[0].clientX : e.clientX;
         var offsetX = touchX - this.getBoundingClientRect().left;
         var val = offsetX / this.offsetWidth;
         if (val < 0.0 || val > 1.0) return;
         this.dataset.brightness = val * 255;
         this.querySelector('div').style = 'width: ' + (val * 100) + '%';
     }
     document.querySelector('.ajax-slider').addEventListener('mousemove', sliderUpdateDisplay);
     document.querySelector('.ajax-slider').addEventListener('mouseleave', function(e) {
         this.querySelector('div').style = "width: 0;";
     });
     document.querySelector('.ajax-slider').addEventListener('touchmove', sliderUpdateDisplay);
     document.querySelector('.ajax-slider').addEventListener('touchstart', function(e) { e.preventDefault(); });

    document.querySelectorAll('[data-brightness]')
        .forEach(el => el.addEventListener('click', setLights));
    document.querySelectorAll('.ajax-slider')
        .forEach(el => el.addEventListener('touchend', setLights));
});
