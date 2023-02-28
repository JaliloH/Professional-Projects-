var is_hidden = false;
var columnValues = [];
var geocoder;            
var goog_map;

window.onload = function() {
    get_cells();
    codeAddress();
};



function show_image(inp_src, width, height, alt) {
    let curs_src = inp_src.replace(".jpg", ".png");
    $('body').css('cursor', `url(${curs_src}),auto`);

    let img_container = document.getElementById('imgContainer');
    img_container.replaceChildren();

    var img = document.createElement("img");
    img.src = inp_src;
    img.width = width;
    img.height = height;
    img.alt = alt;

    imgContainer.appendChild(img);

    
    
}

function toggle() {
    let img_container = document.getElementById('imgContainer');
    let button = document.getElementById('imgButton');
    let prev_img = getImageFromContainer(img_container);

    if(is_hidden) {
        prev_img.hidden = false;
        is_hidden = false;
        button.innerHTML = "Go Away";
    }
    else {
        prev_img.hidden = true;
        is_hidden = true;
        button.innerHTML = "Come Back!";
    }
    
}

function get_cells() {

    let table = document.getElementById('sch_table');

    var cells = table.querySelectorAll("td:nth-child(4)");

    for (var i = 0; i < cells.length; i++) {
        columnValues.push(cells[i].textContent);
    }

}

function initMap() {
    var myLatLng = {lat: 44.977276, lng: -93.232266};
    geocoder = new google.maps.Geocoder();
    goog_map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    zoom: 14
    });
}

function codeAddress() {

    
    for(i = 0; i < columnValues.length; i++) {
        
        var address = columnValues[i];

        const infoWindow = new google.maps.InfoWindow({
            content: address,
            disableAutoPan: true,
        });

        geocoder.geocode( { 'address': address}, function(results, status) {
        if (status == 'OK') {
            var marker = new google.maps.Marker({
            map: goog_map,
            position: results[0].geometry.location
            
        });

        marker.addListener("click", () => {
            infoWindow.open(map, marker);
    
        });

        } else {
                alert('Geocode was not successful for the following reason: ' + status);
            }
        });
    }
    

}

function divContainsImage(divElement) {
    let imageElements = divElement.getElementsByTagName("img");
    return imageElements.length;
}

function getImageFromContainer(containerElement) {
    var imageElement = containerElement.querySelector("img");
    return imageElement;
}
