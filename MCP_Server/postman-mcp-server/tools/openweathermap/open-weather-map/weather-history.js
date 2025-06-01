/**
 * Function to access historical weather data for a specific location.
 *
 * @param {Object} args - Arguments for the weather history request.
 * @param {number} args.lat - Latitude of the location.
 * @param {number} args.lon - Longitude of the location.
 * @param {number} args.start - Start time for the historical data (Unix timestamp).
 * @param {number} args.end - End time for the historical data (Unix timestamp).
 * @returns {Promise<Object>} - The historical weather data for the specified location.
 */
const executeFunction = async ({ lat, lon, start, end }) => {
  const baseUrl = 'http://api.openweathermap.org/data/2.5/history/city';
  const apiKey = process.env.OPENWEATHERMAP_API_KEY;
  try {
    // Construct the URL with query parameters
    const url = new URL(baseUrl);
    url.searchParams.append('lat', lat);
    url.searchParams.append('lon', lon);
    url.searchParams.append('type', 'hour');
    url.searchParams.append('start', start);
    url.searchParams.append('end', end);
    url.searchParams.append('appid', apiKey);

    // Perform the fetch request
    const response = await fetch(url.toString(), {
      method: 'GET'
    });

    // Check if the response was successful
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData);
    }

    // Parse and return the response data
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error accessing historical weather data:', error);
    return { error: 'An error occurred while accessing historical weather data.' };
  }
};

/**
 * Tool configuration for accessing historical weather data.
 * @type {Object}
 */
const apiTool = {
  function: executeFunction,
  definition: {
    type: 'function',
    function: {
      name: 'get_weather_history',
      description: 'Access historical weather data for a specific location.',
      parameters: {
        type: 'object',
        properties: {
          lat: {
            type: 'number',
            description: 'Latitude of the location.'
          },
          lon: {
            type: 'number',
            description: 'Longitude of the location.'
          },
          start: {
            type: 'number',
            description: 'Start time for the historical data (Unix timestamp).'
          },
          end: {
            type: 'number',
            description: 'End time for the historical data (Unix timestamp).'
          }
        },
        required: ['lat', 'lon', 'start', 'end']
      }
    }
  }
};

export { apiTool };