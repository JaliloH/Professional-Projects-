let map, infoWindow, marker;
let search_value = null;
var latitude, longitude = null;

async function initMap() {

  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const { places } = await google.maps.importLibrary("places");

  // code below puled from google maps places api to pull users current location //
  infoWindow = new google.maps.InfoWindow();

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };
        map.setCenter(pos);
        marker = new AdvancedMarkerElement({
          map: map,
          position: pos,
          title: "your location",
        });
      },
    );
  } else {
    console.log("Error for user geolocation");
  }
  // ----------------------------------------- // 

  map = new Map(document.getElementById("map"), {
    zoom: 16,
    mapId: "MainMap",
  });

  var search_bar = document.getElementById("search-bar-input");
  map.addListener('click', function(e) {
    var geocoder = new google.maps.Geocoder();
    latitude = e.latLng.lat();
    longitude = e.latLng.lng();
    
    var latlng = new google.maps.LatLng(latitude, longitude);

    var location_type = null

    geocoder.geocode({'latLng': latlng}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[0]) {
          search_bar.value = results[0].formatted_address;
          location_type = results[0].types[0];
        } else {
          console.log('No results found');
        }
      } else {
        console.log('Geocoder failed due to: ' + status);
      }
    });

  });



  const center = { lat: 44.9737, lng: -93.2311 };

  const defaultBounds = {
    north: center.lat + 0.1,
    south: center.lat - 0.1,
    east: center.lng + 0.1,
    west: center.lng - 0.1,
  };

  const input = document.getElementById("search-bar-input");
  const options = {
    bounds: defaultBounds,
    componentRestrictions: { country: "us" },
    fields: ["address_components", "geometry", "icon", "name"],
    strictBounds: false,
  };

  const autocomplete = new google.maps.places.Autocomplete(input, options);

}

$('#search-submit-btn').click(async function() {
  var search_bar = document.getElementById("search-bar-input");
  if(latitude == null || longitude == null) {
    search_value = search_bar.value;
  }
  await $.ajax({
    url: "/search",
    type: 'GET',
    data: {
        lat: latitude,
        long: longitude,
        search_value: search_value
    },
    success: function(data) {
      document.write(data);
      display();
    },
    error: function(xhr, status, error) {
      console.error(error);
    }
  });
});

$(() => {
    initMap();
    display()
}); 