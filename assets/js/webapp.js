storage = {
  first_visit: false,
  fire_relocate: true
}
$(document).ready(function() {
  localStorage.removeItem('first_visit_done');
  if ($('.home').length) {
    if (typeof(Storage) == "undefined") {
      $('#startquestion').html('<div id="browser-error"><h2>Nicht unterstützter Browser</h2><p>Bitte aktualisiere Deinen Browser.<br>Google Chrome 4+, Internet Explorer 8+, Firefox 3.5+, Safari 4+, Opera 11.5+</p><p><a href=""></a></div>').css({bottom: 0});
      $('#startquestion').fadeIn();
      $('#important-links').fadeIn();
    }
    else {
      storage['first_visit'] = null == localStorage.getItem('first_visit_done')
      if (storage['first_visit']) {
        $('#startquestion').fadeIn(600);
        $('#important-links').fadeIn(600);
        
        $('#startquestion-type').multiselect({
          buttonClass: 'form-control',
          buttonContainer: '<div class="btn-group bootstrap-multiselect" />',
          numberDisplayed: 1,
          nSelectedText: ' Fahrzeugvarianten',
          allSelectedText: 'beliebiges Fahrzeug',
          nonSelectedText: 'bitte wählen',
          includeSelectAllOption: true,
          selectAllText: 'alle auswählen'
        });
        
        // Geo-Live-Suche
        $('#startquestion-location').live_search({
          url: '/search-region-live',
          form: '#startquestion-form',
          input: '#startquestion-location',
          live_box: '#startquestion-location-live',
          submit: '#startquestion-submit',
          livesearch_result_only: true,
          process_result_line: function(result) {
            return('<li data-q="' + result['lat'] + ',' + result['lon'] + '" data-q-descr="' + result['postalcode'] + ' ' + result['name'] + '">' + result['postalcode'] + ' ' + result['name'] + '</li>');
          },
          after_submit: function() {}
        });
        
        $('#startquestion-form').submit(function(evt) {
          evt.preventDefault();
          if ($('#startquestion-location').attr('data-q')) {
            $('#search-location').attr('data-q', $('#startquestion-location').attr('data-q'));
            $('#search-location').val($('#startquestion-location').val());
            $('#search-type').val($('#startquestion-type').val());
            $('#search-type').multiselect('refresh');
            $('#search-form select').change(function(evt) {
              search_stations(false);
            });
            search_stations(true);
          }
        });
      }
      else {
        $('#header').css({ display: 'block' });
        if ($(window).width() >= 768)
          $('#search').fadeIn(200);
        else {
          $('#search').css({ display: 'block' });
        }
      }
      
      // init category icons
      storage['station_type_icons'] = {
        1: L.VectorMarkers.icon({icon: 'bicycle', prefix: 'fa', markerColor: '#00B44C', iconColor: '#FFFFFF'}),
        2: L.VectorMarkers.icon({icon: 'bicycle', prefix: 'fa', markerColor: '#000000', iconColor: '#FFFFFF'}),
        3: L.VectorMarkers.icon({icon: 'bicycle', prefix: 'fa', markerColor: '#000000', iconColor: '#FFFFFF'}),
        4: L.VectorMarkers.icon({icon: 'car', prefix: 'fa', markerColor: '#006AB4', iconColor: '#FFFFFF'}),
        5: L.VectorMarkers.icon({icon: 'truck', prefix: 'fa', markerColor: '#00B2B4', iconColor: '#FFFFFF'})
      }
      
      $('#search').css({ top: $('#header').height() });
      
      if ($(window).width() >= 768)
        $('#search').css({ width: '280px', 'padding-left': '15px', 'padding-right': '15px' });
      else
        $('#search').css({ width: '0px', 'padding-left': '0px', 'padding-right': '0px' });

      $('#search-toggle').click(function() {
        if ($('#search').width()) {
          $('#search').animate({ width: '0px', 'padding-left': '0px', 'padding-right': '0px' });
        }
        else {
          $('#search').animate({ width: '280px', 'padding-left': '15px', 'padding-right': '15px' });
        }
      });
      
      $('#search-type').multiselect({
        buttonClass: 'form-control',
        buttonContainer: '<div class="btn-group bootstrap-multiselect" />',
        numberDisplayed: 1,
        nSelectedText: ' Fahrzeugvarianten',
        allSelectedText: 'beliebiges Fahrzeug',
        nonSelectedText: 'bitte wählen',
        includeSelectAllOption: true,
        selectAllText: 'alle auswählen'
      });
      
      // Geo-Live-Suche
      $('#search-location').live_search({
        url: '/search-region-live',
        form: '#search-form',
        input: '#search-location',
        live_box: '#search-location-live',
        submit: '#basic-submit',
        livesearch_result_only: true,
        process_result_line: function(result) {
          return('<li data-q="' + result['lat'] + ',' + result['lon'] + '" data-q-descr="' + result['postalcode'] + ' ' + result['name'] + '">' + result['postalcode'] + ' ' + result['name'] + '</li>');
        },
        after_submit: function() {}
      });
      
      if (!storage['first_visit']) {
        $('#search-form select').change(function(evt) {
          search_stations(false);
        });
      }
      
      $('#search-form').submit(function(evt) {
        evt.preventDefault();
        if ($('#search-location').attr('data-q'))
          search_stations(true);
      });
      
      $(window).on('resize', function() {
        if ($(window).width() >= 768) {
          $('#search').css({ width: '280px', 'padding-left': '15px', 'padding-right': '15px' });
        }
        else {
          $('#search').css({ width: '0px', 'padding-left': '0px', 'padding-right': '0px' });
        }
      });
      
      // Init map
      L.Icon.Default.imagePath = '/static/images/leaflet/' ;
      map = new L.Map('map', { zoomControl: false, attributionControl: false });
      var backgroundLayer = new L.TileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v9/tiles/256/{z}/{x}/{y}?access_token=' + mobilitaet_finden_conf['mapbox_token'], {
        maxZoom: 18, 
        minZoom: 1
      });
      storage['map'] = map;
      L.control
        .zoom({ position: 'bottomleft'})
        .addTo(map);
      map.setView(new L.LatLng(51.163375, 10.447683), 7).addLayer(backgroundLayer);
      areas = L.layerGroup().addTo(map);
      
      storage['markers'] =  new L.LayerGroup();
      storage['markers'].addTo(map);
      
      map.on('moveend', function() {
        if (storage['fire_relocate'] && !storage['first_visit'])
          search_stations(false);
      });
    }
  }
});


function search_stations(relocate) {
  if (relocate)
    storage['fire_relocate'] = false;
  
  // activate select onchange if first load
  if (storage['first_visit']) {
    localStorage.setItem('first_visit_done', true);
  }
  fq = [];
  var map_border = storage['map'].getBounds();
  if (relocate) {
    lat = parseFloat($('#search-location').attr('data-q').split(',')[0]);
    lon = parseFloat($('#search-location').attr('data-q').split(',')[1]);
    
    // 1px lon = 0,00017578125 degree
    // 1px lat = 0,000087890625 degree
    limits = Array(
      'location.lat>=' + String(lat - 1.2 * (0.000087890625 * $(window).height())),
      'location.lat<=' + String(lat + 1.2 * (0.000087890625 * $(window).height())),
      'location.lon>=' + String(lon - 1.2 * (0.00017578125 * $(window).width())),
      'location.lon<=' + String(lon + 1.2 * (0.00017578125 * $(window).width()))
    );
  }
  else {
    lat = storage['map'].getCenter()['lat'];
    lon = storage['map'].getCenter()['lng'];
    limits = Array(
      'location.lat>=' + String(lat - 1.2 * (map_border.getNorth() - map_border.getSouth())),
      'location.lat<=' + String(lat + 1.2 * (map_border.getNorth() - map_border.getSouth())),
      'location.lon>=' + String(lon - 1.2 * (map_border.getEast() - map_border.getWest())),
      'location.lon<=' + String(lon + 1.2 * (map_border.getEast() - map_border.getWest()))
    );
  }
  search_params = {
    'pp': 10000,
    'l': limits.join(';'),
    'vehicle_type': $('#search-type').val().join(',')
  }
  // vehicle_all
  if ($('#search-vehicle_all').val()) {
    search_params['vehicle_all'] = $('#search-vehicle_all').val();
    if (typeof(Storage) !== "undefined")
      localStorage.setItem("vehicle_all", $('#search-vehicle_all').val());
  }
  
  // vehicle_type
  if ($('#search-vehicle_type').val()) {
    search_params['vehicle_type'] = $('#search-vehicle_type').val().join(',');
    if (typeof(Storage) !== "undefined")
      localStorage.setItem("vehicle_type", $('#search-vehicle_type').val().join(','));
  }
  $.post('/search/sharing-stations', search_params, function(raw_data) {
    $('#loading-overlay').css({'display': 'none'});
    storage['markers'].clearLayers()
    $(raw_data.response).each(function(i, item) {
      marker_text = '<strong>' + item.name + '</strong><br>';
      if (item.vehicle_all) {
        marker_text += 'Fahrzeuge: ' + item.vehicle_all + '<br>';
      }
      marker_text += 'Anbieter: <a href="/anbieter/' + item.sharing_provider_slug + '">' + item.sharing_provider_name + '</a>';
      if (item.station_type)
        marker = L.marker([item.lat, item.lon], { icon: storage.station_type_icons[item.station_type] } ).bindPopup(marker_text);
      else
        marker = L.marker([item.lat, item.lon]).bindPopup(marker_text);
      storage['markers'].addLayer(marker);
    });
  });
  
  if (relocate) {
    if ($('#search-location').attr('data-q')) {
      storage['map'].setView([$('#search-location').attr('data-q').split(',')[0], $('#search-location').attr('data-q').split(',')[1]], 13);
    }
  }
  
  if (storage['first_visit']) {
    storage['map'].options.minZoom = 12;
    $('#important-links').fadeOut(400);
    $('#startquestion').fadeOut(400, function() {
      $('#startquestion').remove();
    });
    $('#header').fadeIn();
    if ($(window).width() >= 768)
      $('#search').fadeIn(200);
    else
      $('#search').css({ display: 'block' });
    
    storage['first_visit'] = false;
  }
  
  if (relocate)
    storage['fire_relocate'] = true;
}

