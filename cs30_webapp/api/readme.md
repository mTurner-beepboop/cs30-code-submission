This is the instruction file for the API of the carbon emmissions web app, it should be updated 
throughout development to ensure it remains up to date with all requests the are available for use.


Since many requests may use the same form of JSON request/response, they will be defined here for simplicity.
 - Flatfile Entry
 {
 'ref_num':<int > 999> 
 'navigation_info':{
	'scope':<ONE of 'Scope 1','Scope 2','Scope 3'>
	'level_1':<string>
	'level_2':<string>
	'level_3':<string>
	'level_4':<string>
	'level_5':<string>
	}
'calculation_info':{
	'ef':<double>
	'cu':<string>
	}
'other_info':{
	'last_update':<datetime>
	'preference':<int>
	'source':<string>
 }

- Message form
{
'message':<string>
}

- Category form
{
'subcategories':<list of strings>
'id':<integer>
}

---INTERNAL---
To request the full contents of the database:
Send GET request to <host>/api/carbon
The API will return a stream of JSON documents of the flatfile entry form.

To request one specific flatfile entry:
Send GET request to <host>/api/carbon/<ref_num>
The API will return the requested entry in flatfile entry form or pass an error if not found

To add a new entry to the flatfile database:
Send POST request of flatfile form to <host>/api/carbon
This will return a HTTP response - either 201, or 400 if request was malformed

To delete all entries from the database (this is just a development tool, will likel be removed):
Send DELETE request to <host>/api/carbon
The API will return how many rows were deleted in message form, along with a HTTP response 204

To update an entry in the database:
Send PUT request of form flatfile entry to <host>/api/carbon/<ref_num>
The API will either return the same request back to signify success, or a HTTP response 400 if request was malformed

To delete single entry from database:
Send DELETE request to <host>/api/carbon/<ref_num>
The API will return if row was deleted in message form, along with HTTP response 204 if it was



---ETERNAL---
To find available scopes and levels:
For scopes, send a GET request to <host>/api/carbon/scope
The API will return a list of scopes in category form, eg {"subcategories":["Scope 1", "Scope 2"], "id":0}

To find levels, send post request to the same address with information down to the level you are looking for
eg: {"scope":"Scope 3","level1":"Food", "level2":"Meat"} would return a list of available level 3 categories for that path
The API will again return this as a list of results in category form, if there is only one entry matching the given path, the subcategories field will return empty and the id field will contain the id of the item
Note: for now null fields are denoted with "x" in the database, this will be updated later in development, but currently, a sample return for a single entry would be {"subcategories":["x"],"id":5829}
The API will als return an id number if no other entries exist at any level, this is simply because data is missing - eg sending a request of Scope 3, Food, Meat, Game, would give a return of {"subcategoreis":["birds"],"id":5829}
If the path provided does not exist, the API will return {"message":"Path not found"}


To calculate a given amount of an item:
Send POST request to <host>/api/carbon/info of the form {"id":<integer>, "amount":<integer>}
The API will return a message of the form {"result":<float>, "calc_unit":<string>, "source":<string>}
Note: if the API cannot find a matching id, will return entry not found message