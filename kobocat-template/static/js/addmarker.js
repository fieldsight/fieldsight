var map = L.map("map", {
		center: [27.714875814507074, 85.3243088722229],
		zoom: 10
});

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

map.addLayer(googleStreets);
layerswitcher = L.control.layers(baseLayers, {}, {collapsed: true}).addTo(map);

newMarker = new L.marker();
if(elat == "None"){
	lat = 27.714875814507074;
}else{
	lat = parseFloat(elat);
}

if(elong == "None"){
	lon = 85.3243088722229;
}else{
	lon = parseFloat(elong);
}
addMarker(lat,lon);
function addMarker(lat, lon){
	if(newMarker != ""){
		map.removeLayer(newMarker);
	}
	var icon = L.icon({
		//iconSize: [27, 27],
		//iconAnchor: [14, 35],
		iconAnchor: [14, 42],
		popupAnchor:  [1, -24],
		iconUrl: static_url+'css/images/marker-icon.png'
	});
	newMarker = new L.marker([lat,lon],{icon: icon,draggable:'true'});			
	
	newMarker.on('dragend', function(event){
		var marker = event.target;
		var position = marker.getLatLng();
		marker.setLatLng(position,{draggable:'true'}).update();
		$("#Latitude")[0].value = position.lat;
		$("#Longitude")[0].value  = position.lng;
	});
	
	map.addLayer(newMarker);
	//console.log($("#Latitude"));
	$("#Latitude")[0].value = lat;
	$("#Longitude")[0].value = lon;


}

map.on('click',function(e){
	lat = e.latlng.lat;
	lon = e.latlng.lng;
	addMarker(lat,lon);

});


$(".LatLon").on('input',function(){
	if($(this)[0].id == "Latitude"){
		lat = $(this)[0].value;
		console.log(lat);
		console.log("reaadcee")
	}
	else {
		lon = $(this)[0].value;
	}
	//console.log($(this)[0].value);
	if(lat && lon){

	    addMarker(lat,lon);
	}

});

	

