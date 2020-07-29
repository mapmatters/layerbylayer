mapboxgl.accessToken = 'pk.eyJ1IjoibWFwbWF0dGVycyIsImEiOiJjamc0Y2p1OWwxNWN6MnBzMTJ6czRrZnY1In0.Beyp8DKNzxakGHxuSIgNfA';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapmatters/ckbxxbw9w2is41jmsd8uyix4l',
    center: [127.0755, 37.5185],
    zoom: 10,
    scrollZoom: true
});

map.addControl(
    new mapboxgl.GeolocateControl({
        positionOptions: {
            enableHighAccuracy: true
        },
        fitBoundsOptions: {
            maxZoom: 11
        },
        trackUserLocation: false,
        showAccuracyCircle: false
    })
);


// Holds visible airport features for filtering
var mycamping = [];
 
// Create a popup, but don't add it to the map yet.
var popup = new mapboxgl.Popup({
closeButton: false
});

var filterEl = document.getElementById('feature-filter');

function normalize(string) {
    return string.trim().toLowerCase();
    }

function getUniqueFeatures(array, comparatorProperty) {
    var existingFeatureKeys = {};
    // Because features come from tiled vector data, feature geometries may be split
    // or duplicated across tile boundaries and, as a result, features may appear
    // multiple times in query results.
    var uniqueFeatures = array.filter(function (el) {
        if (existingFeatureKeys[el.properties[comparatorProperty]]) {
            return false;
        } else {
            existingFeatureKeys[el.properties[comparatorProperty]] = true;
            return true;
        }
    });

    return uniqueFeatures;
}

map.on('load', function () {
    map.addSource('campingsites', {
        'type': 'vector',
        'url': 'mapbox://mapmatters.9ilda2dr'
    });
    map.addLayer({
        'id': 'camping',
        'source': 'campingsites',
        'source-layer': 'camp_geo-1m11gy',
        'type': 'symbol',
        'layout': {
            'text-field': ['get', 'name'],
            'text-variable-anchor': ['top', 'bottom', 'left', 'right'],
            'text-radial-offset': 0.5,
            "text-size": [
                "interpolate",
                ["linear"],
                ["zoom"],
                7,
                8,
                22,
                26
            ],
            'text-justify': 'auto',
            'icon-image': 'mountain-15',
            'icon-padding': 0,
            'icon-size': 1.5,
            'icon-allow-overlap': true
        }
    });
    
    var mycamping = map.queryRenderedFeatures({ layers: ['camping'] });

    map.on('click', 'camping', function (e) {
        // Change the cursor style as a UI indicator.
        map.getCanvas().style.cursor = 'pointer';
        popup.remove();
        map.flyTo({
            center: e.features[0].geometry.coordinates
        });
        // Populate the popup and set its coordinates based on the feature.
        var feature = e.features[0];
        popup
            .setLngLat(feature.geometry.coordinates)
            .setHTML(
                '<h3>' + feature.properties.name +
                '  ' +
                '<a style="text-decoration:none;" href=" ' + "https://www.instagram.com/explore/tags/" + feature.properties.hashtag + ' " target="bar"> ' + '<img src="img/instagram.png" alt="hashtag" style="width:24px;height:24px;">' + ' </a>' +
                '  ' +
                '<a style="text-decoration:none;" href=" ' + "https://www.youtube.com/results?search_query=" + feature.properties.hashtag + ' " target="bar">' + '<img src="img/youtube.png" alt="youtube" style="width:24px;height:24px;">' + ' </a>' +
                '</h3>' +
                // '<h4><a href=" ' + "https://www.instagram.com/explore/tags/" + feature.properties.hashtag + ' " target="bar"> #' + feature.properties.hashtag + ' </a></h4>' +
                // '<h4><a href=" ' + "https://www.youtube.com/results?search_query=" + feature.properties.hashtag + ' " target="bar">' + "Search on Youtube" + ' </a></h4>' +
                '<p>' + feature.properties.addr + '<br>' + feature.properties.call_num + '</p>')
            .addTo(map);
    });

    map.on('mouseenter', 'camping', function () {
        map.getCanvas().style.cursor = 'pointer';
    });

    // Change it back to a pointer when it leaves.
    map.on('mouseleave', 'camping', function () {
        map.getCanvas().style.cursor = ''
    });

    filterEl.addEventListener('keyup', function (e) {
        // var value = normalize(e.target.value);

        // Filter visible features that don't match the input value.
        var filtered = mycamping.filter(function (feature) {
            var name = normalize(feature.properties.name);
            // var code = normalize(feature.properties.addr);
            return name.indexOf(value) > -1 ;//|| code.indexOf(value) > -1;
        });

        // Populate the sidebar with filtered results
        // renderListings(filtered);

        // Set the filter to populate features into the layer.
        if (filtered.length) {
            map.setFilter('camping', [
                'match',
                ['get', 'name'],
                filtered.map(function (feature) {
                    return feature.properties.name;
                }),
                true,
                false
            ]);
        }
    });

});