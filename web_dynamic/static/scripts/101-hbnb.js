let allUsers;

/**
 * IIFE Function to retrieve all users from the database
 */
(function getAllUsers () {
  $.get('http://127.0.0.1:5001/api/v1/users', function (data, _) {
    allUsers = data;
  });
})();

/**
 * Callback function to setup wwebpage and also add event handlers when DOM is fully loaded
 */
function initScript () {
  const amenityCheckboxes = $(".amenities input[type='checkbox']");
  const stateCheckboxes = $('.state-checkbox');
  const cityCheckboxes = $('.city-checkbox');

  const apiStatus = $('div#api_status');
  const search = $('button');

  const jsonPost = {};
  const amenityIds = [];
  const amenityNames = [];
  const cityIds = [];
  const cityNames = [];
  const stateIds = [];
  const stateNames = [];

  // Add event handler for checkboxes with callback function bound to local variables
  amenityCheckboxes.on('click', checkboxFn.bind({}, amenityIds, amenityNames, 'amenities'));
  cityCheckboxes.on('click', checkboxFn.bind({}, cityIds, cityNames, 'locations'));
  stateCheckboxes.on('click', checkboxFn.bind({}, stateIds, stateNames, 'locations'));

  initialAPICall(apiStatus, jsonPost);

  jsonPost.amenities = amenityIds;
  jsonPost.cities = cityIds;
  jsonPost.states = stateIds;
  search.on('click', filterSearch.bind({}, jsonPost));
}

/**
 * This callback function inserts <article> tags corresponding to the places retrieved from database
 * @param   {object} data Object containing places retrieved from database
 */
function fillArticle (data, _) {
  const placesSection = $('section.places');

  placesSection.children('article').remove();
  for (const place of data) {
    const articleTag = `
      <article>
        <div class="title_box">
          <h2>${place.name}</h2>
          <div class="price_by_night">${place.price_by_night}</div>
        </div>
        <div class="information">
          <div class="max_guest">
            <div class="icon"></div>
              ${place.max_guest} Guest${place.max_guest !== 1 ? 's' : ''}
          </div>
          <div class="number_rooms">
            <div class="icon"></div>
            ${place.number_rooms} Bedroom${place.number_rooms !== 1 ? 's' : ''}
          </div>
          <div class="number_bathrooms">
            <div class="icon"></div>
            ${place.number_bathrooms} Bathroom${place.number_bathrooms !== 1 ? 's' : ''}
          </div>
        </div>
        <div class="description">
          ${place.description}
        </div>
        <div class="reviews">
          <h2>Reviews</h2> <span data-id="${place.id}">show</span>
          <ul class="hide"></ul>
        </div>
      </article>
      `;
    placesSection.append(articleTag);
  }
  $('article .reviews span').click(getReviews.bind({}));
}

/**
 * This function get the reviews on a place
 */
function getReviews (e) {
  const placeId = $(e.target).attr('data-id');
  const ul = $(e.target).siblings('ul');
  const reviewH2 = $(e.target).siblings('h2');

  ul.toggleClass('show hide');
  if (ul.hasClass('show')) {
    $(e.target).text('hide');
    ul.children('li').remove();
    $.get(`http://127.0.0.1:5001/api/v1/places/${placeId}/reviews`, function (data, textStatus) {
      reviewH2.text(`${data.length || ''} Reviews`);
      for (const review of data) {
        const date = new Intl.DateTimeFormat(navigator.language, { dateStyle: 'long' }).format(new Date(review.updated_at));
        const user = allUsers ? allUsers.find((el, _) => el.id === review.user_id) || '' : '';
        const reviewLI = `
          <li>
            <h3>From ${user && user.first_name} the ${date}</h3>
            <p>${review.text}</p>
          </li>
          `;
        ul.append(reviewLI);
      }
    });
  } else {
    $(e.target).text('show');
    reviewH2.text('Reviews');
  }
}

/**
 * This function retrieves all places present in database as filtered by jsonPost param
 * @param   {object} jsonPost   Object containing POST request body
 */
function filterSearch (jsonPost) {
  $.ajax({
    type: 'POST',
    url: 'http://127.0.0.1:5001/api/v1/places_search/',
    data: JSON.stringify(jsonPost),
    contentType: 'application/json',
    success: fillArticle
  });
}

/**
 * This callback function populates two arrays when a checkbox is clicked
 * @param   {Array} amenityIds     Array containing Ids of checked input checkboxes
 * @param   {Array} amenityNames   Array containing Names of checked input checkboxes
 * @param   {String} cls           String is the class of h4 tag to modify
 */
function checkboxFn (Ids, Names, cls, e) {
  const newId = $(e.target).attr('data-id');
  const newName = $(e.target).attr('data-name');

  if ($(e.target).is(':checked')) {
    Ids.push(newId);
    Names.push(newName);
  } else {
    Ids.splice(Ids.indexOf(newId), 1);
    Names.splice(Names.indexOf(newName), 1);
  }
  // Set text of h4 tag to string of all checked amentities
  $(`.${cls} h4`).text(Names.sort().join(', '));
}

/**
 * This function retrieves the status of api and also all places present in database
 * @param   {object} apiStatus  jQuery Object representing the #api_status div
 * @param   {object} jsonPost   Object containing POST request body
 */
function initialAPICall (apiStatus, jsonPost) {
  $.get('http://127.0.0.1:5001/api/v1/status/', function (data, textStatus) {
    if (data.status === 'OK') { apiStatus.addClass('available'); } else { apiStatus.removeClass('available'); }
  });

  filterSearch(jsonPost);
}

$(document).ready(initScript);
