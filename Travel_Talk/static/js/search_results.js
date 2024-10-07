

async function initMap() {

  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");
  const { places } = await google.maps.importLibrary("places");

  var search_bar = document.getElementById("search-bar-input");

  const input = document.getElementById("search-bar-input");
  const options = {
    bounds: defaultBounds,
    componentRestrictions: { country: "us" },
    fields: ["address_components", "geometry", "icon", "name"],
    strictBounds: false,
  };

  const autocomplete = new google.maps.places.Autocomplete(input, options);

}

function ClickLocationLink(e) {
    console.log(e)
    var clicked_location_name;
    var clicked_location_photo;
    var clicked_location_id;
    var clicked_location_type;

    for(var name in searchResults) {
        if(name == e.target.childNodes[0].data.trim())  {
            clicked_location_name = name;
            clicked_location_photo = searchResults[name][0];
            clicked_location_id = searchResults[name][2];
            clicked_location_type = searchResults[name][3];
        }

    }

    $.ajax({
        url: "/get_reviews",
        type: 'GET',
        data: {
            location_name: clicked_location_name,
            location_photo: clicked_location_photo,
            location_id: clicked_location_id,
            location_type: clicked_location_type
        },
        success: function(data) {
            console.log(data)
            $("#search_results_grid").html(data);
            display()
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
      });
}

$(() => {
    initMap();
}); 