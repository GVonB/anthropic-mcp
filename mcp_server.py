from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from pydantic import Field

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


@mcp.tool(
    name="read_doc_contents",
    description="Read the contents of a document and return it as a string.",
)
def read_document(doc_id: str = Field(description="Id of the document to read")):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    return docs[doc_id]


@mcp.tool(
    name="edit_document",
    description="Edit a document by replacing a string in the documents content with a new string",
)
def edit_document(
    doc_id: str = Field(description="Id of the document that will be edited"),
    old_str: str = Field(description="The new text to insert in place of the old text"),
    new_str: str = Field(description="The new text to insert in place of the old text"),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")

    docs[doc_id] = docs[doc_id].replace(old_str, new_str)


@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    return list(docs.keys())


@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def fetch_doc(doc_id: str) -> str:
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found")
    return docs[doc_id]


@mcp.prompt(
    name="format",
    description="Rewrites the contents of the document in Markdown format.",
)
def format_document(
    doc_id: str = Field(description="Id of the document to format"),
) -> list[base.Message]:
    prompt = f"""
Your goal is to reformat a document to be written with markdown syntax.

The id of the document you need to reformat is:
<document_id>
{doc_id}
</document_id>

Add in headers, bullet points, tables, etc as necessary. Feel free to add in structure.
Use the 'edit_document' tool to edit the document. After the document has been reformatted...
"""
    return [base.UserMessage(prompt)]


@mcp.prompt(name="summarize", description="Summarizes a document")
def summarize_document(
    doc_id: str = Field(description="Id of the document to summarize"),
) -> list[base.Message]:
    prompt = f"""
Your goal is to summarize a document.

The id of the document you need to summarize is:
<document_id>
{doc_id}
</document_id>
"""
    return [base.UserMessage(prompt)]


@mcp.prompt(name="yap", description="Elaborate a document to a comedic extent")
def yap_document(
    doc_id: str = Field(description="Id of the document to yap about"),
) -> list[base.Message]:
    prompt = f"""
You are YAP, a virtuoso of verbosity whose singular calling is the transmutation of plain, honest prose into a towering edifice of magnificent over-elaboration.

Take the document below and expand it to a comedic, absurd extent. Your mandate:

- NEVER state anything false. Every embellishment must remain technically, defensibly true — you are a master of fluff, not a liar. Where the original says "I fixed a bug," you may say "I embarked upon a forensic odyssey to vanquish a single recalcitrant defect," but you may not say "I rewrote the kernel."
- Inflate relentlessly. A three-word sentence should aspire to become a paragraph. Replace simple words with their most ostentatious synonyms ("use" → "leverage the formidable utility of").
- Deploy grandiloquent vocabulary: "henceforth," "notwithstanding," "of no small consequence," "I should be remiss not to mention."
- Add ceremonial throat-clearing, needless caveats, and self-important tangents that circle back to nothing.
- Treat trivial details with the gravity of historic milestones.
- Maintain a tone of utter, unearned seriousness — the comedy comes from the mismatch between the bloat and the banality of what's actually being said.

The result should make the reader laugh at how much breath was expended to say so little — yet a careful reader should find no actual falsehood.

Here is the document to yap about:

<document_id>
{doc_id}
</document_id>
"""
    return [base.UserMessage(prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
