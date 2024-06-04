document.getElementById('lifeCycleForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var productName = document.getElementById('productName').value;
    var productDescription = document.getElementById('productDescription').value;

    $.ajax({
        url: 'http://localhost:8000/api/lcs/', // Update with your actual API URL
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            name: productName,
            description: productDescription
        }),
        success: function(response) {
            document.getElementById('stagesResult').innerHTML = '<pre>' + JSON.stringify(response, null, 2) + '</pre>';
        },
        error: function(xhr, status, error) {
            document.getElementById('stagesResult').innerHTML = 'Error: ' + xhr.responseText;
        }
    });
});

document.getElementById('footprintForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var productName = document.getElementById('footprintName').value;
    var lifeStages = document.getElementById('lifeStages').value.split(',');
    var weights = {};
    document.getElementById('weights').value.split(',').forEach(function(weight, index) {
        if (weight.trim()) {
            weights[lifeStages[index].trim()] = parseFloat(weight);
        }
    });

    $.ajax({
        url: 'http://localhost:8000/api/calculate/', // Update with your actual API URL
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            name: productName,
            life_cycle_stages: lifeStages,
            weights: weights
        }),
        success: function(response) {
            document.getElementById('footprintResult').innerHTML = '<pre>' + JSON.stringify(response, null, 2) + '</pre>';
        },
        error: function(xhr, status, error) {
            document.getElementById('footprintResult').innerHTML = 'Error: ' + xhr.responseText;
        }
    });
});
