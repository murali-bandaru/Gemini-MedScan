function analyzeSymptoms() {
    const symptoms = document.getElementById("symptoms").value;

    fetch("http://localhost:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms }),
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById("output").innerText = data.analysis || data.error;
        });
}

function uploadReport() {
    const file = document.getElementById("fileInput").files[0];
    let formData = new FormData();
    formData.append("file", file);

    fetch("http://localhost:5000/scan-report", {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {
            document.getElementById("output").innerText = data.analysis || data.error;
        });
}
