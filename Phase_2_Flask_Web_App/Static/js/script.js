const button = document.getElementById("recordButton");

let mediaRecorder;
let audioChunks = [];
let stream;
let timer;
let seconds = 3;

button.addEventListener("click", async function () {

    button.disabled = true;

    document.getElementById("resultCard").style.display = "none";
    document.getElementById("loadingCard").style.display = "none";

    stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);

    audioChunks = [];

    mediaRecorder.ondataavailable = function (event) {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async function () {

        clearInterval(timer);

        button.innerHTML = "Analyzing...";

        document.getElementById("loadingCard").style.display = "block";

        const blob = new Blob(audioChunks, {
            type: "audio/webm"
        });

        const formData = new FormData();

        formData.append("audio", blob, "recording.webm");

        try {

            const response = await fetch("/upload", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            document.getElementById("loadingCard").style.display = "none";

            if (data.success) {

                const prediction = document.getElementById("prediction");
                const confidence = document.getElementById("confidence");
                const description = document.getElementById("description");

                prediction.innerHTML = data.prediction;
                confidence.innerHTML = data.confidence + "%";

                if (data.prediction === "Healthy") {

                    prediction.style.color = "#22c55e";

                    description.innerHTML =
                        "No Parkinson's indicators were detected in this voice sample.";

                } else {

                    prediction.style.color = "#ef4444";

                    description.innerHTML =
                        "Voice characteristics associated with Parkinson's were detected. Please consult a qualified healthcare professional for further evaluation.";

                }

                document.getElementById("resultCard").style.display = "block";

            } else {

                alert(data.message);

            }

        } catch (err) {

            console.error(err);

            alert("Something went wrong.");

        }

        stream.getTracks().forEach(track => track.stop());

        button.disabled = false;
        button.innerHTML = "🎤 Start Voice Analysis";
        seconds = 3;

    };

    mediaRecorder.start();

    timer = setInterval(() => {

        button.innerHTML = `🎙 Recording... ${seconds}s`;

        seconds--;

        if (seconds < 0) {

            mediaRecorder.stop();

        }

    }, 1000);

});


document.getElementById("againButton").addEventListener("click", function () {

    document.getElementById("resultCard").style.display = "none";

    window.scrollTo({

        top: 0,

        behavior: "smooth"

    });

});