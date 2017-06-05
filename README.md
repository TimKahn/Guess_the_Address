## Address Prediction for AirDNA

#### Overview:
AirDNA has a robust model for predicting the AirBNB revenue potential of a property based on AirBNB rates/occupancy at comparable properties nearby.  As they expand into automated property valuation -- how much is a property actually worth, given its AirBNB revenue potential? -- they need address-specific information for AirBNB rentals in order to compare directly with market data, like MLS listings.

#### Challenge / Goal:
AirBNB publishes a good deal of information in its listings, but not the address -- you only get an address when you book a stay.  Maps on the AirBNB website show the general vicinity of the property as a circle, not as a point; the actual location of the property is randomized within the circle.  My goal is to 'predict' the addresses by comparing features of AirBNB listings to other data (e.g., from county recorder & tax assessor records), and provide a confidence measure for those predictions.

#### Data:
* AirDNA's 'proprietary' data for Denver, scraped from AirBNB listings.
* Similar data scraped from a competing service (Homeaway, VRBO) that includes reliable latitude/longitude.
* County recorder data
* Tax assessor data

**Possible obstacle:**  
One fundamental challenge is creating labeled training & test data.  The hope is that we can get labels by comparing AirBNB listings to other platforms' listings (Homeaway, VRBO) that reveal latitude/longitude.  Only listings with very close matches (on host name, description, etc.) will be used as training / test data, since this is actually a prediction too!  We believe that there is enough redundancy in listings across platforms for this to work.

#### Ideas / methods:
* Attempt to tackle each zip code independently.  Could be problematic for training, as classes will be severely imbalanced: matches may represent less than 1% of the available training data.
* For each property within a given radius (400m?) of a property with a known address, create a training point by comparing to the known property.  This will generate one 'match' training point and many 'non-match' training points.
* Use logistic regression, SVMs, random forest, or boosting to classify correct matches (positive) vs. bad matches (negative).  Features could be boolean or differences:
```
"AirBNB Host Name == First Name on Deed"
"AirBNB data shows swimming pool == Assessor data shows swimming pool"
"Bedrooms on AirBNB listing - Bedrooms in Assessor Data"
```

* Extra credit: Bayesian methods.  If we correctly classify some portion of the properties in a zip code, is our posterior probability of classifying the remaining properties greater than the prior?
* Extra credit: Extracting street numbers from images using a CNN.

#### Presentation:
MVP is a slide presentation and/or poster.  If time and results allow, a web app with a visualization of the model in a given zip code would be awesome.

## Resources and References:

#### Predicting address from property features/description
* None found yet...

#### Scraping:
* https://ianlondon.github.io/blog/web-scraping-discovering-hidden-apis/
* http://www.verginer.eu/blog/web-scraping-airbnb/
* https://github.com/tomslee/airbnb-data-collection

#### AirBNB-related news:
* https://motherboard.vice.com/en_us/article/airbnbs-in-a-hot-legal-mess-with-new-york-and-its-not-going-away
