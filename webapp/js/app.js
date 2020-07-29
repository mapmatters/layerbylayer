// initailize
mapboxgl.accessToken =
// 'sk.eyJ1IjoibWFwbWF0dGVycyIsImEiOiJja2MzNDBucDkxcjAzMnNuNDR1ejNrMmJjIn0.d5vZhI6SupVvQ6y-iswd7A';
'pk.eyJ1IjoibWFwbWF0dGVycyIsImEiOiJjamc0Y2p1OWwxNWN6MnBzMTJ6czRrZnY1In0.Beyp8DKNzxakGHxuSIgNfA';

const filterGroup = document.getElementById('filter-group');
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapmatters/ckc3zy2gs07ob1inoizstc8vx?optimize=true',
  center: [127.6755, 36.2185],
  zoom: 6,
  scrollZoom: true,
  maxZoom: 15,
  minZoom: 6,
  localIdeographFontFamily: false//"'Noto Sans', 'Noto Sans CJK SC', sans-serif"
});

// control area
map.addControl(
  new mapboxgl.GeolocateControl({
    positionOptions: {
      enableHighAccuracy: true
    },
    fitBoundsOptions: {
      maxZoom: 11
    },
    trackUserLocation: true,
    showAccuracyCircle: false
  })
  );
  
map.addControl(new mapboxgl.NavigationControl());

const infoBox = {
  closePopup: function() {
    document.getElementById("popup").innerHTML = "";
  },
  copyFunc: function() {
    let copyText = document.getElementById("camp-name");
    copyText.select();
    document.execCommand("Copy");
  }
};

// define functions
const queryFeatures = {
  normalize: function(string) {
    return string.trim().toLowerCase();
  },
  getUniqueFeatures: function(array, comparatorProperty) {
    var existingFeatureKeys = {};
    // Because features come from tiled vector data, feature geometries may be split
    // or duplicated across tile boundaries and, as a result, features may appear
    // multiple times in query results.
    var uniqueFeatures = array.filter(function (e) {
      if (existingFeatureKeys[e.properties[comparatorProperty]]) {
        return false;
      } else {
        existingFeatureKeys[e.properties[comparatorProperty]] = true;
        return true;
      }
    });
    return uniqueFeatures;
  }
}


camping_result = [];


map.on('load', function () {
  let layers = map.getStyle().layers;
  // Find the index of the first symbol layer in the map style
  let firstSymbolId;

  for (let i = 0; i < layers.length; i++) {
    if (layers[i].type === 'symbol') {
      firstSymbolId = layers[i].id;
      break;
    }
  }

  map.addSource('campingsites', {
    'type': 'vector',
    'url': 'mapbox://mapmatters.9ilda2dr'
  });

  // circle layer
  map.addLayer({
    'id': 'camping-circle',
    'source': 'campingsites',
    'source-layer': 'camp_geo-1m11gy',
    'type': 'circle',
    "minzoom": 1, 
    "maxzoom": 9, 
    "layout": {
      "visibility": "visible"
    },
    'paint': {
      // make circles larger as the user zooms from z12 to z22
      'circle-radius': {
        'base': 1.75,
        'stops': [
          [1, 2],
          [9, 5]
        ]
      },
      // color circles by ethnicity, using a match expression
      // https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-match
      'circle-color': '#136C26',
      'circle-opacity': 0.6
    }
  });

  // symbol layer
  map.addLayer({
      'id': 'camping',
      'source': 'campingsites',
      'source-layer': 'camp_geo-1m11gy',
      'type': 'symbol',
      "minzoom": 9, // Set zoom level to whatever suits your needs
      'layout': {
        'visibility': 'visible',
        'icon-image': [
          'case',
          ['>', ['get', 'posts'], 3000],'my-castle-15',
          ['>', ['get', 'posts'], 1000],'my-home-15',
          ['>', ['get', 'posts'], 10],'my-campsite-11',
          // ['>=', ['get', 'posts'], 0],'mountain-11',
          'my-campsite-11'
          // ""
        ],
        'icon-padding': 0,
        "icon-size": ['interpolate', ['linear'], ['zoom'], 10, 0.7, 15, 1.8],
        'icon-allow-overlap': true
      }
    },
    firstSymbolId
  );

  // lable layer
  map.addLayer({
    "id": "camping-label",
    "type": "symbol",
    "source": "campingsites",
    'source-layer': 'camp_geo-1m11gy',
    "minzoom": 9, // Set zoom level to whatever suits your needs
    'layout': {
      'visibility': 'visible',
      'text-field': ['get', 'name'],
      'text-variable-anchor': ['top', 'bottom', 'left', 'right'],
      'text-radial-offset': 1.2,
      'text-font': ['Noto Sans CJK JP Regular'],
      // 'text-color': '#48567A',
      "text-size": [
        "interpolate",
        ["linear"],
        ["zoom"],
        7,8,
        22,23
      ],
      'text-justify': 'auto'
    },
    "paint": {
      "text-color": "#013522",
      "text-halo-color": "#fff",
      "text-halo-width": 1
    },
  });

  map.on('data', function () {
    let features = map.querySourceFeatures('campingsites', {
      sourceLayer: 'camp_geo-1m11gy'
    });
    features ? camping_result = queryFeatures.getUniqueFeatures(features, 'name') : null ;
  });
  
  let filterInput = document.getElementById('filter-input');
  filterInput.addEventListener('keyup', function (e) {
    let value = queryFeatures.normalize(e.target.value);

    // Filter visible features that don't match the input value.
    let filtered = camping_result.filter(function (feature) {
      let name = queryFeatures.normalize(feature.properties.name);
      let addr = queryFeatures.normalize(feature.properties.addr);
      return name.indexOf(value) > -1 || addr.indexOf(value) > -1;
    });
    // if (txtValue.toUpperCase().indexOf(filter) > -1) {
    //   li[i].style.display = "";
    // } else {
    //   li[i].style.display = "none";
    // }
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
        true,false
      ]);
      map.setFilter('camping-circle', [
        'match',
        ['get', 'name'],
        filtered.map(function (feature) {
          return feature.properties.name;
        }),
        true,false
      ]);
      map.setFilter('camping-label', [
        'match',
        ['get', 'name'],
        filtered.map(function (feature) {
          return feature.properties.name;
        }),
        true,false
      ]);
    }
  });

  // water icon
  const waterIcon = document.getElementById("waterIcon");
  const defaultWaterColor = map.getPaintProperty('water', 'fill-color');
  const clickWaterIcon = function (e) {
    e.preventDefault;
    e.stopPropagation;
    // let waterLayer = map.getLayer('water');
    let waterLayer = map.querySourceFeatures('composite', {
      sourceLayer: 'water'
      // filter: ['in', 'COUNTY', feature.properties.COUNTY]
    });
    console.log(waterLayer);
    // let line = turf.polygonToLine(waterLayer);
    // let buffered = turf.buffer(waterLayer, 1, {units: 'kilometers'});
    let currentWaterColor = map.getPaintProperty('water', 'fill-color')
    defaultWaterColor !== currentWaterColor 
    ? map.setPaintProperty('water', 'fill-color', 'hsl(197, 67%, 92%)') 
    : map.setPaintProperty('water', 'fill-color', '#33AFFF') ;
  };
  waterIcon.onclick = clickWaterIcon;
  

  const clickMajorLabel = function (e) {
    let features = map.queryRenderedFeatures(e.point);
    // console.log(features[0]);
    let coordinates = features[0].geometry.coordinates;
    map.flyTo({ center: coordinates, zoom: 9});
  }

  const clickMinorLabel = function (e) {
    let features = map.queryRenderedFeatures(e.point);
    // console.log(features[0]);
    let coordinates = features[0].geometry.coordinates;
    map.flyTo({ center: coordinates, zoom: 11 });
  }

  const clickPopup = function (e) {
    let feature = e.features[0];
    let coordinates = feature.geometry.coordinates
    let infoWindow = document.createElement('div');
    infoWindow.id = 'popup';
    document.body.appendChild(infoWindow);
    // infoWindow.className = 'container';

    let phoneTag = feature.properties.call_num ? 'tel:' : '#';
    let phoneLink = feature.properties.call_num ? feature.properties.call_num : '';
    let phoneNum = feature.properties.call_num ? feature.properties.call_num : '전화번호 등록예정';
    let description = 
    // https://codepen.io/ainalem/pen/RqYZNO
    `<div class="to-contents">
        <div class="top">
            <img class="profile_img" src="img/camping-1.svg" alt="profile image" style="width:24px;height:24px;">
            <div class="name-large"> ${feature.properties.name} </div>
            <input type="text" value=${feature.properties.name} id="camp-name" style="position:absolute;left:-1000px;top:-1000px;">
            <a onclick="infoBox.copyFunc()" style="cursor:cell;"> <img class="clipboard_img" src="img/clipboard.png" alt="clipboard" style="width:16px;height:16px;"> </a>
            <div class="x-touch" onclick=infoBox.closePopup()>
                <div class="x">
                    <div class="line1"></div>
                    <div class="line2"></div>
                </div>
            </div>
        </div>
        <div class="bottom">
            <div class="row">
                <img class="link_img" src="img/instagram.png" alt="hashtag" style="width:24px;height:24px;">
                <div class="link"><a href="https://www.instagram.com/explore/tags/${feature.properties.hashtag}" target="bar">
                  #${feature.properties.hashtag} ${feature.properties.posts} posts</a></div>
            </div>
            <div class="row">
              <img class="link_img" src="img/youtube.png" alt="hashtag" style="width:24px;height:24px;">
              <div class="link"><a href="https://www.youtube.com/results?search_query=${feature.properties.hashtag}" target="bar">
                Search ${feature.properties.hashtag}</a></div>
            </div>
            <div class="row2">
              <div class="link_phone">${feature.properties.addr}&nbsp;&nbsp;&nbsp;<a href="${phoneTag}${phoneLink}">${phoneNum}</a></div>
            </div>
            <div class="row2">
              <a href="https://forms.gle/v5FQajKGyvNiD9jk9" target="_blank">
              <img class="link_img" align="left" src="img/info.png" alt="hashtag" style="width:16px;height:16px; position:relative; left:310px">
              </a>
            </div>
        </div>
    </div>`
    
    map.flyTo({ center: coordinates, zoom: 12 });
    document.getElementById("popup").innerHTML = description;
  };

  map.on('click', 'settlement-major-label', clickMajorLabel);
  map.on('click', 'settlement-minor-label', clickMinorLabel);

  map.on('click', 'camping', clickPopup);
  map.on('click', 'camping-circle', clickPopup);
  map.on('click', 'camping-label', clickPopup);
  
  map.on('dragend', function () {
    // document.getElementById("popup").innerHTML = "";
    document.getElementById("popup") ? document.getElementById("popup").remove() : null;
  });

  map.on('mouseenter', 'camping', function () {
    map.getCanvas().style.cursor = 'pointer';
  });


});



// const toggleLayers = [
  //   ['> 1500 posts',['>', ['get', 'posts'],3000], "./img/castle-15.svg"],
  //   ['> 400 posts',['>', ['get', 'posts'],1000], './img/stadium-15.svg'],
  //   ['> 0 posts',['>', ['get', 'posts'],10], './img/ranger-station-11.svg'],
  //   ['All capming site',['>=', ['get', 'posts'],0], './img/mountain-11.svg']
  // ];
 
  // // set up the corresponding toggle button for each layer
  // toggleLayers.forEach(function(item) {
  //   let toggleLayer = document.createElement('div');
  //   toggleLayer.className = 'active';
  //   toggleLayer.href = '#';
    
  //   let toggleImg = document.createElement('img');
  //   toggleImg.src = item[2]
    
  //   let toggleText = document.createTextNode(item[0]);
  //   toggleText.innerHTML = item[0]
  //   toggleText.className = 'toggle'

  //   toggleLayer.append(toggleImg);
  //   // toggleLayer.append(toggleText);
    
  //   toggleImg.onclick = function(e) {
  //     e.preventDefault;
  //     e.stopPropagation;
  //     let filter = item[1];
  //     // console.log(filter);
  //     map.setFilter('camping',filter);
  //     map.setFilter('camping-label',filter);
  //     map.flyTo({ zoom: 8 });
  //     // map.fitBounds(bounds, {padding: 20});
  //   };
  //   let layers = document.getElementById('menu');
  //   layers.appendChild(toggleLayer);
  // });



  // function myFunction() {
  //   // Declare variables
  //   var input, filter, ul, li, a, i, txtValue;
  //   input = document.getElementById('myInput');
  //   filter = input.value.toUpperCase();
  //   ul = document.getElementById("myUL");
  //   li = ul.getElementsByTagName('li');
  
  //   // Loop through all list items, and hide those who don't match the search query
  //   for (i = 0; i < li.length; i++) {
  //     a = li[i].getElementsByTagName("a")[0];
  //     txtValue = a.textContent || a.innerText;
  //     if (txtValue.toUpperCase().indexOf(filter) > -1) {
  //       li[i].style.display = "";
  //     } else {
  //       li[i].style.display = "none";
  //     }
  //   }
  // }