#### v0.0.7
- New response Schema for the Haystack-API after version bump and removal of LiteLLM.

#### v0.0.6
- Added the new parameter `return_content` to the `list_docs` method. The method `list_docs` now by default doesn't return document content (to save on bandwidth). Set `return_content` to `True` to return the content of the documents.  

#### v0.0.5
- Initial Release. Compatible with `haystack-api` v0.0.1