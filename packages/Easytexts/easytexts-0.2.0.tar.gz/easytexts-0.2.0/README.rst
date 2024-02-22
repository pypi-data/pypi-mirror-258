EasyText: A Simple File Handler for Python


Install EasyText using pip:

	pip install easytext

Usage:

Import the EasyText module:

	from easytext import *


Explore the available functions:
Writing and Appending:

append(location_and_name, text, log=False, newline=True): Appends text to a file, optionally adding a newline and logging the action.
rewrite(location_and_name, text, log=False): Overwrites the entire content of a file with new text, optionally logging the action.
create_if_doesnt_exist(location_and_name, text, log=False): Creates a new file and writes text to it, handling existing files gracefully, optionally logging the action.
Reading:

read(location_and_name, log=False): Reads the entire content of a file and returns it as a string, optionally logging the action.
Clearing and Checking:

clear(location_and_name, log=False): Empties the content of a file, optionally logging the action.
is_clear(location_and_name, log=False): Checks if a file is empty, returning True if empty, False otherwise, optionally logging the result.
Deleting:

delete(location_and_name): Deletes a file.
Checking Existence:

does_exist(location_and_name): Checks if a file exists, returning True if exists, False otherwise.
Examples

See the following examples for how to use EasyText:

[Write and append to a file][example_write_append]
[Rewrite the content of a file][example_rewrite]
[Create a new file][example_create]
[Read the contents of a file][example_read]
[Clear a file][example_clear]
[Check if a file is empty][example_is_clear]
[Delete a file][example_delete]
[Check if a file exists][example_does_exist]



Disclaimer

While EasyText handles common errors and is suitable for learning and small projects, it's not intended for critical or demanding projects due to its limited scope and testing.


Additional Notes

The log parameter allows you to control if certain actions are logged for debugging or tracking purposes.
The newline parameter in append allows you to control whether a newline character is added before the appended text.