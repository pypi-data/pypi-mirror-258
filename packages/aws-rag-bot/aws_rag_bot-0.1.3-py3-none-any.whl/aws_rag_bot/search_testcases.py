import unittest
from aws_opensearch_vector_database import get_opensearch_endpoint, get_embeddings_from_model, EmbeddingTypes
from langchain_openai import OpenAIEmbeddings
from langchain.embeddings.bedrock import BedrockEmbeddings

# Put test case constants specific to user here:
domain_name = "rise-gardens-kb-v2"
website_sitemap = "https://www.risegardens.com/sitemap.xml"


# Test Cases
# use unittest - https://www.dataquest.io/blog/unit-tests-python/
#https://machinelearningmastery.com/a-gentle-introduction-to-unit-testing-in-python/


# Call all in the most simple form to ensure they run
#   then consider deeper test cases for core functions (like content source functions)

# clean_documents_newlines_spaces_and_tabs
# Load a single document with junk that I can validate, then clean it and validate it

# get_opensearch_endpoint
# Single test
class TestOpenSearchVectorDBLoader(unittest.TestCase):
    def test_get_opensearch_endpoint(self):
        endpoint = get_opensearch_endpoint(domain_name=domain_name)
        self.assertIn("amazonaws.com", endpoint)

    def test_get_embeddings_from_model_default(self):
        embedding = get_embeddings_from_model()
        self.assertTrue(embedding)
        self.assertEqual(type(embedding), BedrockEmbeddings)

    def test_get_embeddings_from_model_openai(self):
        embedding = get_embeddings_from_model(EmbeddingTypes.OPENAI_GPT_DEFAULT)
        self.assertTrue(embedding)
        self.assertEqual(type(embedding), OpenAIEmbeddings)


# get_urls_from_sitemap
# Test against a known sitemap and make sure count is greater than a value

# scrape_website_pages
# Test a small known website
# use blacklist
# use whitelist
# use chunk size

# get_documents_from_folder
# filter_urls_with_blacklist
# filter_urls_with_whitelist
# chunk_up_documents
# get_documents_from_website

# OpenSearchVectorDBLoader
# load_from_documents
# load
# delete_index
# get_index_name

# Test load and search for a known document

if __name__ == '__main__':
    unittest.main()
