#!/usr/bin/env python3
"""
SOAP UserService client — pure Python, no Zeep dependency.

Builds SOAP envelopes with lxml, sends them over HTTP with requests,
and parses the XML response.

Start the server first:
    python soap_server.py

Then run:
    python soap_client.py

Dependencies:
    pip install requests lxml
"""

from __future__ import annotations

import requests
from lxml import etree

ENDPOINT = "http://localhost:8000/userservice"
TNS      = "http://example.com/userservice"
SOAP_NS  = "http://schemas.xmlsoap.org/soap/envelope/"

# ---------------------------------------------------------------------------
# Build helpers
# ---------------------------------------------------------------------------

def _build_envelope(action: str, **fields) -> bytes:
    """Construct a minimal SOAP 1.1 request envelope for the given action."""
    env  = etree.Element(f"{{{SOAP_NS}}}Envelope",
                         nsmap={"soap": SOAP_NS, "tns": TNS})
    body = etree.SubElement(env, f"{{{SOAP_NS}}}Body")
    op   = etree.SubElement(body, f"{{{TNS}}}{action}")
    for tag, val in fields.items():
        etree.SubElement(op, tag).text = str(val)
    return etree.tostring(env, xml_declaration=True, encoding="UTF-8")


def _post(action: str, **fields) -> etree._Element:
    """Send a SOAP request and return the parsed XML root."""
    body = _build_envelope(action, **fields)
    resp = requests.post(
        ENDPOINT,
        data=body,
        headers={"Content-Type": "text/xml; charset=utf-8",
                 "SOAPAction": f'"{action}"'},
    )
    return etree.fromstring(resp.content)


def _field(root: etree._Element, name: str) -> str:
    """Extract the text of the first element matching local-name."""
    els = root.xpath(f"//*[local-name()='{name}']")
    return els[0].text if els and els[0].text else ""


def print_user(label: str, root: etree._Element) -> None:
    fault = root.xpath("//*[local-name()='faultstring']")
    if fault:
        print(f"  {label}: FAULT -> {fault[0].text}")
        return
    print(f"  {label}:")
    print(f"    userId   = {_field(root, 'userId')}")
    print(f"    username = {_field(root, 'username')}")
    print(f"    email    = {_field(root, 'email')}")
    print(f"    role     = {_field(root, 'role')}")

# ---------------------------------------------------------------------------
# Demo calls
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== getUser (id=42) ===")
    print_user("Result", _post("getUser", userId=42))

    print("\n=== getUser (id=99, non-existent) ===")
    print_user("Result", _post("getUser", userId=99))

    print("\n=== createUser ===")
    print_user("Created", _post("createUser",
                                 username="lbernard",
                                 email="l.bernard@example.com",
                                 role="admin"))

    print("\n=== updateRole (id=42 -> reviewer) ===")
    print_user("Updated", _post("updateRole", userId=42, role="reviewer"))
