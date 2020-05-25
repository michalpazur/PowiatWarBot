d3.json('../map-data/powiaty.json').then(function(powiatyJson)
{
    var map = L.map('map').setView([0,0], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'}
    ).addTo(map);
    var powiatyBaseLayer = L.geoJSON(powiatyJson,
        {
            style: function(feature)
            {
                return {fillOpacity: 1, color: feature.properties.value}
            }
        }).addTo(map)
    map.fitBounds(powiatyBaseLayer.getBounds())
})