#!/usr/bin/env python3
"""
SOAP UserService server

Operations
----------
getUser(userId)             -> UserResponse
createUser(username,email,role) -> UserResponse
updateRole(userId, role)    -> UserResponse

Run:
    python soap_server.py

Dependencies:
    pip install flask lxml
"""

from __future__ import annotations

from flask import Flask, Response, request
from lxml import etree

app = Flask(__name__)

TNS  = "http://example.com/userservice"
SOAP = "http://schemas.xmlsoap.org/soap/envelope/"
XSD  = "http://www.w3.org/2001/XMLSchema"

USERS: dict[int, dict] = {
    42: dict(user_id=42, username="jdupont",  email="j.dupont@example.com",  role="editor"),
    43: dict(user_id=43, username="mmartin",  email="m.martin@example.com",  role="viewer"),
}
_next_id: int = 44

# ---------------------------------------------------------------------------
# Static WSDL
# ---------------------------------------------------------------------------
WSDL = f"""<?xml version="1.0" encoding="UTF-8"?>
<definitions
    xmlns="http://schemas.xmlsoap.org/wsdl/"
    xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
    xmlns:tns="{TNS}"
    xmlns:xsd="{XSD}"
    targetNamespace="{TNS}" name="UserService">
  <types>
    <xsd:schema targetNamespace="{TNS}">
      <xsd:complexType name="GetUserRequest">
        <xsd:sequence><xsd:element name="userId" type="xsd:int"/></xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="CreateUserRequest">
        <xsd:sequence>
          <xsd:element name="username" type="xsd:string"/>
          <xsd:element name="email"    type="xsd:string"/>
          <xsd:element name="role"     type="xsd:string"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="UpdateRoleRequest">
        <xsd:sequence>
          <xsd:element name="userId" type="xsd:int"/>
          <xsd:element name="role"   type="xsd:string"/>
        </xsd:sequence>
      </xsd:complexType>
      <xsd:complexType name="UserResponse">
        <xsd:sequence>
          <xsd:element name="userId"   type="xsd:int"/>
          <xsd:element name="username" type="xsd:string"/>
          <xsd:element name="email"    type="xsd:string"/>
          <xsd:element name="role"     type="xsd:string"/>
        </xsd:sequence>
      </xsd:complexType>
    </xsd:schema>
  </types>
  <message name="GetUserRequest"><part name="p" type="tns:GetUserRequest"/></message>
  <message name="CreateUserRequest"><part name="p" type="tns:CreateUserRequest"/></message>
  <message name="UpdateRoleRequest"><part name="p" type="tns:UpdateRoleRequest"/></message>
  <message name="UserResponse"><part name="p" type="tns:UserResponse"/></message>
  <portType name="UserPortType">
    <operation name="getUser">
      <input message="tns:GetUserRequest"/><output message="tns:UserResponse"/>
    </operation>
    <operation name="createUser">
      <input message="tns:CreateUserRequest"/><output message="tns:UserResponse"/>
    </operation>
    <operation name="updateRole">
      <input message="tns:UpdateRoleRequest"/><output message="tns:UserResponse"/>
    </operation>
  </portType>
  <binding name="UserBinding" type="tns:UserPortType">
    <soap:binding style="rpc" transport="http://schemas.xmlsoap.org/soap/http"/>
    <operation name="getUser">
      <soap:operation soapAction="getUser"/>
      <input><soap:body use="literal" namespace="{TNS}"/></input>
      <output><soap:body use="literal" namespace="{TNS}"/></output>
    </operation>
    <operation name="createUser">
      <soap:operation soapAction="createUser"/>
      <input><soap:body use="literal" namespace="{TNS}"/></input>
      <output><soap:body use="literal" namespace="{TNS}"/></output>
    </operation>
    <operation name="updateRole">
      <soap:operation soapAction="updateRole"/>
      <input><soap:body use="literal" namespace="{TNS}"/></input>
      <output><soap:body use="literal" namespace="{TNS}"/></output>
    </operation>
  </binding>
  <service name="UserService">
    <port name="UserPort" binding="tns:UserBinding">
      <soap:address location="http://localhost:8000/userservice"/>
    </port>
  </service>
</definitions>"""

# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def _envelope(body_el: etree._Element) -> bytes:
    env  = etree.Element(f"{{{SOAP}}}Envelope", nsmap={"soap": SOAP, "tns": TNS})
    body = etree.SubElement(env, f"{{{SOAP}}}Body")
    body.append(body_el)
    return etree.tostring(env, xml_declaration=True, encoding="UTF-8")


def _fault(code: str, msg: str) -> bytes:
    env  = etree.Element(f"{{{SOAP}}}Envelope", nsmap={"soap": SOAP})
    body = etree.SubElement(env, f"{{{SOAP}}}Body")
    f    = etree.SubElement(body, f"{{{SOAP}}}Fault")
    etree.SubElement(f, "faultcode").text   = code
    etree.SubElement(f, "faultstring").text = msg
    return etree.tostring(env, xml_declaration=True, encoding="UTF-8")


def _user_el(user: dict) -> etree._Element:
    resp = etree.Element(f"{{{TNS}}}UserResponse")
    for tag, val in [("userId", str(user["user_id"])), ("username", user["username"]),
                     ("email", user["email"]), ("role", user["role"])]:
        etree.SubElement(resp, tag).text = val
    return resp


def _text(root: etree._Element, name: str) -> str:
    els = root.xpath(f"//*[local-name()='{name}']")
    return els[0].text.strip() if els and els[0].text else ""

# ---------------------------------------------------------------------------
# Operation handlers  — return (bytes, http_status)
# ---------------------------------------------------------------------------

def op_get_user(root):
    uid  = int(_text(root, "userId"))
    user = USERS.get(uid)
    if user is None:
        return _fault("soap:Server", f"User {uid} not found"), 500
    return _envelope(_user_el(user)), 200


def op_create_user(root):
    global _next_id
    USERS[_next_id] = dict(user_id=_next_id, username=_text(root, "username"),
                           email=_text(root, "email"), role=_text(root, "role"))
    payload = _envelope(_user_el(USERS[_next_id])), 200
    _next_id += 1
    return payload


def op_update_role(root):
    uid  = int(_text(root, "userId"))
    user = USERS.get(uid)
    if user is None:
        return _fault("soap:Server", f"User {uid} not found"), 500
    user["role"] = _text(root, "role")
    return _envelope(_user_el(user)), 200


HANDLERS = {"getUser": op_get_user, "createUser": op_create_user, "updateRole": op_update_role}

# ---------------------------------------------------------------------------
# Flask routes
# ---------------------------------------------------------------------------

@app.route("/userservice", methods=["GET"])
def wsdl():
    return Response(WSDL, mimetype="text/xml")


@app.route("/userservice", methods=["POST"])
def soap_endpoint():
    action = request.headers.get("SOAPAction", "").strip('"').strip()
    try:
        root = etree.fromstring(request.data)
    except etree.XMLSyntaxError as exc:
        return Response(_fault("soap:Client", str(exc)), status=400, mimetype="text/xml")

    if not action:
        body_el = root.find(f"{{{SOAP}}}Body")
        if body_el is not None and len(body_el):
            action = etree.QName(body_el[0].tag).localname

    handler = HANDLERS.get(action)
    if handler is None:
        return Response(_fault("soap:Client", f"Unknown action: {action}"),
                        status=400, mimetype="text/xml")

    body, status = handler(root)
    return Response(body, status=status, mimetype="text/xml")


if __name__ == "__main__":
    print("SOAP service  : http://localhost:8000/userservice")
    print("WSDL contract : http://localhost:8000/userservice?wsdl")
    app.run(host="0.0.0.0", port=8000, debug=False)
