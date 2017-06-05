## Project Log

#### 6.3.2017 Saturday
* VRBO scrape strategy: moving the map (with dynamic search enabled) shows a URL in Network with a JSON response that specifies everything on the google map displayed on VRBO.  I systematically changed parameters in this URL string to get the desired JSONs.
* Final VRBO scrape was based on sorting properties by distance from downtown on VRBO, manually going through the results pages until results land outside of Denver (i.e. Thornton, Littleton), and then iterating through the same pages (just increment page number!) with the scraper.

#### 6.5.2017 Monday
* Opted to use googlemaps API for geocoding/reverse geocoding to ensure consistency.  Using Place ID for comparisons should work better than lat/lon.
* Noted duplicate googlemaps place IDs in the VRBO and Homeaway data.  This may require chronological data to resolve.  For now, I'm keeping the duplicates -- better chance of matching a description to AirBNB, and it's possible that different units in a condo would have the same gmaps ID.
* Dropped non-unique property IDs from VRBO/Homeaway data.
