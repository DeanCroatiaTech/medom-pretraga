import asyncio
import os
import ssl
from typing import Any, Dict, List

import certifi
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_tavily import TavilyCrawl, TavilyExtract, TavilyMap
from rich import Console
from rich.panel import Panel
from sqlalchemy.testing.suite.test_reflection import metadata
from logger import Colors, log_error, log_header, log_info, log_success, log_warning

console = Console()
load_dotenv()

# Configure SSL context to use certifi certificates
ssl_context = ssl.create_default_context(cafile=certifi.where())
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()


embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    show_progress_bar=False,
    chunk_size=50,
    retry_min_seconds=10,
)
chroma = Chroma(persist_directory="chroma_db", embedding_function=embeddings)
vectorstore = PineconeVectorStore(
    index_name="langchain-doc-index", embedding=embeddings
)
tavily_extract = TavilyExtract()
tavily_map = TavilyMap(max_depth=5, max_breadth=20, max_pages=1000)
tavily_crawl = TavilyCrawl()


def chunk_urls(urls: List[str], chunk_size: int = 3) -> List[List[str]]:
    """Split URLs into chunks of specified size."""
    chunks = []
    for i in range(0, len(urls), chunk_size):
        chunk = urls[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

async def extract_batch(urls: List[str], batch_num: int) -> List[Dict[str, Any]]:
    """Extract documents from a batch of URLs."""
    try:
        console.print(f"🔄 Processing batch {batch_num} with {len(urls)} URLs", style="blue")
        docs = await tavily_extract.ainvoke(input={"urls": urls})
        results = docs.get('results', [])
        console.print(f"✅ Batch {batch_num} completed - extracted {len(results)} documents", style="green")
        return results
    except Exception as e:
        console.print(f"❌ Batch {batch_num} failed: {e}", style="red")
        return []


async def index_documents_async(documents: List[Document], batch_size: int = 50):
    """Process documents in batches asynchronously."""
    log_header("VECTOR STORAGE PHASE")
    log_info(
        f"📚 VectorStore Indexing: Preparing to add {len(documents)} documents to vector store",
        Colors.DARKCYAN,
    )

    # Create batches
    batches = [
        documents[i : i + batch_size] for i in range(0, len(documents), batch_size)
    ]

    log_info(
        f"📦 VectorStore Indexing: Split into {len(batches)} batches of {batch_size} documents each"
    )

    # Process all batches concurrently
    async def add_batch(batch: List[Document], batch_num: int):
        try:
            await vectorstore.aadd_documents(batch)
            log_success(
                f"VectorStore Indexing: Successfully added batch {batch_num}/{len(batches)} ({len(batch)} documents)"
            )
        except Exception as e:
            log_error(f"VectorStore Indexing: Failed to add batch {batch_num} - {e}")
            return False
        return True

    # Process batches concurrently
    tasks = [add_batch(batch, i + 1) for i, batch in enumerate(batches)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Count successful batches
    successful = sum(1 for result in results if result is True)

    if successful == len(batches):
        log_success(
            f"VectorStore Indexing: All batches processed successfully! ({successful}/{len(batches)})"
        )
    else:
        log_warning(
            f"VectorStore Indexing: Processed {successful}/{len(batches)} batches successfully"
        )


async def main():

    # Initialize TavilyMap with custom settings
    tavily_map = TavilyMap(
        max_depth=3,        # Crawl up to 3 levels deep
        max_breadth=15,     # Follow up to 15 links per page
        max_pages=150        # Limit to 50 total pages for demo
    )

    print("✅ TavilyMap initialized successfully!")


    # Example website to map
    demo_url = "https://medom-nekretnine.com/stan/"

    console.print(f"🔍 Mapping website structure for: {demo_url}", style="bold blue")
    console.print("This may take a moment...")

    # Map the website structure
    site_map = tavily_map.invoke(demo_url)

    # Display results
    urls = site_map.get('results', [])
    console.print(f"\n✅ Successfully mapped {len(urls)} URLs!", style="bold green")

    # Show first 10 URLs as examples
    console.print("\n📋 First 50 discovered URLs:", style="bold yellow")
    for i, url in enumerate(urls[:50], 1):
        console.print(f"  {i:2d}. {url}")

    if len(urls) > 10:
        console.print(f"  ... and {len(urls) - 50} more URLs")

    # Select a few interesting URLs for extraction
    console.print(f"📚 Extracting content from {len(urls)} URLs...", style="bold blue")

    # Extract content
    extraction_result = await tavily_extract.ainvoke(input={"urls": urls})

    # Display results
    extracted_docs = extraction_result.get('results', [])
    console.print(f"\n✅ Successfully extracted {len(extracted_docs)} documents!", style="bold green")

    # Show summary of each extracted document
    for i, doc in enumerate(extracted_docs, 1):
        url = doc.get('url', 'Unknown')
        content = doc.get('raw_content', '')

        # Create a panel for each document
        panel_content = f"""URL: {url}
            Content Length: {len(content):,} characters
            Preview: {content}..."""

        console.print(Panel(panel_content, title=f"Document {i}", border_style="blue"))
        print()  # Add spacing

    # Process a larger set of URLs in batches
    url_batches = chunk_urls(urls[:100], chunk_size=10)

    console.print(f"📦 Processing URLs in {len(url_batches)} batches", style="bold yellow")

    # Process batches concurrently
    tasks = [extract_batch(batch, i + 1) for i, batch in enumerate(url_batches)]
    batch_results = await asyncio.gather(*tasks)

    # Flatten results
    all_extracted = []
    for batch_result in batch_results:
        all_extracted.extend(batch_result)

    for result in batch_results:
        all_extracted.extend(result)

    all_docs = [Document(page_content=item['raw_content'], metadata={"source": item['url']}) for item in all_extracted]
    console.print(f"\n🎉 Batch processing complete! Total documents extracted: {len(all_extracted)}", style="bold green")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    splitted_docs = text_splitter.split_documents(all_docs)

    log_success(
        f"Text Splitter: Created {len(splitted_docs)} chunks from {len(all_docs)} documents"
    )

    # Process documents asynchronously
    await index_documents_async(splitted_docs, batch_size=500)

    log_header("PIPELINE COMPLETE")
    log_success("🎉 Documentation ingestion pipeline finished successfully!")
    log_info("📊 Summary:", Colors.BOLD)
    log_info(f"   • URLs mapped: {len(site_map['results'])}")
    log_info(f"   • Documents extracted: {len(all_docs)}")
    log_info(f"   • Chunks created: {len(splitted_docs)}")

    log_success("Finish")

if __name__ == "__main__":
    asyncio.run(main())