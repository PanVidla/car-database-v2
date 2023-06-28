# PanVidla's Definitive Car Database
This is a database serving to collect and keep track of cars I've owned and driven in video games.

## Backlog
### General
* ADD: Add the option to add and delete thumbnails for Cars and Instances.
* ADD: Add the option to add and delete regular pictures to Company and Competition objects.
* ADD: Add the option to hard delete Cars, Games and Instances.
* ~~ADD: Make it possible to add more than one condition to a rule.~~

## v1.3.0.0.0
### General
* ADD: Add pagination on long tables.
* ADD: Add the ability to change the order of EventType objects without having to rewrite them all one by one.
* ADD: Add the option to copy EventType objects.
* ADD: Add a dropdown menu to the Events button that will take the user to the events for a specific game.
* CHANGE: Make the buttons for editing and deleting of game activities appear in a modal.
* CHANGE: Make different tables in the Relationships section of a detail view appear in tabs, not all at once.

### Need for Speed III: Hot Pursuit
* ADD: Game statistics on the Instance overview screen OR a separate statistics screen.

### Need for Speed: Road Challenge
* ADD: Game statistics on the Instance overview screen OR a separate statistics screen.

### Forza Horizon 4
* ADD: Add the option to add, edit, delete and view FH4 instances, events, series of events etc.
* ADD: Make it possible to import FH4 event records from a CSV file.

## v1.2.0.0.0
### General
* CHECK: Merge all the new DB migrations into one file and add them to Git.
* ~~ADD: Add the option to select own color for instance types and specializations.~~
* ~~ADD: Add selection of currently active Instance.~~
* ~~ADD: Add counting of sessions.~~
* ~~ADD: Add the possibility of defining custom rules for events.~~
* CHANGE: Add the option to delete logos easily.
* CHANGE: Make sure related entities (text, images...) get deleted on deletion of objects.
* CHANGE: Make sure datetime_edited changes when deleting related objects on entities that have it.
* CHANGE: Remove the Developer, Car manufacturer and Part manufacturer columns from specialized Company overviews.
* CHANGE: Consolidate the button coloring and grouping in the remaining detail views.
* CHANGE: Remove irrelevant columns from tables in detail views.
* CHANGE: The "Add instance" button in a Game-specific Instance overview should lead to creation of a car for the game in question.
* CHANGE: Make prototypes / concept cars also colored a different way, like fictional cars.
* FIX: Prevent cars from copying text and images twice when making a second copy of one car.
* FIX: Wins should also be counted as "podiums".
* FIX: Assists are still not copying over to the Instance from Car when creating it.
* FIX: Last played datetime updated for an Instance should also update the last played datetime for its Game.
* FIX: The app crashes when trying to create an engine with an undefined no. of valves per cylinder.

### Need for Speed III: Hot Pursuit
* ADD: Add the option to add text and images to NFS3 events and tracks.
* FIX: Add missing color formatting to Event and Track overviews.
* FIX: Make sure the no. of lap and track records is counted correctly (it's probably happening because when updating an event record, the record is not registered as a record a second time, as it's compared to the same value).

### Need for Speed: Road Challenge
* ADD: The ability to add, edit, delete and view NFS4 instances, events, tracks etc.
* FIX: The NFS4 instance doesn't need the is_pursuit attribute!

## v1.1.0.0.0
### General
* ~~ADD: Add the ability to upload and delete images to all the entities that support it.~~
* ~~ADD: Color the background of an instance view with the color provided in the Instance detail.~~
* ~~ADD: Add the ability to copy selected instances (Car, Engine).~~
* ~~ADD: Make sure no duplicit entries can be added.~~
* ~~ADD: Make the parsing of added text such that it's possible to add several paragraphs at a time.~~
* ~~CHANGE: Consolidate the many buttons in the Car detail view into a concise nav bar.~~
* ~~CHANGE: If a Car is fictional, make its row in the overview colored to signify that.~~
* ~~CHANGE: Unify the format of datetime display in overviews and detail views.~~
* ~~CHANGE: Move the Instance dropdown generation to a separate HTML snippet.~~
* ~~CHANGE: Refactor the names of Car forms to make more sense.~~
* ~~CHANGE: Remove the "non-electric" fuel types from selection when creating an electric engine and vice versa.~~
* ~~CHANGE: Make everything possible in detail views clickable.~~
* ~~CHANGE: Remove unnecessary decimal points where not needed.~~
* ~~CHANGE: Break up the detail view of Company with headings so it feels less cluttered.~~
* ~~FIX: The GameSeries of a game cannot seem to be changed additionally.~~
* ~~FIX: Add formatting, proper strings and coloring to the Instance and game-specific overviews.~~

### Crazy Taxi
* ~~FIX: The formatting and buttons in the Crazy Taxi overview are broken.~~

### Need for Speed III: Hot Pursuit
* ~~ADD: The ability to add, edit, delete and view NFS3 instances.~~
* ~~ADD: The ability to add, edit, delete and view events, event records, tracks and track records.~~
* ~~ADD: Color and number formatting of all NFS3 views.~~

## v1.0.0.1.0
### General
* ~~ADD: Add display of metadata to all the objects that support it.~~
* ~~ADD: Add a list of actively played games to the top menu, so one can get to their overview.~~
* ~~ADD: Display flashed messages with categories.~~
* ~~CHANGE: Make the general information about a Car display in only two columns.~~
* ~~CHANGE: Re-make the engine selection when adding a Car to not have the redundant Skip button.~~
* ~~CHANGE: Make the redirect towards the specific kind of engine after deleting a text, not to the overview.~~
* ~~CHANGE: Visually separate the Part details with headings to make it less cluttered.~~
* ~~CHANGE: Replace the text block with an insertable HTML snippet.~~
* ~~CHANGE: Remove unnecessary columns from the Car overview.~~
* ~~FIX: Entities that can be deleted using the is_deleted attribute shouldn't be visible anywhere.~~
* ~~FIX: Entities that can be deleted using the is_deleted should not be included in counts.~~
* ~~FIX: Create a get method for the official name of an engine.~~
* ~~FIX: Remove the unit from the forced induction boost pressure column.~~
* ~~FIX: Make the dropdown menus appear above the nav, not under. (x)~~
* ~~FIX: Engines are displaying incorrectly in the Company view.~~
* ~~FIX: Make text in views appear in order.~~
* ~~FIX: It should be possible to add an instance with no specialization.~~
* ~~FIX: Assists should be pre-selected when creating an instance. (x)~~
* ~~FIX: Drivetrain and engine layout are not being assigned correctly.~~

## v1.0.0.0.0
### General
* ~~The ability to add, edit, delete and view all instances of objects defined in the general model.~~
  * ~~All views should have relevant tables of objects that they are in relationship with.~~
  * ~~All add methods with multiple steps should have their progress bars set correctly.~~
  * ~~All attributes of all objects should be protected from invalid data.~~
  * ~~All delete methods should delete relevant entries of related type and should be safe to use.~~
  * ~~Make the number of instances display correctly.~~
* ~~The ability to add, delete and view text and images for the objects which their definition allows it for.~~
* ~~User login for security purposes.~~

### Crazy Taxi
* ~~The ability to add, edit, delete and view instances for Crazy Taxi.~~
