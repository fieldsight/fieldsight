
    $(document).ready(function() {
        var map = L.map('map').setView([27.7, 85.4], 7);
				
				osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
					attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
				}).addTo(map);

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
				
				layerswitcher = L.control.layers(baseLayers, {}, {collapsed: true}).addTo(map);

    });
                