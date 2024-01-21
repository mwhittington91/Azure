#https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart/v11/azure-search-quickstart.ipynb

import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient 
from azure.search.documents import SearchClient
from azure.search.documents.indexes.models import (
    ComplexField,
    CorsOptions,
    SearchIndex,
    ScoringProfile,
    SearchFieldDataType,
    SimpleField,
    SearchableField
)
from dotenv import load_dotenv
load_dotenv()


# Set the service endpoint and API key from the environment

service_name = os.environ["SEARCH-SERVICE-NAME"]
admin_key = os.environ["SEARCH-SERVICE-ADMIN-API-KEY"]

index_name = "hotels-quickstart"

# Create an SDK client
endpoint = "https://{}.search.windows.net/".format(service_name)
admin_client = SearchIndexClient(endpoint=endpoint,
                      index_name=index_name,
                      credential=AzureKeyCredential(admin_key))

search_client = SearchClient(endpoint=endpoint,
                      index_name=index_name,
                      credential=AzureKeyCredential(admin_key))

# Specify the index schema
name = index_name
fields = [
        SimpleField(name="HotelId", type=SearchFieldDataType.String, key=True),
        SearchableField(name="HotelName", type=SearchFieldDataType.String, sortable=True),
        SearchableField(name="Description", type=SearchFieldDataType.String, analyzer_name="en.lucene"),
        SearchableField(name="Description_fr", type=SearchFieldDataType.String, analyzer_name="fr.lucene"),
        SearchableField(name="Category", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
    
        SearchableField(name="Tags", collection=True, type=SearchFieldDataType.String, facetable=True, filterable=True),

        SimpleField(name="ParkingIncluded", type=SearchFieldDataType.Boolean, facetable=True, filterable=True, sortable=True),
        SimpleField(name="LastRenovationDate", type=SearchFieldDataType.DateTimeOffset, facetable=True, filterable=True, sortable=True),
        SimpleField(name="Rating", type=SearchFieldDataType.Double, facetable=True, filterable=True, sortable=True),

        ComplexField(name="Address", fields=[
            SearchableField(name="StreetAddress", type=SearchFieldDataType.String),
            SearchableField(name="City", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
            SearchableField(name="StateProvince", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
            SearchableField(name="PostalCode", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
            SearchableField(name="Country", type=SearchFieldDataType.String, facetable=True, filterable=True, sortable=True),
        ])
    ]
cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
scoring_profiles = []
suggester = [{'name': 'sg', 'source_fields': ['Tags', 'Address/City', 'Address/Country']}]

# index = SearchIndex(
#     name=name,
#     fields=fields,
#     scoring_profiles=scoring_profiles,
#     suggesters = suggester,
#     cors_options=cors_options)

# try:
#     result = admin_client.create_index(index)
#     print ('Index', result.name, 'created')
# except Exception as ex:
#     print (ex)

# Add documents

# documents = [
#     {
#     "@search.action": "upload",
#     "HotelId": "1",
#     "HotelName": "Secret Point Motel",
#     "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
#     "Description_fr": "L'hôtel est idéalement situé sur la principale artère commerciale de la ville en plein cœur de New York. A quelques minutes se trouve la place du temps et le centre historique de la ville, ainsi que d'autres lieux d'intérêt qui font de New York l'une des villes les plus attractives et cosmopolites de l'Amérique.",
#     "Category": "Boutique",
#     "Tags": [ "pool", "air conditioning", "concierge" ],
#     "ParkingIncluded": "false",
#     "LastRenovationDate": "1970-01-18T00:00:00Z",
#     "Rating": 3.60,
#     "Address": {
#         "StreetAddress": "677 5th Ave",
#         "City": "New York",
#         "StateProvince": "NY",
#         "PostalCode": "10022",
#         "Country": "USA"
#         }
#     },
#     {
#     "@search.action": "upload",
#     "HotelId": "2",
#     "HotelName": "Twin Dome Motel",
#     "Description": "The hotel is situated in a  nineteenth century plaza, which has been expanded and renovated to the highest architectural standards to create a modern, functional and first-class hotel in which art and unique historical elements coexist with the most modern comforts.",
#     "Description_fr": "L'hôtel est situé dans une place du XIXe siècle, qui a été agrandie et rénovée aux plus hautes normes architecturales pour créer un hôtel moderne, fonctionnel et de première classe dans lequel l'art et les éléments historiques uniques coexistent avec le confort le plus moderne.",
#     "Category": "Boutique",
#     "Tags": [ "pool", "free wifi", "concierge" ],
#     "ParkingIncluded": "false",
#     "LastRenovationDate": "1979-02-18T00:00:00Z",
#     "Rating": 3.60,
#     "Address": {
#         "StreetAddress": "140 University Town Center Dr",
#         "City": "Sarasota",
#         "StateProvince": "FL",
#         "PostalCode": "34243",
#         "Country": "USA"
#         }
#     },
#     {
#     "@search.action": "upload",
#     "HotelId": "3",
#     "HotelName": "Triple Landscape Hotel",
#     "Description": "The Hotel stands out for its gastronomic excellence under the management of William Dough, who advises on and oversees all of the Hotel's restaurant services.",
#     "Description_fr": "L'hôtel est situé dans une place du XIXe siècle, qui a été agrandie et rénovée aux plus hautes normes architecturales pour créer un hôtel moderne, fonctionnel et de première classe dans lequel l'art et les éléments historiques uniques coexistent avec le confort le plus moderne.",
#     "Category": "Resort and Spa",
#     "Tags": [ "air conditioning", "bar", "continental breakfast" ],
#     "ParkingIncluded": "true",
#     "LastRenovationDate": "2015-09-20T00:00:00Z",
#     "Rating": 4.80,
#     "Address": {
#         "StreetAddress": "3393 Peachtree Rd",
#         "City": "Atlanta",
#         "StateProvince": "GA",
#         "PostalCode": "30326",
#         "Country": "USA"
#         }
#     },
#     {
#     "@search.action": "upload",
#     "HotelId": "4",
#     "HotelName": "Sublime Cliff Hotel",
#     "Description": "Sublime Cliff Hotel is located in the heart of the historic center of Sublime in an extremely vibrant and lively area within short walking distance to the sites and landmarks of the city and is surrounded by the extraordinary beauty of churches, buildings, shops and monuments. Sublime Cliff is part of a lovingly restored 1800 palace.",
#     "Description_fr": "Le sublime Cliff Hotel est situé au coeur du centre historique de sublime dans un quartier extrêmement animé et vivant, à courte distance de marche des sites et monuments de la ville et est entouré par l'extraordinaire beauté des églises, des bâtiments, des commerces et Monuments. Sublime Cliff fait partie d'un Palace 1800 restauré avec amour.",
#     "Category": "Boutique",
#     "Tags": [ "concierge", "view", "24-hour front desk service" ],
#     "ParkingIncluded": "true",
#     "LastRenovationDate": "1960-02-06T00:00:00Z",
#     "Rating": 4.60,
#     "Address": {
#         "StreetAddress": "7400 San Pedro Ave",
#         "City": "San Antonio",
#         "StateProvince": "TX",
#         "PostalCode": "78216",
#         "Country": "USA"
#         }
#     }
# ]

# try:
#     result = search_client.upload_documents(documents=documents)
#     print("Upload of new document succeeded: {}".format(result[0].succeeded))
# except Exception as ex:
#     print (ex.message)

results =  search_client.search(search_text="*", include_total_count=True)

print ('Total Documents Matching Query:', results.get_count())
for result in results:
    print("{}: {}".format(result["HotelId"], result["HotelName"]))

results =  search_client.search(search_text="wifi", include_total_count=True, select='HotelId,HotelName,Tags')

print ('Total Documents Matching Query:', results.get_count())
for result in results:
    print("{}: {}: {}".format(result["HotelId"], result["HotelName"], result["Tags"]))
