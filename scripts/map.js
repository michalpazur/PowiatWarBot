d3.json('../map-data/powiaty.json').then(function(powiatyJson)
{
    function mergedPowiaty(feature, layer)
    {
        console.log(feature.properties.belongs_to)
        layer.setStyle(
            {
                className: 'powiat ' + feature.properties.name,
                fillColor: powiatyJson[feature.properties.belongs_to].value,
                fillOpacity: 1,
                weight: 1,
                color: 'black'
            })
    }
    function dashedPowiaty(feature, layer)
    {
        layer.setStyle(
            {
                className: 'territory ' + feature.properties.name,
                dashArray: '3 15',
                color: 'black',
                weight: 1,
                fillOpacity: 0
            })
        var territoryName = feature.properties.name.replace('miasto', '');
        var firstLetter = territoryName.toUpperCase().charAt(0);
        territoryName = territoryName.slice(1);
        territoryName = firstLetter + territoryName;
        popupContent = "<b>" + territoryName + "</b> occupied by <b>" + feature.properties.belongs_to_name.replace('miasto', '') + "</b>.";
        layer.bindPopup(popupContent);
    }

    function countryHover(feature, layer)
    {
        layer.setStyle(
            {
                fill: false,
                color: 'limegreen',
                weight: 3
            })
    }

    var map = L.map('map').setView([0,0], 10);
    var stamenMap = new L.StamenTileLayer("terrain");
    map.addLayer(stamenMap);
    
    d3.json('../map-data/powiaty-shapes.json').then(function(powiatyShapesJson)
    {
        powiatyShapes = topojson.feature(powiatyShapesJson, powiatyShapesJson.objects.data);

        for (var obj in powiatyJson)
        {
            var mergedPowiat = topojson.merge(powiatyShapesJson, powiatyShapesJson.objects.data.geometries.filter(function (p) { return p.properties.belongs_to == obj}));
            mergedPowiat.properties = {};
            mergedPowiat.properties.belongs_to = obj;
            L.geoJSON(mergedPowiat, {onEachFeature: mergedPowiaty}).addTo(map);
        }

        var dashedLayer = L.geoJSON(powiatyShapes, {onEachFeature: dashedPowiaty}).addTo(map);
        map.fitBounds(dashedLayer.getBounds());
    })
})