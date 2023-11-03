function docReady () {
  const checkbox = $("input[type='checkbox']");
  const apiStatus = $('div#api_status');

  let amenityIds = [];
  let amenityNames = [];

  checkbox.click(function () {
    const newId = $(this).attr('data-id');
    const newName = $(this).attr('data-name');

    if ($(this).is(':checked')) {
      amenityIds.push(newId);
      amenityNames.push(newName);
    } else {
      amenityIds = amenityIds.filter((id) => id !== newId);
      amenityNames = amenityNames.filter((name) => name !== newName);
    }
    $('.amenities h4').text(amenityNames.sort().join(', '));
  });

  $.get('http://0.0.0.0:5001/api/v1/status/', function (data, textStatus) {
    if (data.status === 'OK') { apiStatus.addClass('available'); } else { apiStatus.removeClass('available'); }
  });
}

$(document).ready(docReady);
