## Project Log

#### 6.3.2017 Saturday
* VRBO scrape strategy: moving the map (with dynamic search enabled) shows a URL in Network with a JSON response that specifies everything on the google map displayed on VRBO.  I systematically changed parameters in this URL string to get the desired JSONs.
* Final VRBO scrape was based on sorting properties by distance from downtown on VRBO, manually going through the results pages until results land outside of Denver (i.e. Thornton, Littleton), and then iterating through the same pages (just increment page number!) with the scraper.

#### 6.5.2017 Monday
* Opted to use googlemaps API for geocoding/reverse geocoding to ensure consistency.  Using Place ID for comparisons should work better than lat/lon.
* Noted duplicate googlemaps place IDs in the VRBO and Homeaway data.  This may require chronological data to resolve.  For now, I'm keeping the duplicates -- better chance of matching a description to AirBNB, and it's possible that different units in a condo would have the same gmaps ID.
* Dropped duplicate titles from VRBO/Homeaway data.
* Dropped duplicate titles from AirBNB data for use in text comparison.
* Note: I opted to drop titles instead of property IDs; perhaps it's possible to have multiple titles associated with a property?
* FuzzyWuzzy with simple word ratio to find and score best matches between titles on Homeaway/VRBO and AirBNB.

#### 6.6.2017 Tuesday
* Find distances between VRBO/Homeaway listings and their matched listings on AirBNB.
* Manually validate matched listings.
* Create a function that designates bounds on lat/lon for comparison to an AirBNB listing.
* Find a test zipcode.  Pull records from Attom.  Geocode via address to get gmaps lat/lon (but: how many records?)
* Pull Attom records within lat/lon bounds for a single property subject to distance being within 400m (or whatever bounds).
* Automate for all zipcodes in dataset.
* Should I only use 'entire home' listings?
* Possibility that listing is not even within 400m circle!  Example: VRBO 4105204 / AirBNB 1005908
* Consider using lat/lon differences instead of distance.
