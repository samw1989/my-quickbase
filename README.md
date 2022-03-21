## my-quickbase

---

A simple means to interact with Quickbase databases, making use of Quickbase's [RESTful API](http://www.quickbase.com/api-guide/index.html).


### Requirements

- pytest
- requests
- python-decouple

### Installation

`pip install my-quickbase`

### Usage

#### Backup All Tables

The complete_backup method will produce a folder of JSON backups for every report in every table, where the report name contains the string 'BACKUP'

For example:

![](https://i.imgur.com/5razIAb.png)

To commence the backup:

```
import my_quickbase as mq

query = mq.AppQuery(app_id='xxxxxx', 
                    realm='myrealm.quickbase.com', 
                    token='QB-USER-TOKEN xxxxxxx')

query.complete_backup()

```

**Note:** _The realm and token parameters can be optional if variables Q_REALM and Q_USER_TOKEN are added to the
environment variables or added to a settings.ini file._

#### Acquire Iterable of Records for a Single Report

Returns a generator expression comprising an iterable of other generator objects, each representing an API call. 
The actual calls are only made when something is done with the data (e.g. converting to list, exporting to JSON).



```import my_quickbase as mq

query = mq.RecordsQuery(app_id='xxxxxx', 
                    table_id='xxxxx'
                    realm='myrealm.quickbase.com', 
                    token='QB-USER-TOKEN xxxxxxx')

# This must be called first
query.get_field_mapping()

# Returns a generator expression, which can be converted:
query.get_records(report_id='12345')

# e.g. Convert to List:
records_lst = list(query.get_records(report_id='12345'))
```

#### Insert or Update Records

Inserting or updating a record relies on the RecordQuery and its upsert_data() method. 

This method requires a list of dictionaries, with each dictionary creating/updating a single record.
MyQuickbase then converts this input list into the format required by Quickbase's API.

Each of these dictionaries used as an input parameter to the upsert_data() method must contain a mapping of field IDs 
numbers to a value. For example:

```   
data = [
            {
              "5": 'fish',  # Text
              "11": 100,  # Numeric-Currency
              "3": 1420  # Record ID #
             },
             {
              "5": 'fosh',
              "11": '$540',
              "3": 1421
             },
        ]
```

The maximum payload size is 10mb. You may need to divide data into chunks, if upserting a particular large amount.

Formatting of data values is explained in Quickbase API docs here: https://developer.quickbase.com/fieldInfo

Example use:

```
query = mq.RecordsQuery(app_id='xxxxxx', 
                        table_id='xxxxx'
                        realm='myrealm.quickbase.com', 
                        token='QB-USER-TOKEN xxxxxxx')
query.get_field_mapping()

data_insert = [ 
            {
                 "6": "bish",
                 "7": 800
            },
            {
                "6": "bosh",
                "7": 3500
            }
        ]
        
response = query.upsert_data(data_insert)  # Returns requests response, 
                                           # including details of which records updated/inserted/failed


```

To update an existing record, simply include the record ID field ID as a key to each dictionary, 
along with the record ID value. 

e.g, if Record ID field ID is 3, and ID of record to be updated is 10:

```
data_update = [ 
                {
                     "6": "moose",
                     "7": 340.
                     "3": 10
                }
               ]

response = query.upsert_data(data_update)

```
