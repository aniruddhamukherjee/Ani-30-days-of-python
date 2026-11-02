# Graph Report - my_enterprise_api  (2026-11-01)

## Corpus Check
- Corpus is ~7,934 words - fits in a single context window. You may not need a graph.

## Summary
- 155 nodes · 213 edges · 11 communities (7 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `79b39628`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Product API Endpoints
- Exception Handling
- App Lifecycle & Health
- Database Infrastructure (Docker)
- Base CRUD Service
- Database Session & ORM
- API Service Infrastructure (Docker)
- Security & Authentication
- Product Schemas & DTOs
- Application Configuration

## God Nodes (most connected - your core abstractions)
1. `Product` - 9 edges
2. `api` - 9 edges
3. `db` - 8 edges
4. `BaseService` - 7 edges
5. `update_product()` - 7 edges
6. `AppException` - 6 edges
7. `create_product()` - 6 edges
8. `get_product()` - 6 edges
9. `setup_exception_handlers()` - 6 edges
10. `ProductBase` - 5 edges

## Surprising Connections (you probably didn't know these)
- `create_product()` --references--> `ProductCreate`  [EXTRACTED]
  app/api/v1/endpoints/products.py → app/schemas/__init__.py
- `update_product()` --references--> `ProductUpdate`  [EXTRACTED]
  app/api/v1/endpoints/products.py → app/schemas/__init__.py
- `create_product()` --references--> `Product`  [EXTRACTED]
  app/api/v1/endpoints/products.py → app/models/__init__.py
- `get_product()` --references--> `Product`  [EXTRACTED]
  app/api/v1/endpoints/products.py → app/models/__init__.py
- `get_product_by_sku()` --references--> `Product`  [EXTRACTED]
  app/api/v1/endpoints/products.py → app/models/__init__.py

## Import Cycles
- None detected.

## Communities (11 total, 4 thin omitted)

### Community 0 - "Product API Endpoints"
Cohesion: 0.13
Nodes (7): create_product(), delete_product(), get_product(), get_product_by_sku(), list_products(), update_product(), Product

### Community 1 - "Exception Handling"
Cohesion: 0.14
Nodes (4): AppException, NotFoundException, setup_exception_handlers(), UnauthorizedException

### Community 2 - "App Lifecycle & Health"
Cohesion: 0.12
Nodes (3): health_check(), lifespan(), test_health_check()

### Community 3 - "Database Infrastructure (Docker)"
Cohesion: 0.12
Nodes (16): container_name, environment, healthcheck, image, ports, restart, volumes, interval (+8 more)

### Community 6 - "API Service Infrastructure (Docker)"
Cohesion: 0.15
Nodes (13): build, container_name, depends_on, env_file, environment, ports, restart, volumes (+5 more)

### Community 7 - "Security & Authentication"
Cohesion: 0.17
Nodes (3): create_access_token(), get_password_hash(), verify_password()

### Community 8 - "Product Schemas & DTOs"
Cohesion: 0.21
Nodes (4): ProductBase, ProductCreate, ProductResponse, ProductUpdate

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseService` connect `Base CRUD Service` to `Database Session & ORM`?**
  _High betweenness centrality (0.131) - this node is a cross-community bridge._
- **Should `Product API Endpoints` be split into smaller, more focused modules?**
  _Cohesion score 0.12615384615384614 - nodes in this community are weakly interconnected._
- **Why does `setup_exception_handlers()` connect `Exception Handling` to `App Lifecycle & Health`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Should `Exception Handling` be split into smaller, more focused modules?**
  _Cohesion score 0.1437908496732026 - nodes in this community are weakly interconnected._
- **Should `App Lifecycle & Health` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `Database Infrastructure (Docker)` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._