d3.json('../map-data/powiaty.json').then(function(powiatyJson)
{
    function mergedPowiaty(feature, layer)
    {
        layer.setStyle(
            {
                className: 'powiat ' + feature.properties.name,
                fillColor: powiatyJson[feature.properties.belongs_to]['color'],
                fillOpacity: 1,
                color: 'black',
                weight: 1
            })
    }
    function dashedPowiaty(feature, layer)
    {
        layer.setStyle(
            {
                className: 'territory ' + feature.properties.name,
                dashArray: '3 15',
                color: 'black',
                weight: 1.5,
                fillOpacity: 0
            })
        var territoryName = feature.properties.name;
        var firstLetter = territoryName.toUpperCase().charAt(0);
        territoryName = territoryName.slice(1);
        territoryName = firstLetter + territoryName;
        popupContent = "<b>" + territoryName + "</b> occupied by <b>" + feature.properties.belongs_to_name + "</b>.";
        layer.bindPopup(popupContent)
    }

    var map = L.map('map').setView([0,0], 10);
    var stamenMap = new L.StamenTileLayer("terrain");
    map.addLayer(stamenMap);
    
    d3.json('../map-data/powiaty-shapes.json').then(function(powiatyShapes)
    {
        var dashedLayer = L.geoJSON(powiatyShapes, {onEachFeature: dashedPowiaty}).addTo(map)
        map.fitBounds(dashedLayer.getBounds())
    })
})