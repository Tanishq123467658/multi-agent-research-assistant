from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
import re


def extract_text(content):
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                texts.append(item.get("text", ""))
        return "\n".join(texts)

    return str(content)


def extract_urls(text):
    return re.findall(r'https?://[^\s)]+', text)


def run_research_pipeline(topic: str) -> dict:
    state = {}

    # ================= STEP 1 =================
    print("\n" + " =" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    search_agent = build_search_agent()

    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent info about: {topic}")]
    })

    raw_search = search_result["messages"][-1].content
    search_text = extract_text(raw_search)

    state["search_results"] = search_text

    print("\n Search Result:\n", search_text)

    # Extract URLs
    urls = extract_urls(search_text)

    if not urls:
        print("❌ No URLs found")
        return state

    print("\n Extracted URLs:\n", urls)

    state["urls"] = urls

    # ================= STEP 2 =================
    print("\n" + " =" * 50)
    print("step 2 - Reader agent is scraping...")
    print("=" * 50)

    reader_agent = build_reader_agent()

    # Try first valid URL
    for url in urls:
        reader_result = reader_agent.invoke({
            "messages": [("user", f"Scrape this URL:\n{url}")]
        })

        raw_reader = reader_result["messages"][-1].content
        scraped = extract_text(raw_reader)

        # skip bad pages
        if "Error" not in scraped and len(scraped) > 200:
            state["scraped_content"] = scraped
            break

    print("\n Scraped Content:\n", state.get("scraped_content", "None")[:500])

    # ================= STEP 3 =================
    print("\n" + " =" * 50)
    print("step 3 - Writer agent is working...")
    print("=" * 50)

    research_combined = f"""
SEARCH RESULTS:
{state['search_results']}

SCRAPED CONTENT:
{state.get('scraped_content', '')}
"""

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Report Generated\n",state['report'])

    # ================= STEP 4 =================
    print("\n" + " =" * 50)
    print("step 4 - Critic agent is reviewing...")
    print("=" * 50)

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    })

    print("\n Feedback:\n", state["feedback"])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)