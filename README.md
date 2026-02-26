# Comparative Analysis of Service-Oriented Communication Technologies

This project contains a written academic report comparing four major API communication
paradigms: **SOAP/WSDL**, **REST**, **GraphQL**, and **gRPC**. The report is written in
LaTeX and compiles to a PDF of exactly 10 pages.

---

## What This Report Is About

Modern software systems rarely live on a single machine. They are made up of many services
that talk to each other over a network. The question of *how* those services communicate
is one of the most important architectural decisions you will make. This report examines
four different answers to that question, explains the reasoning behind each one, and helps
you understand when to choose which.

---

## Repository Structure

```
projet-microservice/
├── report.tex              # LaTeX source of the report (10 pages)
├── report.pdf              # Compiled PDF
├── README.md               # This file
└── examples/
    ├── requirements.txt    # All Python dependencies
    ├── soap/
    │   ├── soap_server.py  # SOAP server using Spyne
    │   └── soap_client.py  # SOAP client using Zeep
    ├── rest/
    │   ├── rest_server.py  # REST server using Flask
    │   └── rest_client.py  # REST client using requests
    ├── graphql/
    │   ├── graphql_server.py  # GraphQL server using Strawberry + Uvicorn
    │   └── graphql_client.py  # GraphQL client using requests
    └── grpc/
        ├── user_service.proto  # Protobuf service definition
        ├── generate_proto.py   # Generates pb2 files from the proto
        ├── grpc_server.py      # gRPC server
        └── grpc_client.py      # gRPC client
```

---

## Prerequisites

### LaTeX (to compile the report)

**On Ubuntu / Debian:**
```bash
sudo apt update && sudo apt install texlive-full
```

**On macOS:**
```bash
brew install --cask mactex
```

**On Windows:** install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/).

### Python (to run the examples)

Python 3.10 or later is required. Install all dependencies at once:
```bash
pip install -r examples/requirements.txt
```

---

## How to Compile the Report

Run `pdflatex` twice (the second pass resolves the table of contents page numbers):

```bash
cd /home/khaldoun/projet-microservice
pdflatex report.tex
pdflatex report.tex
```

`report.pdf` will appear in the same folder. To clean up auxiliary files afterwards:
```bash
rm -f report.aux report.log report.toc report.out
```

---

## Report Structure

| Section | Content |
|---|---|
| **1 — Introduction** | Service-oriented computing overview, motivation, brief intro to all four technologies |
| **2 — Technology Analysis** | SOAP, REST, GraphQL, gRPC each analysed across: architecture, strengths, weaknesses, stack, data encoding, environments, security, use cases |
| **3 — Practical Examples** | WSDL + SOAP envelopes · HTTP/JSON REST requests · GraphQL SDL + query/response · gRPC .proto + Python server + Python client |
| **4 — Comparative Table** | 16-row summary across all four technologies |
| **5 — Conclusion** | When each approach is most suitable, industry trends |
| **References** | 8 primary sources |

---

## Running the Python Examples

All examples use the same domain: a `UserService` managing user records. Start each
server in one terminal, then run the client in a second terminal.

### SOAP (Spyne server + Zeep client)

```bash
# Terminal 1
cd examples/soap
python soap_server.py
# WSDL available at http://localhost:8000/?wsdl

# Terminal 2
cd examples/soap
python soap_client.py
```

### REST (Flask server + requests client)

```bash
# Terminal 1
cd examples/rest
python rest_server.py
# API at http://localhost:5000/api/users

# Terminal 2
cd examples/rest
python rest_client.py
```

### GraphQL (Strawberry server + requests client)

```bash
# Terminal 1
cd examples/graphql
python graphql_server.py
# GraphiQL playground at http://localhost:4000/graphql

# Terminal 2
cd examples/graphql
python graphql_client.py
```

### gRPC (protoc + Python server + Python client)

```bash
# Step 1: generate the Python bindings from the .proto file
cd examples/grpc
python generate_proto.py
# Produces user_service_pb2.py and user_service_pb2_grpc.py

# Terminal 1: start the server
python grpc_server.py
# Listening on port 50051

# Terminal 2: run the client
python grpc_client.py
```

---

## The Four Technologies at a Glance

### SOAP / WSDL
- **Origin**: Late 1990s, standardised by W3C and OASIS.
- **Key idea**: Strict XML envelope protocol with a formal WSDL contract and WS-* extensions.
- **Best for**: Enterprise systems, banking, healthcare, anywhere a legal-grade contract and message-level security are required.
- **Avoid when**: Building public APIs, mobile backends, or any context where simplicity matters.

### REST
- **Origin**: Defined by Roy Fielding in his 2000 doctoral dissertation.
- **Key idea**: Use HTTP's existing methods and status codes to act on resources identified by URIs.
- **Best for**: Public APIs, mobile backends, SaaS platforms, any context where developer accessibility and HTTP caching are valuable.
- **Avoid when**: You need low-latency binary communication between internal services or clients have very diverse data requirements.

### GraphQL
- **Origin**: Developed at Facebook in 2012, open-sourced in 2015.
- **Key idea**: Expose a single endpoint with a typed schema; let clients declare exactly what data they need.
- **Best for**: Frontend data layers, backend-for-frontend aggregation, mobile applications with diverse data needs.
- **Avoid when**: You have a simple API with uniform clients, or HTTP caching is critical to your infrastructure.

### gRPC
- **Origin**: Developed by Google, open-sourced in 2016.
- **Key idea**: Define services in `.proto` files, generate code automatically, communicate over HTTP/2 using compact binary Protocol Buffer messages.
- **Best for**: Internal microservice communication, polyglot systems, latency-sensitive services, real-time streaming, IoT and ML workloads.
- **Avoid when**: Your clients are browsers (without a proxy), or you are building a public API for third-party developers.

---

## References

- Fielding, R.T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*. UC Irvine.
- W3C (2007). *SOAP Version 1.2, Part 1*.
- W3C (2007). *WSDL Version 2.0 Part 1: Core Language*.
- The GraphQL Foundation (2021). *GraphQL Specification, October 2021*. https://spec.graphql.org/
- Google LLC (2024). *gRPC Documentation*. https://grpc.io/docs/
- Google LLC (2024). *Protocol Buffers Developer Guide*. https://protobuf.dev/
- Masse, M. (2011). *REST API Design Rulebook*. O'Reilly Media.
- Richardson, L. and Amundsen, M. (2013). *RESTful Web APIs*. O'Reilly Media.


---

## What This Report Is About

Modern software systems rarely live on a single machine. They are made up of many services
that talk to each other over a network. The question of *how* those services communicate
is one of the most important architectural decisions you will make. This report examines
four different answers to that question, explains the reasoning behind each one, and helps
you understand when to choose which.

---

## Repository Structure

```
projet-microservice/
├── report.tex      # The full LaTeX source of the report
├── report.pdf      # The compiled PDF (generated after running pdflatex)
└── README.md       # This file
```

---

## Prerequisites

To compile the report yourself, you need a LaTeX distribution installed on your machine.

**On Ubuntu / Debian:**
```bash
sudo apt update
sudo apt install texlive-full
```

**On macOS (with Homebrew):**
```bash
brew install --cask mactex
```

**On Windows:**
Download and install [MiKTeX](https://miktex.org/) or
[TeX Live](https://www.tug.org/texlive/).

The following LaTeX packages are used by the report. They are included in
`texlive-full` / MiKTeX by default:

| Package | Purpose |
|---|---|
| `inputenc`, `fontenc` | UTF-8 encoding and font encoding |
| `geometry` | Page margins |
| `hyperref` | Clickable links in the table of contents |
| `listings` | Code syntax highlighting |
| `xcolor` | Colors for syntax highlighting |
| `booktabs`, `longtable`, `array` | Tables |
| `setspace` | 1.5x line spacing |
| `parskip` | Paragraph spacing |
| `microtype` | Improved typesetting |
| `fancyhdr` | Headers and footers |
| `titlesec` | Section title formatting |

---

## How to Compile

Open a terminal in the project folder and run `pdflatex` **twice**. The second run is
needed so that LaTeX can resolve the table of contents page numbers correctly.

```bash
cd /home/khaldoun/projet-microservice

pdflatex report.tex
pdflatex report.tex
```

After the second run, `report.pdf` will appear in the same folder. Open it with any PDF
viewer.

If you want to avoid the clutter of auxiliary files (`.aux`, `.log`, `.toc`, etc.) you
can use `latexmk`, which handles multiple passes automatically:

```bash
latexmk -pdf report.tex
```

To clean up auxiliary files after compiling:
```bash
latexmk -c
```

---

## Report Structure

### Section 1 — Introduction

Explains what service-oriented computing is and why the choice of communication technology
matters. Briefly introduces each of the four technologies and sets the stage for the
detailed analysis that follows.

### Section 2 — Technology Analysis by Dimension

The heart of the report. Each of the four technologies gets its own subsection structured
around the same eight evaluation criteria:

1. **Architecture and Principles** — How the technology is designed, what constraints it
   imposes, and how clients and servers interact.
2. **Advantages and Strengths** — What it does particularly well.
3. **Disadvantages and Challenges** — Where it struggles or imposes costs.
4. **Underlying Technology Stack** — What languages, frameworks, and protocols it relies on.
5. **Data Formats and Encoding** — How messages are represented and the impact on size
   and speed.
6. **Typical Execution Environments** — Where you are most likely to encounter it in
   production.
7. **Security Model** — How authentication, authorization, and encryption are handled.
8. **Use Cases** — When it is the right choice and when it is the wrong one.

### Section 3 — Practical Examples

Each technology is illustrated with working code built around a common `UserService`
domain, so you can compare them directly:

- **SOAP/WSDL**: A complete WSDL contract plus the SOAP request and response XML envelopes
  for a `getUser` operation.
- **REST**: HTTP GET and POST requests and responses in JSON, showing how the same user
  resource is read and created.
- **GraphQL**: A schema definition in SDL, a query that fetches only the fields the client
  needs (including related posts), and the server response.
- **gRPC**: A `.proto` file defining the service, a Python server that implements it, and
  a Python client that calls all three RPC methods including a streaming one.

### Section 4 — Comparative Summary Table

A single table comparing all four technologies across 16 dimensions at a glance.
Useful as a quick reference when making architectural decisions.

### Section 5 — Conclusion

Discusses when each technology is most appropriate, reflects on evolving industry trends,
and argues that these four paradigms are complementary rather than competing.

---

## The Four Technologies at a Glance

### SOAP / WSDL

- **Origin**: Late 1990s, standardised by W3C and OASIS.
- **Key idea**: Strict protocol with XML envelopes and a formal WSDL contract.
- **Best for**: Enterprise systems, banking, healthcare, anywhere a legal-grade contract
  and message-level security are required.
- **Avoid when**: Building public APIs, mobile backends, or anything where simplicity and
  developer accessibility matter.

### REST

- **Origin**: Defined by Roy Fielding in his 2000 doctoral dissertation.
- **Key idea**: Use HTTP's existing methods and status codes to act on resources identified
  by URIs. No extra protocol on top.
- **Best for**: Public APIs, mobile backends, web applications, any context where
  developer accessibility and HTTP caching are valuable.
- **Avoid when**: You need low-latency binary communication between internal services, or
  when clients have very diverse data requirements.

### GraphQL

- **Origin**: Developed at Facebook in 2012, open-sourced in 2015.
- **Key idea**: Expose a single endpoint with a typed schema. Let clients declare exactly
  what data they need in each query.
- **Best for**: Frontend-facing data layers, backend-for-frontend aggregation services,
  mobile applications, any context where different clients need different shapes of the
  same data.
- **Avoid when**: You have a simple API with uniform clients, or when HTTP caching is
  critical to your infrastructure.

### gRPC

- **Origin**: Developed by Google, open-sourced in 2016.
- **Key idea**: Define services in `.proto` files, generate code automatically, communicate
  over HTTP/2 using compact binary Protocol Buffer messages.
- **Best for**: Internal microservice communication, polyglot systems, latency-sensitive
  services, real-time streaming, IoT and machine learning workloads.
- **Avoid when**: Your clients are browsers (without an additional proxy layer), or when
  you are building a public API for third-party developers unfamiliar with protobuf.

---

## Code Example Languages

All practical examples in the report are written in:

- **XML** — WSDL and SOAP envelopes
- **JSON** — REST and GraphQL requests and responses
- **GraphQL SDL** — GraphQL schema definition
- **Protocol Buffers** — gRPC service and message definitions
- **Python** — gRPC server and client implementation

---

## References

The report cites the following primary sources:

- Fielding, R.T. (2000). *Architectural Styles and the Design of Network-based Software
  Architectures*. Doctoral dissertation, UC Irvine.
- W3C (2007). *SOAP Version 1.2, Part 1*.
- W3C (2007). *WSDL Version 2.0 Part 1: Core Language*.
- The GraphQL Foundation (2021). *GraphQL Specification, October 2021 Edition*.
- Google LLC (2024). *gRPC Documentation*. https://grpc.io/docs/
- Google LLC (2024). *Protocol Buffers Developer Guide*. https://protobuf.dev/
- Masse, M. (2011). *REST API Design Rulebook*. O'Reilly Media.
- Richardson, L. and Amundsen, M. (2013). *RESTful Web APIs*. O'Reilly Media.
# microservice
