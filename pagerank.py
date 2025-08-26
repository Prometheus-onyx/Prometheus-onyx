import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus.get(page, set())
    num_links = len(links)
    distribution = dict()

    for p in corpus:
        if p in links:
            distribution[p] = damping_factor / num_links if num_links > 0 else 0
        else:
            distribution[p] = (1 - damping_factor) / len(corpus)

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize PageRank values
    ranks = {page: 1 / len(corpus) for page in corpus}
    for _ in range(n):
        # Sample a page according to the transition model
        page = random.choices(list(corpus.keys()), weights=list(ranks.values()))[0]
        # Update the PageRank values according to the transition model
        distribution = transition_model(corpus, page, damping_factor)
        for p in ranks:
            ranks[p] = ranks[p] * (1 - damping_factor) + distribution.get(p, 0) * damping_factor
    # Normalize the PageRank values
    total = sum(ranks.values())
    for p in ranks:
        ranks[p] /= total
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {page: 1 / len(corpus) for page in corpus}
    while True:
        new_ranks = dict()
        for page in corpus:
            new_ranks[page] = (1 - damping_factor) / len(corpus)
            for link in corpus:
                if page in corpus[link]:
                    new_ranks[page] += damping_factor * ranks[link] / len(corpus[link])
        # Check for convergence
        if all(abs(new_ranks[page] - ranks[page]) < 0.001 for page in ranks):
            break
        ranks = new_ranks
    return ranks


if __name__ == "__main__":
    main()


#0114656849 - SKIM