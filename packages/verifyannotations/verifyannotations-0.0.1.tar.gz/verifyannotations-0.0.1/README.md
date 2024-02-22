#### Example usage

```
from verifyannotations import VerifyDataAnnotations

label_folder = "/path/to/labels"  # path to your annotations directory
image_folder = "/path/to/images"  # path to your images directory
result_folder = "/path/to/output"  # where to save the results
image_names_path = "/path/to/image_name_list.txt"  # where to save the image names
class_path = "/path/to/classes.txt"  # a text file containing the classes in your annotations. one class per one line

verifier = VerifyDataAnnotations(
    label_folder,
    image_folder,
    result_folder,
    image_names_path,
    class_path,
)
verifier.run_verification()

```