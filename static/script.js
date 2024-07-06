var form = document.getElementById('busBookingForm');
var content_div = document.getElementById('out-content')

form.addEventListener('submit', (event) => {
    event.preventDefault();
    var bus_from = document.getElementById('bus_from').value;
    var bus_to = document.getElementById('bus_to').value;
    var ac_type = document.getElementById('ac_type').value;
    var bus_type = document.getElementById('bus_type').value;
    var cost = document.getElementById('cost').value;
    content_div.innerHTML = `<div class="loader-container">
            <div class="loader-1"></div>
            <div class="loader-2"></div>
            <div class="loader-3"></div>
        </div>`;
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'bus_from' : bus_from, 
            'bus_to' : bus_to,
            'ac_type' : ac_type,
            'bus_type' : bus_type,
            'cost' : cost
         })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data);
        var content = '';
        if (data.bus_list && data.bus_list.length > 0) {
            for(i = 0 ; i < data.bus_list.length; i++){
                content += `<div class="output-container">
                    <div class="body-container">
                        <h2>${data.bus_list[i]['busName']}</h2>
                        <div class="output-details">
                            <p><b>Starting Point : </b>${data.bus_list[i]['busFrom']} </p>
                            <p><b>Destination : </b>${data.bus_list[i]['busTo']}</p>
                            <p><b>Time : </b>${data.bus_list[i]['startTime']}</p>
                            <p><b>Cost : </b>${data.bus_list[i]['cost']}</p>
                        </div>
                    </div>
                    <div class="button-container">
                        <button>Book Now</button>
                    </div>
                </div>`;
            }
        }else{
            content = `<div class='no-data'>No Data Found<div>`;
        }
        content_div.innerHTML = content;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});