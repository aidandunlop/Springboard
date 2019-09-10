# API Documentation

## Authentication

Need to figure out

## Talks

### **GET** `/api/v1/talks/`

Returns paginated list of talks

#### Sample Response

```json
{
    "message": "Description of what happened",
    "data": [
        {
            "id": 1,
            "title": "Modern Python Dictionaries -- A confluence of a dozen great ideas",
            "description": "Python's dictionaries are stunningly good. Over the years, many great ideas have combined together to produce the modern implementation in Python 3.6. This fun talk uses pictures and little bits of pure python code to explain all of the key ideas and how they evolved over time. Includes newer features such as key-sharing, compaction, and versioning.",
            "presenters": "Raymond Hettinger"
        },
        {
            "id": 2,
            "title": "Passing Exceptions 101: Paradigms in Error Handling",
            "description": "Exception handling in Python can sometimes feel like a Wild West. If you have a send_email function, and the caller inputs an invalid email address, should it: A) Return None or some other special return value, B) Let the underlying exception it might cause bubble up, C) Check via a regex and type checking and raise a ValueError immediately, or D) Make a custom EmailException subclass and raise that? What if there is a network error while the email was sending? Or what if the function calls a helper _format_email that returns an integer (clearly wrong!), or raises an TypeError itself? Should it crash the program or prompt a retry? This talk will introduce the concept of an exception, explain the built-in Python exception hierarchy and the utility of custom subclasses, demonstrate try/except/finally/else syntax, and then explore different design patterns for exception control flow and their tradeoffs using examples. It will also make comparisons to error handling philosophy in other languages, like Eiffel and Go.",
            "presenters": "Amandine Lee"
        },
        {
            "id": 3,
            "title": "Python in The Serverless Era",
            "description": "Serverless is the latest phase in the evolution of cloud development. Its building blocks are functions, a bunch of stateless “nano-services”, that can scale automatically and charged only when used. It enables teams to focus more on development while having fully managed servers. In this talk I'll cover the Serverless Architectures practices, use cases, tooling and the role python plays in it.",
            "presenters": "Benny Bauer"
        }
    ]
}
```

### **GET** `/api/v1/talks/<talk_id:int>/`

Returns single talk details

#### Status Codes

|Code|Description|
|---|---|
|200|Success|
|404|`talk_id` is not in database|

#### Sample Response

```json
{
    "message": "Description of what happened",
    "data": {
        "id": 1,
        "title": "Modern Python Dictionaries -- A confluence of a dozen great ideas",
        "description": "Python's dictionaries are stunningly good. Over the years, many great ideas have combined together to produce the modern implementation in Python 3.6. This fun talk uses pictures and little bits of pure python code to explain all of the key ideas and how they evolved over time. Includes newer features such as key-sharing, compaction, and versioning.",
        "presenters": "Raymond Hettinger"
    }
}
```

### **GET** `/api/v1/talks/random/`

Returns random talk that user has not voted on

#### Sample Response

```json
{
    "message": "Description of what happened",
    "data": {
        "id": 2,
        "title": "Passing Exceptions 101: Paradigms in Error Handling",
        "description": "Exception handling in Python can sometimes feel like a Wild West. If you have a send_email function, and the caller inputs an invalid email address, should it: A) Return None or some other special return value, B) Let the underlying exception it might cause bubble up, C) Check via a regex and type checking and raise a ValueError immediately, or D) Make a custom EmailException subclass and raise that? What if there is a network error while the email was sending? Or what if the function calls a helper _format_email that returns an integer (clearly wrong!), or raises an TypeError itself? Should it crash the program or prompt a retry? This talk will introduce the concept of an exception, explain the built-in Python exception hierarchy and the utility of custom subclasses, demonstrate try/except/finally/else syntax, and then explore different design patterns for exception control flow and their tradeoffs using examples. It will also make comparisons to error handling philosophy in other languages, like Eiffel and Go.",
        "presenters": "Amandine Lee"
    }
}
```

### **POST** `/api/v1/talks/<talk_id:int>/vote/`

Cast vote for `talk_id`

#### TODO

- [ ] Figure out how to overwrite previous votes in the UI and how we are handling in the backend / data part
- [ ] What do votes represent? Like / Dislike makes the most sense, but we don't want to bring negativity to the community

#### Request Body

```json
{
    "vote": "in_person | watch_later"
}
```

#### Status Code

|Code|Description|
|---|---|
|200|Success|
|404|`talk_id` is not in database|

#### Response Body

```json
{
    "message": "Description of what happened"
}
```


### **POST** `/api/v1/predict/`

Returns the predicted list of `talk_id`s and takes the following inputs

- User id from session
- should pass to backend {`user_id`, `labeled_talk_ids`} where `labeled_talk_ids` is a list of `talk_id`s which the user has labeled `in_person` 


#### Request Body
```json
{
  "user_id": 1,
  "labeled_talk_ids": [
    3,
    4,
    5,
    9,
    11,
    16,
    17,
    19,
    20,
    21,
    22,
    27,
    33,
    35,
    39,
    43,
    44,
    45,
    46,
    48,
    49,
    50,
    51,
    53,
    57,
    60,
    61,
    67,
    70,
    73,
    77,
    78,
    81,
    82,
    84,
    85,
    86
  ]
}
```

#### Response Body

```json
{
  "message": "Description of what happened",
  "data": [
    1,
    2,
    3,
    4
  ]
}
```
