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



