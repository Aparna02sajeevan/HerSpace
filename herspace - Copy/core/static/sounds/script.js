const breathingText = document.getElementById("breathing-text");
const cycle = ["Breathe In", "Hold", "Breathe Out", "Hold"];
let index = 0;

function updateBreathing() {
    breathingText.textContent = cycle[index];
    index = (index + 1) % cycle.length;
}

setInterval(updateBreathing, 4000);
