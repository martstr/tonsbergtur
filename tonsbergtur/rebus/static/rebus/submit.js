function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function geoProblemSubmit(problem_id) {

    const responseLbl = document.querySelector('#lblgeo'.concat(problem_id));
    const csrftoken = getCookie('csrftoken');

    function success(position) {
        const data = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            problem_id: problem_id
        };

        fetch(window.location.origin.concat('/check-location/'), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            mode: 'same-origin',
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                if (data.status) {
                    responseLbl.textContent = 'Riktig!';
                } else {
                    responseLbl.textContent = 'Nehei, det er dere ikke.'
                }

            })
            .catch((error) => {
                console.error('Error:', error);
                responseLbl.textContent = error
            });

    }

    function error() {
        responseLbl.textContent = 'Unable to retrieve your location';
    }

    if (!navigator.geolocation) {
        responseLbl.textContent = 'Geolocation is not supported by your browser';
    } else {
        responseLbl.textContent = 'Locating…';
        navigator.geolocation.getCurrentPosition(success, error);
    }

}

function textProblemSubmit(problem_id) {
    const responseLbl = document.querySelector('#lbltext'.concat(problem_id));
    const csrftoken = getCookie('csrftoken');

    const data = {
        answer: document.getElementById('text'.concat(problem_id)).value,
        problem_id: problem_id
    };

    fetch(window.location.origin.concat('/check-text/'), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            if (data.status) {
                responseLbl.textContent = 'Riktig!';
            } else {
                responseLbl.textContent = 'Nope.'
            }

        })
        .catch((error) => {
            console.error('Error:', error);
            responseLbl.textContent = error
        });
}

function numberProblemSubmit(problem_id) {
    const responseLbl = document.querySelector('#lblnumber'.concat(problem_id));
    const csrftoken = getCookie('csrftoken');

    const data = {
        answer: document.getElementById('number'.concat(problem_id)).value,
        problem_id: problem_id
    };

    fetch(window.location.origin.concat('/check-number/'), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: JSON.stringify(data),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:', data);
            if (data.status) {
                responseLbl.textContent = 'Riktig!';
            } else {
                responseLbl.textContent = 'Nope.'
            }

        })
        .catch((error) => {
            console.error('Error:', error);
            responseLbl.textContent = error
        });
}

function openProblemSubmit(problem_id) {
    console.log("Starter");

    const responseLbl = document.querySelector('#lblopen'.concat(problem_id));
    const csrftoken = getCookie('csrftoken');

    const data = {
        answer: document.getElementById('open'.concat(problem_id)).value,
        problem_id: problem_id,
    };

    fetch(window.location.origin.concat('/check-open/'), {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        mode: 'same-origin',
        body: JSON.stringify(data),
    })
    .then((response) => response.json())
    .then((data)     => {
        console.log('Success:', data);
        if (data.status) {
            responseLbl.textContent = 'OK!';
        } else {
            responseLbl.textContent = 'Nope.'
        }

    })
    .catch((error) => {
        console.error('Error:', error);
        responseLbl.textContent = error
    });
}