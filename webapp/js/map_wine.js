
mapboxgl.accessToken =
// 'sk.eyJ1IjoibWFwbWF0dGVycyIsImEiOiJja2MzNDBucDkxcjAzMnNuNDR1ejNrMmJjIn0.d5vZhI6SupVvQ6y-iswd7A';
'pk.eyJ1IjoibWFwbWF0dGVycyIsImEiOiJjamc0Y2p1OWwxNWN6MnBzMTJ6czRrZnY1In0.Beyp8DKNzxakGHxuSIgNfA';

var filterGroup = document.getElementById('filter-group');
var map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapmatters/ckc69smqc12lz1ikirgbbeb90',
  center: [126.994154, 37.5491172],
  zoom: 11,
  scrollZoom: true,
  maxZoom: 15,
  minZoom: 6,
  localIdeographFontFamily: false//"'Noto Sans', 'Noto Sans CJK SC', sans-serif"
});



map.addControl(
  new mapboxgl.GeolocateControl({
    positionOptions: {
      enableHighAccuracy: true
    },
    fitBoundsOptions: {
      maxZoom: 12
    },
    trackUserLocation: true,
    showAccuracyCircle: false
  })
  );
  
map.addControl(new mapboxgl.NavigationControl());

// Create a popup, but don't add it to the map yet.
var popup = new mapboxgl.Popup({
  closeButton: false
});

// var span = document.getElementsByClassName("close")[0];
function closePopup () {
	document.getElementById("popup").innerHTML = "";
};

function imgClick(img) {
  img.style.border = '5px solid pink';
}

map.on('load', function () {
  var layers = map.getStyle().layers;
  // Find the index of the first symbol layer in the map style
  var firstSymbolId;
  
  for (var i = 0; i < layers.length; i++) {
    if (layers[i].type === 'symbol') {
      firstSymbolId = layers[i].id;
      break;
    }
  }
  
  map.addSource('wines', {
    'type': 'vector',
    'url': 'mapbox://mapmatters.bt53lwud'
  });

  const toggleContainer = document.getElementById('filter-group');
  const toggleLayers = [
    ['winebar',['==', ['get', 'type_en'],'winebar'], "bar-11"],
    ['wineshop',['==', ['get', 'type_en'],'wineshop'], "grocery-11"],
  ];

  toggleLayers.forEach(function(item) {
    let symbol = item[2];
    let layerID = item[0];

    if (!map.getLayer(layerID)) {
      map.addLayer({
        'id': layerID,
        'type': 'symbol',
        'source': 'wines',
        'source-layer': 'wine_geo-brimnu',
        'layout': {
          'icon-image': symbol,
          'icon-padding': 0,
          "icon-size": {
            stops: [
              [6, 0.3],
              [11, 1.0],
              [16, 2.7]
            ]
          },
          'icon-allow-overlap': true
        },
        'filter': item[1]
      });

      map.addLayer({
        'id': layerID + '-label',
        'type': 'symbol',
        'source': 'wines',
        'source-layer': 'wine_geo-brimnu',
        'layout': {
          // 'visibility': 'visible',
          'text-field': ['get', 'name'],
          'text-variable-anchor': ['top', 'bottom', 'left', 'right'],
          'text-radial-offset': 0.5,
          'text-font': ['Noto Sans CJK JP Regular'],
          // 'text-color': '#48567A',
          "text-size": [
            "interpolate",
            ["linear"],
            ["zoom"],
            7,
            8,
            22,
            23
          ],
          'text-justify': 'auto'
        },
        "paint": {
          "text-color": "#013522",
          "text-halo-color": "#fff",
          "text-halo-width": 1
        },
        'filter': item[1]
      });

      let toggleLayer = document.createElement('input');

      toggleLayer.type = 'checkbox';
      toggleLayer.id = item[0]
      toggleLayer.checked = true;
      toggleContainer.appendChild(toggleLayer);

      let toggleLabel = document.createElement('label');
      toggleLabel.setAttribute('for', item[0]);
      toggleLabel.textContent = item[0];

      toggleContainer.appendChild(toggleLabel);

      toggleLayer.addEventListener('change', function (e) {
        map.setLayoutProperty(layerID,'visibility',e.target.checked ? 'visible' : 'none');
        map.setLayoutProperty(layerID + '-label','visibility',e.target.checked ? 'visible' : 'none');
      });
    };
    map.on('click', layerID, function (e) {
      var feature = e.features[0];
      var coordinates = feature.geometry.coordinates
      var description = //'<div class="popup">' +
      "<span class='close' onclick=closePopup()>&times;</span>" +
      '<h3>' + feature.properties.name + '</h3>' +
      '<p>' +
        // '<a style="text-decoration:none;" href=" ' + 
        //   " https://www.instagram.com/explore/tags/" + feature.properties.hashtag + ' " target="bar"> ' +
        //   '<img class="middle" src="img/instagram.png" alt="hashtag" style="width:24px;height:24px;">' + ' </a>' +
        // ' #' + feature.properties.hashtag + ' ' + feature.properties.posts + ' posts' + 
          // '<br>' +
          // '<a style="text-decoration:none;" href=" ' +
        // "https://www.youtube.com/results?search_query=" + feature.properties.hashtag + ' " target="bar">' +
        //   '<img src="img/youtube.png" alt="youtube" style="width:24px;height:24px;">' + ' </a>' +
        // '<br>' + 
        feature.properties.address + 
        // '<br>' + feature.properties.call_num + 
        '</p>' + '</div>'
      map.flyTo({ center: coordinates });
      document.getElementById("popup").innerHTML = description;
    });
  });



  // map.on('mousemove', 'camping-icon', function (e) {
  //   if (e.features.length > 0) {
  //     if (hoveredStateId) {
  //       map.setFeatureState({
  //         source: 'campingsites',
  //         id: hoveredStateId
  //       }, {
  //         hover: false
  //       });
  //     }
  //     hoveredStateId = e.features[0].id;
  //     map.setFeatureState({
  //       source: 'campingsites',
  //       id: hoveredStateId
  //     }, {
  //       hover: true
  //     });
  //   }
  // });

  map.on('dragend', function () {
    document.getElementById("popup").innerHTML = "";
  });

  map.on('mouseenter', 'camping', function () {
    map.getCanvas().style.cursor = 'pointer';
  });


});