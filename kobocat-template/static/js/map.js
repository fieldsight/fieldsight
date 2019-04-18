var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
});

googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});
googleHybrid = L.tileLayer('http://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});
googleSat = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});
googleTerrain = L.tileLayer('http://{s}.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});

var baseLayers = {
    "OpenStreetMap": osm,
    "Google Streets": googleStreets,
    "Google Hybrid": googleHybrid,
    "Google Satellite": googleSat,
    "Google Terrain": googleTerrain
};

//arrays for legend
statusIconList = ['marker-red','marker-yellow','marker-green','marker-blue','marker-grey'];
statusText = ['Rejected submission','Flagged submission','Approved submission','Pending submission','No submission'];
progressIconList = ['marker-red','marker10-20','marker30-40','marker50-60','marker70-80','marker80-90','marker90-100'];
progressText = ['0%','0-20%','20-40%','40-60%','60-80%','80-100%', '100%'];
//end array legend
console.log(data);
markers = new L.geoJson(data, {
    pointToLayer: function(feature, latlng) {
        // rejected

        if(feature.status == 1){
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker-red.png'
            });
        }
        else if(feature.status == 2){
            // flagged
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker-yellow.png'
            });
        }
        else if(feature.status == 3){
            // approved
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker-green.png'
            });
        }
        else if(feature.status == 0){
            // pending
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker-blue.png'
            });
        }else if(feature.status == 4){
            // pending ( No Data )
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker-grey.png'
            });
        }
        else{
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker-blue.png'
            });
        }
        //console.log(icon.options);
        var marker = L.marker(latlng, {icon: icon});
        return marker;

    }, 
    onEachFeature: function(feature, layer) {
        var address = feature.properties.address || "";
        var url = "<a href=/fieldsight/site-dashboard/"+feature.id+">"+feature.properties.name+"</a>";
        layer.bindPopup(url+'<br/>'+address);

    }
});

if (initGeoLayers) {
    initGeoLayers();
}

//console.log(data.features.length);
if(data.features.length != 0){
    map = L.map("map",{layers:osm}).fitBounds(markers.getBounds()); 
}
else{
    map = L.map("map",{layers:osm}).setView([27, 85], 6);;
}

//map.addLayer(osm);
layerswitcher = L.control.layers(baseLayers, {}, {collapsed: true}).addTo(map);

map.addLayer(markers);




// map.fitBounds(markers.getBounds());


// layerswitcher.addOverlay(markers, "Schools");




progressLayer = new L.geoJson(data, {
    pointToLayer: function(feature, latlng) {
        // console.log(feature);
        if(feature.progress == 0){
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker-red.png'
            });
        }
        else if(feature.progress >= 1 && feature.progress <= 20){
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker10-20.png'
            });
        }

        else if(feature.progress > 20 && feature.progress <= 40){
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker30-40.png'
            });
        }
        else if(feature.progress > 40 && feature.progress <= 60){
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker50-60.png'
            });
        }
        else if(feature.progress > 60 && feature.progress <= 80){
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker70-80.png'
            });
        }
        else if(feature.progress > 80 && feature.progress < 100){
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker80-90.png'
            });
        }
        else if(feature.progress == 100){
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker90-100.png'
            });
        }
        //console.log(icon.options);
        var marker = L.marker(latlng, {icon: icon});
        return marker;

    }, 
    onEachFeature: function(feature, layer) {
        var address = feature.properties.address || "";
        var url = "<a href=/fieldsight/site-dashboard/"+feature.id+">"+feature.properties.name+"</a>";
        layer.bindPopup(url+'<br/>'+address);

    }
});


progressLayer.on('click',function(){
    console.log("progresslayer clicked");
});

//layerswitcher.addOverlay(progressLayer, "Site Progress");
//legend start
function addLegend(type){

    var legend = L.control({position: 'bottomright'});  
    legend.onAdd = function (map) {
        $('.legend').remove();
        var div = L.DomUtil.create('div', 'info legend'),
            labels = [''];
        //console.log(div);
        if(type == 'form_status'){
            labels.push('<strong>Submission Status</strong>');
            for (var i = 0; i < statusIconList.length; i++) {

                //console.log(icons[i]);
                labels.push(
                    '<div style="display: inline-block; width:25px; height: 25px; "><img style="display: inline-block; width:25px; height: 25px;" src = "'+static_url+'images/'+statusIconList[i]+'.png"></img></div> &ndash; '+ statusText[i]);
            }
            div.innerHTML = labels.join('<br/>');
            return div;

        }
        else {
            labels.push('<strong>Progress Status</strong>');
            for (var i = 0; i < progressIconList.length; i++) {

                //console.log(icons[i]);
                labels.push(
                    '<div style="display: inline-block; width:25px; height: 25px; "><img style="display: inline-block; width:25px; height: 25px;" src = "'+static_url+'images/'+progressIconList[i]+'.png"></img></div> &ndash; '+ progressText[i]);
            }
            div.innerHTML = labels.join('<br/>');
            return div;

        }
    };
    legend.addTo(map);
    $(".info.legend.leaflet-control").css({'background-color':'white', 'padding': '5px'});
}
addLegend('form_status');

//legend end


$(".switch").on('change',function(){
    /*if($(this).is(':checked') == false){
                $(this).is(':checked') = true;
            }
            else{
                $(this).is(':checked') = false;
            } */
    $('.switch').not(this).prop('checked', false);
    if($(this)[0].id == "form_status"){
        addLegend('form_status');
        if(map.hasLayer(progressLayer)){
            console.log('here');
            map.removeLayer(progressLayer);
        }

        if(!map.hasLayer(markers)){
            console.log('not geojson layer');
            map.addLayer(markers);
        }
    }
    else if($(this)[0].id == "project_progress"){
        addLegend('project_progress');
        if(map.hasLayer(markers)){

            map.removeLayer(markers);
        }
        if(!map.hasLayer(progressLayer)){
            map.addLayer(progressLayer);
        }
    }
});

markers.on('click',function(e){
    var site_id = e.layer.feature.id;
    // console.log(server_url+'/fieldsight/api/site-schedules/'+site_id);
    $.ajax({
        url: '/fieldsight/api/site-images/'+site_id,
        type: 'get', // This is the default though, you don't actually need to always mention it
        dataType: "json",
        success: function(data) {
            img = '';
            console.log(data.images);
            for(i=0;i<data.images.length;i++){console.log(data.images[i]);
                img += '<img src = '+data.images[i]+'/>';
            }

            $('.popop-container').show();
            $('.popop-gallery').html(img);
            //$('.popop-gallery').html(data.images);
        },
        failure: function(data) { 
        }
    }); 
    $('.popop-head').addClass('changed');
    $('.popop-head').html(e.layer.feature.properties.name);
    $('.address-popop').html(e.layer.feature.properties.address);
    //$('.contact-popup').html(e.layer.feature.properties.contact);


});

progressLayer.on('click',function(e){
    var site_id = e.layer.feature.id;
    // console.log(server_url+'/fieldsight/api/site-schedules/'+site_id);
    $.ajax({
        url: '/fieldsight/api/site-images/'+site_id,
        type: 'get', // This is the default though, you don't actually need to always mention it
        dataType: "json",
        success: function(data) {
            img = '';
            console.log(data.images);
            for(i=0;i<data.images.length;i++){console.log(data.images[i]);
                img += '<img src = '+data.images[i]+'/>';
            }

            $('.popop-container').show();
            $('.popop-gallery').html(img);
            //$('.popop-gallery').html(data.images);
        },
        failure: function(data) { 
        }
    }); 
    $('.popop-head').addClass('changed');
    $('.popop-head').html(e.layer.feature.properties.name);
    $('.address-popop').html(e.layer.feature.properties.address);
    //$('.contact-popup').html(e.layer.feature.properties.contact);


});

map.on('click',function(){
    $('.popop-head').removeClass('changed');
    $('.popop-head').html('');
    $('.address-popop').html('');
    //$('.contact-popup').html('');
});
