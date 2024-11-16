# Crossref Maker
"doi.py" is a Python script that helps me create a .xml file containing all of a book's metadata (XML metadata) which then can be uploaded to Crossref's web deposit site.
Note that as the Crossref structure can change over time, hence the code must be updated to.
"check.py" is another Python script which analyzes the .xml file previously made and extracts and presents its basic info back to me, it also checks for pages' errors such as overlapping or negative range. It's recommended to use it before uploading the .xml file.
