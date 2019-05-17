function getGeoJsonStyle() {
    return {
        fillOpacity: 0.2,
        color: '#00628e',
        weight: 2,
    };
}

function initFeature(feature, layer) {
    layer.bindTooltip(feature.properties.title, { sticky: true });
    return true;
}

const allLayers = {};
let layerOrders = [];

function sortLayers() {
    const reverse = [...layerOrders].reverse();
    reverse.forEach((layerId) => {
        allLayers[layerId] && allLayers[layerId].bringToBack();
    });

    const firstLayer = allLayers[layerOrders[0]];
    map.flyToBounds(firstLayer.getBounds(), { duration: 0.5 });
}

function loadGeoLayers(geoLayerIds) {
    Object.keys(allLayers).forEach((layerId) => {
        if (geoLayerIds.indexOf(layerId) === -1) {
            map.removeLayer(allLayers[layerId]);
            delete allLayers[layerId];
        }
    });

    geoLayerIds.forEach((geoLayerId) => {
        if (allLayers[geoLayerId]) {
            return;
        }

        $.getJSON('/fieldsight/geo-json/' + geoLayerId + '/', function(data) {
            if (layerOrders.indexOf(geoLayerId) === -1) {
                return;
            }

            layer = L.geoJson(data, {
                style: getGeoJsonStyle,
                onEachFeature: initFeature,
            }).addTo(map);

            allLayers[geoLayerId] = layer;
            sortLayers();
        });
    });

    // if (!geoLayerId) {
    //     if (activeGeoLayer) {
    //         map.removeLayer(activeGeoLayer);
    //     }
    //     return;
    // }
}

function initGeoLayers() {
    $('input[name="geo-layer"]').change(function() {
        var selected = [];
        layerOrders = [];

        $('input[name="geo-layer"]').each(function() {
            if ($(this).is(":checked")) {
                selected.push($(this).val());
                layerOrders.push({
                    level: parseInt($(this).data('level'), 10),
                    id: $(this).val(),
                });
            }
        });
        layerOrders.sort((a, b) => a.level - b.level);
        layerOrders = layerOrders.map(l => l.id);

        loadGeoLayers(selected);
    });
}
