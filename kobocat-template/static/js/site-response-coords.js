// var coordinates = [{"geometry": {"type": "Point", "coordinates": [84.428713,27.2155476] }, "type": "Feature", "properties": {"submitted_by": "elvar", "fs_uuid": "3391", "id": 433}}, {"geometry": {"type": "Point", "coordinates": [85.428713, 27.7155476 ]}, "type": "Feature", "properties": {"submitted_by": "elvar", "fs_uuid": "3391", "id": 435}}, {"geometry": {"type": "Point", "coordinates": [85.4138713, 27.71531476]}, "type": "Feature", "properties": {"submitted_by": "elvar", "fs_uuid": "3804", "id": 450}}];




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

//console.log(data.features.length);
//if(data.features.length!=0){
//map = L.map("map",{layers:osm}).fitBounds(markers); 
// }
//else{
map = L.map("map",{layers:osm}).setView([27, 85], 6);;
//}



site_response = new L.geoJson(coordinates, {
    pointToLayer: function(feature, latlng) {
        
        if(feature.properties.submitted_by == "site_origin" ){
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker-blue.png'
            });
        }
        else{
            icon = L.icon({
                iconSize: [25, 25],
                iconAnchor: [13, 27],
                popupAnchor:  [1, -24],
                iconUrl: static_url+'images/marker-red.png'
            });
        }
        // console.log(latlng);                
        lonlat={'lat': latlng['lng'], 'lng': latlng['lat']}
        var marker = L.marker(lonlat, {icon: icon});


        return marker;
    }, 

    onEachFeature: function(feature, layer) {
        if(feature.properties.submitted_by == "site_origin" ){
                layer.bindPopup("Site Location");
        }
        else{
            layer.bindPopup("Submitted By:"+feature.properties.submitted_by+"<br><a href="+'/fieldsight/application/?submission='+feature.properties.fs_uuid+'#/submission-details'+" target='_blank'>View Submission</a>");
        }
        console.log(layer);
    }
}).addTo(map);

if (coordinates.length > 0) {
    map.fitBounds(site_response.getBounds());
}

console.log(map);


map.on('click',function(){
    $('.popop-head').removeClass('changed');
    $('.popop-head').html('');
    $('.address-popop').html('');
    //$('.contact-popup').html('');
});

if (initGeoLayers) {
    initGeoLayers();
}
