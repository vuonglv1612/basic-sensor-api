const apiUrl = "http://localhost:8000"

const draw = (temperature, humidity) => {
    const colorSelector = (temp) => {
        if(!temp) return temp
        if(temp <= 25) return "green";
        if(temp <= 40) return "orange";
        return "red"
    }
    const data = [
        {
            type: "indicator",
            value: temperature,
            gauge: {axis: {visible: true, range: [0, 100]}, bar: {color: colorSelector(temperature)}},
            domain: {row: 0, column: 0}
        },
        {
            type: "indicator",
            value: humidity,
            gauge: {axis: {visible: true, range: [0, 100]}, bar: {color: "darkblue"}},
            domain: {row: 0, column: 1}
        },
    ];

    const layout = {
        width: 600,
        height: 400,
        margin: {t: 25, b: 25, l: 25, r: 25},
        grid: {rows: 1, columns: 2, pattern: "independent"},
        template: {
            data: {
                indicator: [
                    {
                        title: {text: "Nhiệt độ"},
                        mode: "number+gauge",
                    },
                    {
                        title: {text: "Độ ẩm"},
                        mode: "number+gauge",
                    }
                ]
            }
        }
    };
    Plotly.newPlot('metric', data, layout);
}

const updateTime = (newTime) => {
    let timestampSpan = document.getElementById("timestamp");
    // Update its text content
    timestampSpan.textContent = newTime;
}

const callAPI = (sensor, callback) => {
    const url = `${apiUrl}/api/metrics?sensor=${sensor}`
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => response.json())
        .then(data => {
            callback(data)
        })
        .catch(error => {
            console.error(error);
        });
}

const main = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const sensor = urlParams.get('sensor');
    callAPI(sensor, (data) => {
        draw(data.temperature_c, data.humidity)
        updateTime(data.timestamp)
    })
}

main()
// 2 giay update data 1 lan
setInterval(() => {
    main()
}, 2000)
