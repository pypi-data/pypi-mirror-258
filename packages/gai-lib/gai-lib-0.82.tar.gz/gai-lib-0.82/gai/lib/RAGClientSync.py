import os
import requests
import json
from gai.common.utils import get_lib_config
from fastapi import WebSocketDisconnect
from gai.common.http_utils import http_post, http_post_async, http_delete,http_get,http_delete_async
from gai.common.logging import getLogger
from gai.common.errors import ApiException
logger = getLogger(__name__)
import asyncio
from gai.lib.ClientBase import ClientBase

class RAGClientBase(ClientBase):
    
    def __init__(self,config_path=None):
        super().__init__(config_path)
        self.base_url = os.path.join(
            self.config["gai_url"], 
            self.config["generators"]["rag"]["url"].lstrip('/'))
        logger.debug(f'base_url={self.base_url}')

    def _prepare_files_and_metadata(self, collection_name, file_path, metadata):
        mode = 'rb' if file_path.endswith('.pdf') else 'r'
        with open(file_path, mode) as f:
            files = {
                "file": (os.path.basename(file_path), f if mode == 'rb' else f.read(), "application/pdf"),
                "metadata": (None, json.dumps(metadata), "application/json"),
                "collection_name": (None, collection_name, "text/plain")
            }
            return files

class RAGClientSync(RAGClientBase):

    def __init__(self,config_path=None):
        super().__init__(config_path)

### ----------------- INDEXING ----------------- ###

    # synchronous version of index_file_async
    def index_file(self, 
        collection_name, 
        file_path, 
        title="",
        source="",
        authors="",
        publisher="",
        published_date="",
        comments="",
        keywords="", 
        progress_updater=None):
        url = os.path.join(self.base_url,"index-file")
        metadata = {
            "title": title,
            "source": source,
            "authors": authors,
            "publisher": publisher,
            "published_date": published_date,
            "comments": comments,
            "keywords": keywords
        }

        # We will assume file ending with *.pdf to be PDF but this check should be done before the call.
        mode = 'rb' if file_path.endswith('.pdf') else 'r'
        with open(file_path, mode) as f:
            files = {
                "file": (os.path.basename(file_path), f.read(), "application/pdf"),
                "metadata": (None, json.dumps(metadata), "application/json"),
                "collection_name": (None, collection_name, "text/plain")
            }
            response = http_post(url=url, files=files)

        # Callback for progress update (returns a number between 0 and 100)
        if progress_updater:
            # Exception should not disrupt the indexing process
            try:
                # progress = int((i + 1) / len(chunks) * 100)
                progress = 100
                t = asyncio.create_task(progress_updater(progress))
                asyncio.get_event_loop().run_until_complete(t)
                logger.debug(
                    f"RAGClient: progress={progress}")
                # await send_progress(websocket, progress)
            except WebSocketDisconnect as e:
                if e.code == 1000:
                    # Normal closure, perhaps log it as info and continue gracefully
                    logger.info(
                        f"RAGClient: WebSocket closed normally with code {e.code}")
                    pass
                else:
                    # Handle other codes as actual errors
                    logger.error(
                        f"RAGClient: WebSocket disconnected with error code {e.code}")
                    pass
            except Exception as e:
                logger.error(
                    f"RetrievalGeneration.index_async: Update websocket progress failed. Error={str(e)}")
                pass
        
        # {document_id: "document_id"}
        return json.loads(response.text)

    def retrieve(self, collection_name, query_texts, n_results=None):
        url = os.path.join(self.base_url,"retrieve")
        data = {
            "collection_name": collection_name,
            "query_texts": query_texts
        }
        if n_results:
            data["n_results"] = n_results

        response = http_post(url, data=data)
        return response

    # Database Management

    def delete_collection(self, collection_name):
        url = os.path.join(self.base_url,"collection",collection_name)
        logger.info(f"RAGClient.delete_collection: Deleting collection {url}")
        try:
            response = http_delete(url)
        except ApiException as e:
            if e.code == 'collection_not_found':
                return {"count":0}
            logger.error(e)
            raise e
        return json.loads(response.text)

    def list_collections(self):
        url = os.path.join(self.base_url,"collections")
        response = http_get(url)
        return json.loads(response.text)

    def list_documents(self,collection_name):
        url = os.path.join(self.base_url,"collection",collection_name)
        response = http_get(url)
        return json.loads(response.text)
    
    def get_document(self,doc_id):
        url = os.path.join(self.base_url,"document",doc_id)
        response = http_get(url)
        return json.loads(response.text)

    def delete_document(self,doc_id):
        url = os.path.join(self.base_url,"document",doc_id)
        response = http_delete(url)
        return json.loads(response.text)


    def exists(self,collection_name, file_path):
        url = os.path.join(self.base_url,f"collection/{collection_name}/document_exists")
        with open(file_path, "r") as f:
            text = f.read()        
        files = {
            "file": (file_path, text, "text/plain"),
            "collection_name": (None, collection_name, "text/plain")
        }        
        response = http_post(url, files=files)
        return json.loads(response.text)