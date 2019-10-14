# Database Schema

## `Talk` Table

|Field|Description|
|---|---|
|`id`|Iternal identifier
|`title`|
|`description`|Talk abstract from website
|`presenters`|
|`transcript`|Full talk transcript extracted from YouTube closed captioning
|`created`|Metadata
|`modified`|Metadata

Not sure if we want to include full_text there. Probably need to figure out how things flow

## `Vote` Table

|Field|Description|
|---|---|
|`id`|Iternal identifier
|`talk_id`|Foreign Key in `Talk` table
|`user_id`|Account that cast vote
|`value`|Recorded vote
|`created`|Metadata
|`modified`|Metadata

## `User` Table

|Field|Description|
|---|---|
|`id`|Internal identifier

Joe, this is all you :D
