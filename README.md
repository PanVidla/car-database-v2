# PanVidla's Definitive Car Database
This is a database serving to collect and keep track of cars I've owned and driven in video games.

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

## v1.0.0.1.0
### General
* ADD: Add display of metadata to all the objects that support it.
* ADD: Add a list of actively played games to the top menu, so one can get to their overview.
* ~~CHANGE: Make the general information about a Car display in only two columns.~~
* CHANGE: Re-make the engine selection when adding a Car to not have the redundant Skip button.
* CHANGE: Make the redirect towards the specific kind of engine after deleting a text, not to the overview.
* CHANGE: Visually separate the Part details with headings to make it less cluttered.
* CHANGE: Replace the text block with an insertable HTML snippet.
* ~~CHANGE: Remove unnecessary columns from the Car overview.~~
* FIX: Entities that can be deleted using the is_deleted attribute shouldn't be visible anywhere.
* FIX: Entities that can be deleted using the is_deleted should not be included in counts.
* FIX: Create a get method for the official name of an engine.
* FIX: Remove the unit from the forced induction boost pressure column.
* FIX: Make the dropdown menus appear above the nav, not under.
* FIX: Engines are displaying incorrectly in the Company view.
* FIX: Make text in views appear in order.
* FIX: It should be possible to add an instance with no specialization.
* FIX: Assists should be pre-selected when creating an instance.
* ~~FIX: Drivetrain and engine layout are not being assigned correctly.~~

## v1.1.0.0.0
* ADD: Add the ability to upload images to all the entities that support it.
* ADD: Add the ability to add NFS3 instances.
* ADD: Color the background of an instance view with the color provided in the Instance detail.
* CHANGE: Consolidate the many buttons in the Car detail view into a concise nav bar.
* CHANGE: If a Car is fictional, make its row in the overview colored to signify that.
