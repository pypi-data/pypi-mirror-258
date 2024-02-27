#### v0.0.8
- NEW: New optional parameter `chat_history` in the `.query()` method. It allows to add previous exchange with the LLM to the new query. Chat History must follow the ChatMessages format (dict containing: content, role, name, meta), see https://docs.haystack.deepset.ai/v2.0/docs/data-classes#chatmessage
- Compatible with `haystack-api` v0.0.4

#### v0.0.7
- New response Schema for the Haystack-API after version bump and removal of LiteLLM.

#### v0.0.6
- Added the new parameter `return_content` to the `list_docs` method. The method `list_docs` now by default doesn't return document content (to save on bandwidth). Set `return_content` to `True` to return the content of the documents.  

#### v0.0.5
- Initial Release. Compatible with `haystack-api` v0.0.1